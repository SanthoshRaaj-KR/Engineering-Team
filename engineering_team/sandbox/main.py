from __future__ import annotations

from analyzer import analyze_text


def format_counts(text: str) -> str:
    counts = analyze_text(text)
    return (
        f"Vowels: {counts.vowels}\n"
        f"Consonants: {counts.consonants}\n"
        f"Special Characters: {counts.special_characters}"
    )


def chat_loop() -> None:
    print("Character Counter Chat")
    print("Enter text to analyze. Type 'quit' or 'exit' to stop.")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            print("Goodbye.")
            break
        if user_input.strip().lower() in {"quit", "exit"}:
            print("Goodbye.")
            break
        print(format_counts(user_input))


if __name__ == "__main__":
    chat_loop()
