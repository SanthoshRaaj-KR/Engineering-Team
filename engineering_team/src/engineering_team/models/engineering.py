from typing import Literal

from pydantic import BaseModel


class EngineeringTask(BaseModel):
    id: int
    title: str
    description: str

    assigned_to: Literal[
        "Senior Software Engineer",
        "Innovation Engineer",
        "QA Engineer",
    ]

    priority: Literal[
        "Low",
        "Medium",
        "High",
    ]


class EngineeringExecutionPlan(BaseModel):
    project_summary: str

    implementation_strategy: str

    ai_required: bool
    ai_summary: str | None = None

    engineering_tasks: list[EngineeringTask]

    dependencies: list[str]

    assumptions: list[str]

    risks: list[str]