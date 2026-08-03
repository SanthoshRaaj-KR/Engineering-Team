import subprocess
import sys
from pathlib import Path

from crewai.tools import tool


SANDBOX_DIR = Path(__file__).parents[3] / "sandbox"
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

RUN_TIMEOUT_SECONDS = 60
MAX_OUTPUT_CHARS = 8000


def _resolve(filename: str) -> Path:
    """Resolve a filename inside the sandbox, refusing paths that escape it."""
    path = (SANDBOX_DIR / filename).resolve()
    if not path.is_relative_to(SANDBOX_DIR.resolve()):
        raise ValueError(f"Path escapes the sandbox directory: {filename}")
    return path


def _truncate(text: str) -> str:
    if len(text) <= MAX_OUTPUT_CHARS:
        return text
    return text[:MAX_OUTPUT_CHARS] + f"\n...[truncated, {len(text)} chars total]"


def _format_result(label: str, completed: subprocess.CompletedProcess) -> str:
    status = "SUCCESS" if completed.returncode == 0 else "FAILED"
    return _truncate(
        f"{label}\n"
        f"exit_code: {completed.returncode} ({status})\n"
        f"--- stdout ---\n{completed.stdout or '(empty)'}\n"
        f"--- stderr ---\n{completed.stderr or '(empty)'}"
    )


@tool("List Sandbox Files")
def list_sandbox_files() -> str:
    """List every file currently present in the sandbox directory, including
    files inside subdirectories. Use this before reading or writing so you know
    what already exists."""
    paths = sorted(
        path.relative_to(SANDBOX_DIR).as_posix()
        for path in SANDBOX_DIR.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )
    return "\n".join(paths) if paths else "The sandbox is empty."


@tool("Read Sandbox File")
def read_sandbox_file(filename: str) -> str:
    """Read a text file from the sandbox by its path relative to the sandbox
    root, for example 'app/main.py'. Use this to inspect code that another
    engineer has already written before you modify or review it."""
    try:
        path = _resolve(filename)
    except ValueError as exc:
        return str(exc)
    if not path.is_file():
        return f"No such file in the sandbox: {filename}"
    return _truncate(path.read_text(encoding="utf-8"))


@tool("Write Sandbox File")
def write_sandbox_file(filename: str, content: str) -> str:
    """Write text content to a sandbox file, creating or completely replacing
    it. The filename is a path relative to the sandbox root and may include
    subdirectories, for example 'app/services/parser.py' - any missing parent
    directories are created automatically. Always pass the full final content
    of the file, never a fragment or a diff."""
    try:
        path = _resolve(filename)
    except ValueError as exc:
        return str(exc)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} characters to {filename}."


@tool("Run Python File")
def run_python_file(filename: str) -> str:
    """Execute a Python file from the sandbox with the current interpreter and
    return its exit code, stdout and stderr. Use this to prove that the code you
    wrote actually imports and runs. A non-zero exit code means the code is
    broken and you must fix it before reporting the work as done."""
    try:
        path = _resolve(filename)
    except ValueError as exc:
        return str(exc)
    if not path.is_file():
        return f"No such file in the sandbox: {filename}"
    try:
        completed = subprocess.run(
            [sys.executable, str(path)],
            cwd=SANDBOX_DIR,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return (
            f"Running {filename} timed out after {RUN_TIMEOUT_SECONDS} seconds. "
            "The file probably blocks on input or starts a long-running server; "
            "guard that behaviour behind a __main__ block or a separate entrypoint."
        )
    return _format_result(f"Ran python {filename}", completed)


@tool("Run Sandbox Tests")
def run_sandbox_tests() -> str:
    """Run pytest across the whole sandbox directory and return the results.
    Use this after writing or changing tests to confirm they actually pass.
    Failing tests must be fixed before the work is reported as complete."""
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=SANDBOX_DIR,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_SECONDS * 3,
        )
    except subprocess.TimeoutExpired:
        return f"pytest timed out after {RUN_TIMEOUT_SECONDS * 3} seconds."
    except FileNotFoundError:
        return "pytest is not available in this environment."
    if "No module named pytest" in (completed.stderr or ""):
        return (
            "pytest is not installed in this environment. "
            "Verify your tests with Run Python File instead."
        )
    if completed.returncode == 5:
        return "pytest ran but collected no tests. Make sure your test files are named test_*.py."
    return _format_result("Ran pytest -q", completed)


# Engineers can inspect, write and execute code.
sandbox_engineer_tools = [
    list_sandbox_files,
    read_sandbox_file,
    write_sandbox_file,
    run_python_file,
    run_sandbox_tests,
]

# QA can inspect and execute, but never modify the implementation.
sandbox_qa_tools = [
    list_sandbox_files,
    read_sandbox_file,
    run_python_file,
    run_sandbox_tests,
]

# Backwards-compatible alias.
sandbox_tools = sandbox_engineer_tools


def _never_cache(*_args, **_kwargs) -> bool:
    return False


for _tool in sandbox_engineer_tools:
    _tool.cache_function = _never_cache
