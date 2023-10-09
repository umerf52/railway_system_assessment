from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/check_conflicts")
async def check_conflicts(request: Request):
    data = await request.json()
    station_graph = data["station_graph"]
    routes = data["routes"]
    check_route = data["check_route"]
