import networkx as nx
from fastapi import Body, FastAPI, HTTPException

# from pydantic import Body

app = FastAPI()


# Create an undirected graph to represent the station topology
def _generate_graph(station_graph) -> nx.Graph:
    graph = nx.Graph()
    for edge in station_graph:
        graph.add_edge(edge["start"], edge["end"])
    return graph


# Remove occupied sections from the graph
def _remove_occupied_sections(graph, routes) -> nx.Graph:
    occupied_sections = set()

    for route in routes:
        if route["occupied"]:
            # Create a path between occupied nodes so it can be excluded from the graph
            # Using that path, get edges that should be removed from the graph
            path = nx.shortest_path(graph, source=route["start"], target=route["end"])
            for section in zip(path[:-1], path[1:]):
                occupied_sections.add(section)

    graph.remove_edges_from(occupied_sections)
    return graph


def _check_if_path_exists(graph, check_route) -> bool:
    return nx.has_path(graph, source=check_route["start"], target=check_route["end"])


example_parameters = {
    "station_graph": [
        {"start": "Station West", "end": "Entry Signal West"},
        {"start": "Entry Signal West", "end": "Point 1"},
        {"start": "Point 1", "end": "Exit Signal West 1"},
        {"start": "Point 1", "end": "Exit Signal West 2"},
        {"start": "Exit Signal West 1", "end": "Exit Signal East 1"},
        {"start": "Exit Signal West 2", "end": "Exit Signal East 2"},
        {"start": "Exit Signal East 1", "end": "Point 2"},
        {"start": "Exit Signal East 2", "end": "Point 2"},
        {"start": "Point 2", "end": "Entry Signal East"},
        {"start": "Entry Signal East", "end": "Station East"},
    ],
    "routes": [
        {"start": "Entry Signal West", "end": "Exit Signal East 1", "occupied": False},
        {"start": "Entry Signal West", "end": "Exit Signal East 2", "occupied": False},
        {"start": "Exit Signal East 1", "end": "Station East", "occupied": False},
        {"start": "Exit Signal East 2", "end": "Station East", "occupied": False},
        {"start": "Entry Signal East", "end": "Exit Signal West 1", "occupied": False},
        {"start": "Entry Signal East", "end": "Exit Signal West 2", "occupied": False},
        {"start": "Exit Signal West 1", "end": "Station West", "occupied": True},
        {"start": "Exit Signal West 2", "end": "Station West", "occupied": False},
    ],
    "check_route": {"start": "Entry Signal West", "end": "Exit Signal East 2"},
}


# Endpoints


@app.post(
    "/check_conflicts",
    responses={
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"success": True},
                },
            },
        },
    },
)
async def check_conflicts(data: dict = Body(..., example=example_parameters)):
    if (
        not data
        or "station_graph" not in data
        or "routes" not in data
        or "check_route" not in data
    ):
        raise HTTPException(status_code=404, detail="Invalid request body")
    station_graph = data["station_graph"]
    routes = data["routes"]
    check_route = data["check_route"]

    graph = _generate_graph(station_graph)

    graph = _remove_occupied_sections(graph, routes)

    return {"success": _check_if_path_exists(graph, check_route)}


@app.get("/")
async def root():
    return {
        "message": "Functionality is available at /check_conflicts",
        "documentation": "Check out documentation at /docs",
    }
