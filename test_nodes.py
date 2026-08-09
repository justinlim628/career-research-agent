from app.graph.nodes import (
    aggregate_skills,
    extract_all_skills,
    filter_relevance,
    generate_queries,
    generate_report,
    search,
)

result = generate_queries("AI Engineer", 3)
print(result)

search_res = search(result)
print([r["url"] for r in search_res if "url" in r])

filtered_res = filter_relevance(search_res)
print([r["url"] for r in filtered_res if "url" in r])

skills = extract_all_skills(filtered_res)
print(skills)
agg_skills = aggregate_skills(skills)
print(agg_skills.most_common(10))

report = generate_report(agg_skills, "AI Engineer")
print(report)
