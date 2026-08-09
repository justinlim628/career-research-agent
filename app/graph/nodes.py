from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas import SearchQueries, ExtractSkills
from tavily import TavilyClient
import os
from collections import Counter


load_dotenv()
llm = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')
structured_llm = llm.with_structured_output(SearchQueries)
extract_llm = llm.with_structured_output(ExtractSkills)

tavily_client = TavilyClient()


def generate_queries(role: str, n: int = 3) -> list[str]:
    prompt = f"For the role '{role}', generate {n} search queries to find job requirements and skills on job posting websites."
    response = structured_llm.invoke(prompt)
    queries = response.queries

    return queries


def search(queries: list[str], max_result: int = 5) -> list[dict]:
    all_results = []
    for query in queries:
        response = tavily_client.search(query, max_results=max_result)
        all_results.extend(response['results'])

    return all_results


def filter_relevance(results: list[dict], threshold: float = 0.7) -> list[dict]:
    filtered = [r for r in results if r['score'] > threshold]

    seen_url = set()
    deduped = []
    for r in filtered:
        if r['url'] not in seen_url:
            seen_url.add(r['url'])
            deduped.append(r)

    return deduped


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


def aggregate_skills(skills: list[str]) -> Counter:
    normalized = [s.strip().lower() for s in skills]

    return Counter(normalized)


def generate_report(counter: Counter, role: str) -> str:
    top_skills = counter.most_common(10)
    lines = [f"# Skill Report for {role}\n"]
    lines.append("## Top Skills\n")
    for skill, count in top_skills:
        lines.append(f"- {skill.capitalize()}: mentioned {count} times")
    return "\n".join(lines)