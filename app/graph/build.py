from langgraph.graph import END, StateGraph

from app.graph.nodes import (
    aggregate_skills_node,
    extract_skills_node,
    filter_relevance_node,
    generate_queries_node,
    generate_report_node,
    search_node,
)
from app.graph.state import AgentState

graph = StateGraph(AgentState)

graph.add_node("generate_queries", generate_queries_node)
graph.add_node("search", search_node)
graph.add_node("filter_relevance", filter_relevance_node)
graph.add_node("extract_skills", extract_skills_node)
graph.add_node("aggregate_skills", aggregate_skills_node)
graph.add_node("generate_report", generate_report_node)

graph.set_entry_point("generate_queries")

graph.add_edge("generate_queries", "search")
graph.add_edge("search", "filter_relevance")
graph.add_edge("filter_relevance", "extract_skills")
graph.add_edge("extract_skills", "aggregate_skills")
graph.add_edge("aggregate_skills", "generate_report")
graph.add_edge("generate_report", END)

app_graph = graph.compile()
