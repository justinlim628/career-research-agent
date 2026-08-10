from collections import Counter

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

from app.graph.state import AgentState
from app.schemas import ExtractSkills, SearchQueries

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
structured_llm = llm.with_structured_output(SearchQueries)
extract_llm = llm.with_structured_output(ExtractSkills)

tavily_client = TavilyClient()


def generate_queries(role: str, n: int = 3) -> list[str]:
    prompt = f"For the role '{role}', generate {n} search queries to find job requirements and skills on job posting websites."
    response = structured_llm.invoke(prompt)
    queries = response.queries

    return queries


def generate_queries_node(state: AgentState) -> dict:
    queries = generate_queries(state["role"], state["n"])
    return {"queries": queries}


def search(queries: list[str], max_results: int = 5) -> list[dict]:
    all_results = []
    for query in queries:
        response = tavily_client.search(query, max_results=max_results)
        all_results.extend(response["results"])

    return all_results


def search_node(state: AgentState) -> dict:
    results = search(state["queries"], state["max_results"])

    return {"search_results": results}


def filter_relevance(results: list[dict], threshold: float = 0.7) -> list[dict]:
    filtered = [r for r in results if r["score"] > threshold]

    seen_url = set()
    deduped = []
    for r in filtered:
        if r["url"] not in seen_url:
            seen_url.add(r["url"])
            deduped.append(r)

    return deduped


def filter_relevance_node(state: AgentState) -> dict:
    filtered_results = filter_relevance(state["search_results"], state["threshold"])

    return {"filtered_results": filtered_results}


def extract_skills(result: dict) -> list[str]:
    prompt = f"Extract the technical skills, tools, and concepts required for the role, based on this text:\n\n{result['content']}"
    response = extract_llm.invoke(prompt)
    return response.skills


def extract_all_skills(results: list[dict]) -> list[str]:
    all_skills = []
    for result in results:
        print(f"extracting skills in {result['url']}")
        skills = extract_skills(result)
        all_skills.extend(skills)

    return all_skills


def extract_skills_node(state: AgentState) -> dict:
    skills = extract_all_skills(state["filtered_results"])

    return {"skills": skills}


def aggregate_skills(skills: list[str]) -> Counter:
    normalized = [s.strip().lower() for s in skills]

    return Counter(normalized)


def aggregate_skills_node(state: AgentState) -> dict:
    counter = aggregate_skills(state["skills"])
    return {"aggregated_skills": dict(counter)}


def generate_report(aggregated_skills: dict, role: str) -> str:
    top_skills = Counter(aggregated_skills).most_common(10)
    lines = [f"# Skill Report for {role}\n"]
    lines.append("## Top Skills\n")
    for skill, count in top_skills:
        lines.append(f"- {skill.capitalize()}: mentioned {count} times")
    return "\n".join(lines)


def generate_report_node(state: AgentState) -> dict:
    report = generate_report(state["aggregated_skills"], state["role"])

    return {"report": report}


def increase_search_scope_node(state: AgentState) -> dict:
    print("Retrying...")
    return {
        "max_results": state["max_results"] + 5,
        "retry_count": state["retry_count"] + 1,
    }
