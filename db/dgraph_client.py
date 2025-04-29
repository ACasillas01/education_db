import os
import pydgraph

DGRAPH_URI = os.getenv("DGRAPH_URI", "localhost:9080")

def create_dgraph_client():
    stub = pydgraph.DgraphClientStub(DGRAPH_URI)
    return pydgraph.DgraphClient(stub), stub
