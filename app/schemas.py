from pydantic import BaseModel, Field


class SearchQueries(BaseModel):
    queries: list[str] = Field(description="A list of search queries for finding job requirements")


class ExtractSkills(BaseModel):
    skills: list[str] = Field(description="Technical skills, tools, or concepts mentioned as requirements for this role")