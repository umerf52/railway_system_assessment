import networkx as nx
from fastapi import FastAPI, Request

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


@app.post("/check_conflicts")
async def check_conflicts(request: Request):
    data = await request.json()
    station_graph = data["station_graph"]
    routes = data["routes"]
    check_route = data["check_route"]

    graph = _generate_graph(station_graph)

    graph = _remove_occupied_sections(graph, routes)

    return {"success": _check_if_path_exists(graph, check_route)}
