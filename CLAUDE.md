# Career Research Agent — Project Memory

## Purpose
Learning project to gain hands-on experience with LangGraph/agentic workflows,
prioritized ahead of summarization-portfolio because target AI Engineer job
descriptions repeatedly require agent/tool-use experience the developer lacked.

## Scope
Phase 1: Research a target role (e.g. "AI Engineer") by searching job postings
and aggregating frequently-required skills into a report.
Phase 2 (not started): Resume upload + skill-gap/match analysis against
Phase 1's findings.

## Project Structure

app/
├── main.py # FastAPI app, static file serving, POST /research
├── schemas.py # ResearchRequest/Response, SearchQueries, ExtractSkills
├── graph/
│ ├── state.py # AgentState (TypedDict)
│ ├── nodes.py # all node functions + their AgentState wrappers
│ └── build.py # StateGraph assembly (nodes, edges, conditional edges)
├── static/index.html # UI
notebooks/ # evaluation/experimentation (excluded from Docker image)


## Graph Design
Linear pipeline with one retry loop:

generate_queries → search → filter_relevance
↓ (conditional: retry_search)
filtered_results < 3 AND retry_count < 3?
├─ yes → increase_scope (max_results += 5, retry_count += 1) → back to search
└─ no → extract_skills → aggregate_skills → generate_report → END

- `AgentState` splits fields into **inputs** (role, n, max_results, threshold,
  retry_count — set once in `initial_state`) vs **outputs** (queries,
  search_results, filtered_results, skills, aggregated_skills, report — filled
  progressively by nodes).
- Structured output (Pydantic + `with_structured_output`) used for
  `generate_queries` and `extract_skills`.
- `aggregate_skills` is its own node (not folded into `generate_report`)
  because the conditional-retry logic and future output-format flexibility
  needed it as a separate state field.

## Status
- [DONE] Full graph built and verified end-to-end (both the "enough results"
  and "retries then gives up" paths tested manually by varying `threshold`)
- [DONE] FastAPI `POST /research` endpoint
- [DONE] Basic HTML/JS UI (loading state + error handling)
- [DONE] Dockerized, verified working locally via `docker compose up --build`
- [TODO] Quality improvements (deliberately deferred): tighten
  `extract_skills` prompt to exclude generic/degree-requirement terms,
  add a stopword filter in `aggregate_skills`, then re-test with larger
  sample size — noise doesn't self-correct with more data because generic
  terms dominate proportionally more, not less
- [TODO] Before/after evaluation of the prompt change — planned in
  `notebooks/evaluation.ipynb` (kept out of the Docker image), comparing
  skill-extraction output on the same `filtered_results` before/after the
  prompt fix, plus a simple noise-ratio metric against a manual stopword list
- [NOT STARTED] Cloud deployment (Render, same pattern as expense-tracker)
- [NOT STARTED] Phase 2 (resume matching)