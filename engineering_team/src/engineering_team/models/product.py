from pydantic import BaseModel

class ProductRequirementSpecification(BaseModel):
    product_overview: str
    problem_statement: str
    business_objective: str

    functional_requirements: list[str]
    non_functional_requirements: list[str]

    user_stories: list[str]

    in_scope: list[str]
    out_of_scope: list[str]

    constraints: list[str]
    assumptions: list[str]

    success_criteria: list[str]
    deliverables: list[str]

    open_questions: list[str]