from pydantic import BaseModel


class ImplementationReport(BaseModel):
    summary: str

    completed_tasks: list[int]

    implementation_notes: str

    files_created: list[str]

    files_modified: list[str]
