from typing import TypedDict


class AgentState(TypedDict):
    role: str
    n: int
    max_results: int
    threshold: float
    retry_count: int
    queries: list[str]
    search_results: list[dict]
    filtered_results: list[dict]
    skills: list[str]
    aggregated_skills: dict[str, int]
    report: str


