import sys
# ✅ Point this to the location of your CLRS library folder
sys.path.append(r"C:\Users\nadiy\OneDrive\Documents\DSA Coursework\Libraries")

from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

# ---------- Simple Example Dataset ----------
# Each edge = (station1, station2, travel_time)
edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 5),
    ('B', 'D', 10),
    ('C', 'E', 3),
    ('E', 'D', 4)
]

# Build weighted graph
# We need to create the graph with the correct number of vertices
# First, let's get all unique vertices
vertices = set()
for u, v, w in edges:
    vertices.add(u)
    vertices.add(v)

# Create a mapping from vertex name to index
vertex_to_index = {vertex: idx for idx, vertex in enumerate(sorted(vertices))}
index_to_vertex = {idx: vertex for vertex, idx in vertex_to_index.items()}

# Create graph with the correct number of vertices
G = AdjacencyListGraph(len(vertices), weighted=True)

# Add edges to the graph
for u, v, w in edges:
    u_idx = vertex_to_index[u]
    v_idx = vertex_to_index[v]
    G.insert_edge(u_idx, v_idx, w)

# ---------- Dijkstra Shortest Path ----------
source = 'A'
target = 'D'

# Convert vertex names to indices for dijkstra
source_idx = vertex_to_index[source]
target_idx = vertex_to_index[target]

# Run dijkstra - it returns distances and predecessors as arrays of indices
dist, parent = dijkstra(G, source_idx)

# Print the shortest-time path and distance
def get_path(parent, target_idx, index_to_vertex):
    path = []
    current_idx = target_idx
    while current_idx is not None:
        path.insert(0, index_to_vertex[current_idx])
        # parent array uses -1 or similar for no parent, check the actual value
        if parent[current_idx] == current_idx:  # source node
            break
        current_idx = parent[current_idx]
    return path

path = get_path(parent, target_idx, index_to_vertex)
print("=== Task 2a: Journey Planner ===\n")
print(f"Shortest-time path from {source} to {target}: {' → '.join(path)}")
print(f"Total travel time: {dist[target_idx]} minutes")