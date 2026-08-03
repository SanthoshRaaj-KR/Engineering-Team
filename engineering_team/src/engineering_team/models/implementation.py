from pydantic import BaseModel


class TechnologyRecommendation(BaseModel):
    technology: str

    purpose: str

    reason: str

    advantages: list[str]

    disadvantages: list[str]

    production_ready: bool


class InnovationReport(BaseModel):
    summary: str

    recommendations: list[TechnologyRecommendation]


class ImplementationReport(BaseModel):
    summary: str

    completed_tasks: list[int]

    implementation_notes: str

    files_created: list[str]

    files_modified: list[str]