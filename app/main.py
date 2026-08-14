from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.graph.build import app_graph
from app.schemas import ResearchRequest, ResearchResponse

app = FastAPI(title="Career Research Agent API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    initial_state = {
        "role": request.role,
        "n": request.n,
        "max_results": request.max_results,
        "threshold": request.threshold,
        "retry_count": 0,
        "queries": [],
        "search_results": [],
        "filtered_results": [],
        "skills": [],
        "aggregated_skills": [],
        "report": "",
    }

    result = app_graph.invoke(initial_state)

    return ResearchResponse(
        report=result["report"], aggregated_skills=result["aggregated_skills"]
    )
