# Railway Interlocking Assessment

This is a simple FastAPI server to quickly demonstrate the required functionality.

## Explanation
- This problem can be looked at as a graph problem.
- By default, all nodes are bidirectional and reachable from each other.
- Occupied routes basically tell us which edges to be removed from the graph.
- Once the edges have been removed, we can check for conflicts by finding a path in the graph between the two nodes. If nodes are reachable, then there is no conflict. If nodes are not reachable, then there is a conflict.

## Solution
- Instead of reinventing the wheel, I used a library [networkx](https://github.com/networkx/networkx) specialized for working with graph problems.
- This allowed me to quickly prototype the solution since I don't have to worry about how to represent the nodes and edges of the graph in my code.
- Similarly, I used the library's built-in function to find a path between two nodes.
- I created a graph, removed occupied sections from the graph, and then checked for reachability.

## Running the server
- Install the dependencies using `pip install -r requirements.txt`
- Run the server using `uvicorn src.server:app --reload`

## Deployed version
- The server is deployed on Vercel and can be accessed at https://railway-system-assessment.vercel.app/

## Deployment
- I used Vercel to deploy the server since it allows free usage for hobby projects.
- I used this guide for deployment: https://abdadeel.medium.com/deploy-fastapi-app-on-vercel-serverless-b9fc35bba74d

## Technical decisions
- I used FastAPI since it is easy to understand, but can also be scaled to production. Other choices were Flask or Django but they are an overkill for a simple project like this.
- There might be other approaches to solve this problem, (like directly creating a graph with removed edges) but this approach made logical sense to me.
- Tests were skipped due to time constraints. Simple tests for successful responses, invalid parameters.
- Similarly, code can be refactored into separate files for endpoints, graph logic, examples, etc.
- It was also possible to implement the graph logic myself, but I decided to use a library since it is more robust and tested. Moreover, it allowed me to focus on the problem itself rather than the implementation details.
