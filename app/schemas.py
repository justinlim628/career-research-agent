from pydantic import BaseModel, Field


class SearchQueries(BaseModel):
    queries: list[str] = Field(
        description="A list of search queries for finding job requirements"
    )


class ExtractSkills(BaseModel):
    skills: list[str] = Field(
        description="Technical skills, tools, or concepts mentioned as requirements for this role"
    )


class ResearchRequest(BaseModel):
    role: str
    n: int = 3
    max_results: int = 5
    threshold: float = 0.7


class ResearchResponse(BaseModel):
    report: str
    aggregated_skills: dict[str, int]
