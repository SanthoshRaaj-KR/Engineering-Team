from typing import Literal

from pydantic import BaseModel


class Issue(BaseModel):
    severity: Literal[
        "Low",
        "Medium",
        "High",
        "Critical",
    ]

    description: str

    recommendation: str


class QAReport(BaseModel):
    passed: bool

    summary: str

    issues: list[Issue]