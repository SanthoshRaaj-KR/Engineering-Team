from typing import Literal
from pydantic import BaseModel


class AIRecommendation(BaseModel):
    feature: str
    objective: str
    suggested_approach: str
    expected_benefit: str
    complexity: Literal["Low", "Medium", "High"]


class AIAssessment(BaseModel):
    ai_required: bool
    confidence: float
    reasoning: str
    recommendations: list[AIRecommendation] = []