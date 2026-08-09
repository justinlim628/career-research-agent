from app.graph.build import app_graph

initial_state = {
    "role": "AI Engineer",
    "n": 3,
    "max_results": 5,
    "threshold": 0.7,
    "queries": [],
    "search_results": [],
    "filtered_results": [],
    "skills": [],
    "aggregated_skills": {},
    "report": "",
}

result = app_graph.invoke(initial_state)
print(result["report"])
