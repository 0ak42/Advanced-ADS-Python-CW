# oskar kane
# Jeet Nadiapara
import sys
import heapq

# Point this to the location of your CLRS library folder
sys.path.append(r"C:\Users\nadiy\OneDrive\Documents\GitHub\Advanced-ADS-Python-CW\task2\Libraries")

from adjacency_list_graph import AdjacencyListGraph

# Fix the dijkstra import - try different import methods
try:
    from dijkstra import dijkstra  # If dijkstra is a function in dijkstra.py
except ImportError:
    try:
        from dijkstra import dijkstra as dijkstra_func  # If it's named differently
    except ImportError:
        # If imports fail, use our own implementation
        def dijkstra_func(graph, source_idx):
            return custom_dijkstra(graph, source_idx)


def custom_dijkstra(graph, source_idx):
    """
    Custom Dijkstra implementation that works with AdjacencyListGraph
    """
    n = graph.get_card_V()
    dist = [float('inf')] * n
    parent = [None] * n
    visited = [False] * n

    dist[source_idx] = 0
    parent[source_idx] = source_idx

    for _ in range(n):
        # Find unvisited vertex with minimum distance
        min_dist = float('inf')
        u = None
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        if u is None:
            break

        visited[u] = True

        # Check all neighbors of u
        for edge in graph.get_adj_list(u):
            v = edge.get_v()
            weight = edge.get_weight()

            if not visited[v]:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u

    return dist, parent


class ModifiedAdjacencyListGraph(AdjacencyListGraph):
    """Modified version that allows updating edge weights"""

    def insert_or_update_edge(self, u, v, w):
        """Insert edge or update weight if edge exists"""
        try:
            self.insert_edge(u, v, w)
        except RuntimeError:
            # Edge exists, find and update it
            for node in self.adj[u]:
                if node.get_data() == v:
                    node.set_data(v, w)  # Update weight
                    break
            # Also update the reverse for undirected graph
            for node in self.adj[v]:
                if node.get_data() == u:
                    node.set_data(u, w)
                    break


def parse_tube_data(csv_data):
    """Parse CSV data and handle duplicate edges by keeping minimum weight"""
    edges_dict = {}
    stations = set()

    lines = csv_data.strip().split('\n')

    # Collect all stations
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 3:
            line_name, station1, station2 = parts[0], parts[1], parts[2]
            if station1: stations.add(station1)
            if station2: stations.add(station2)

    # Process edges, keeping minimum weight for duplicates
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) == 4 and parts[3]:
            line_name, station1, station2, weight = parts
            if station1 and station2 and weight:
                edge_key = tuple(sorted([station1, station2]))
                current_weight = int(weight)

                if edge_key not in edges_dict or current_weight < edges_dict[edge_key]:
                    edges_dict[edge_key] = current_weight

    # Convert to edges list
    edges = []
    for (station1, station2), weight in edges_dict.items():
        edges.append((station1, station2, weight))

    return list(stations), edges


# Your CSV data
csv_data = """LineOne,LineOne_One,,
LineOne,LineOne_Two,,
LineOne,LineOne_Three,,
LineOne,LineOne_Four,,
LineOne,LineOne_Five,,
LineOne,LineOne_One,LineOne_Two,4
LineOne,LineOne_Two,LineOne_Three,2
LineOne,LineOne_Three,LineOne_Four,3
LineOne,LineOne_Four,LineOne_Five,6
LineTwo,LineTwo_One,,
LineTwo,LineOne_Two,,
LineTwo,LineTwo_Three,,
LineTwo,LineOne_Four,,
LineTwo,LineTwo_Five,,
LineTwo,LineTwo_One,LineOne_Two,4
LineTwo,LineOne_Two,LineTwo_Three,3
LineTwo,LineTwo_Three,LineOne_Four,2
LineTwo,LineOne_Four,LineTwo_Five,5
LineThree,LineTwo_One,,
LineThree,LineThree_Two,,
LineThree,LineOne_Three,,
LineThree,LineOne_Four,,
LineThree,LineThree_Five,,
LineThree,LineTwo_One,LineThree_Two,5
LineThree,LineThree_Two,LineOne_Three,2
LineThree,LineOne_Three,LineOne_Four,2
LineThree,LineOne_Four,LineThree_Five,3"""

# Parse data
stations, edges = parse_tube_data(csv_data)
vertex_to_index = {station: idx for idx, station in enumerate(sorted(stations))}
index_to_vertex = {idx: station for station, idx in vertex_to_index.items()}

print("=== Tube Network ===")
print(f"Stations: {len(stations)}")
print("Station mapping:")
for station, idx in vertex_to_index.items():
    print(f"  {idx}: {station}")

print(f"\nConnections: {len(edges)}")
for u, v, w in edges:
    print(f"  {u} ↔ {v} ({w} min)")

# Build graph with modified class
G = ModifiedAdjacencyListGraph(len(stations), weighted=True)

for u, v, w in edges:
    u_idx = vertex_to_index[u]
    v_idx = vertex_to_index[v]
    G.insert_or_update_edge(u_idx, v_idx, w)

print("\n=== Journey Planning ===")


def get_path(parent, target_idx, index_to_vertex):
    """Reconstruct path from parent array"""
    if parent[target_idx] is None:
        return []

    path = []
    current_idx = target_idx

    while current_idx is not None:
        path.insert(0, index_to_vertex[current_idx])
        if parent[current_idx] == current_idx:  # Reached source
            break
        current_idx = parent[current_idx]

    return path


# Test routes
routes = [
    ('LineOne_One', 'LineOne_Five'),
    ('LineTwo_One', 'LineThree_Five'),
    ('LineOne_One', 'LineTwo_Five'),
    ('LineTwo_One', 'LineOne_Five')
]

# Try to use the library dijkstra, fall back to custom implementation
try:
    # Test if we can call dijkstra
    if 'dijkstra_func' in locals():
        dijkstra_algorithm = dijkstra_func
    else:
        dijkstra_algorithm = dijkstra
    print("Using library Dijkstra implementation")
except:
    dijkstra_algorithm = custom_dijkstra
    print("Using custom Dijkstra implementation")

for source, target in routes:
    if source in vertex_to_index and target in vertex_to_index:
        source_idx = vertex_to_index[source]
        target_idx = vertex_to_index[target]

        print(f"\nRoute: {source} → {target}")

        try:
            dist, parent = dijkstra_algorithm(G, source_idx)

            if dist[target_idx] != float('inf'):
                path = get_path(parent, target_idx, index_to_vertex)
                print(f"✓ Path: {' → '.join(path)}")
                print(f"  Total time: {dist[target_idx]} minutes")

                # Show detailed journey
                print("  Detailed journey:")
                current = target_idx
                journey_steps = []
                while current != source_idx:
                    prev = parent[current]
                    time_segment = dist[current] - dist[prev]
                    journey_steps.insert(0,
                                         f"    {index_to_vertex[prev]} → {index_to_vertex[current]} ({time_segment} min)")
                    current = prev
                for step in journey_steps:
                    print(step)
            else:
                print(f"✗ No path exists")

        except Exception as e:
            print(f"✗ Error finding path: {e}")
            # Fall back to custom implementation
            print("  Trying custom implementation...")
            try:
                dist, parent = custom_dijkstra(G, source_idx)
                if dist[target_idx] != float('inf'):
                    path = get_path(parent, target_idx, index_to_vertex)
                    print(f"✓ Path: {' → '.join(path)}")
                    print(f"  Total time: {dist[target_idx]} minutes")
                else:
                    print(f"✗ No path exists")
            except Exception as e2:
                print(f"✗ Custom implementation also failed: {e2}")
    else:
        missing = [s for s in [source, target] if s not in vertex_to_index]
        print(f"\n✗ Stations not found: {', '.join(missing)}")

# Show network summary
print(f"\n=== Network Summary ===")
print(f"Total stations: {len(stations)}")
print(f"Total connections: {len(edges)}")
print("\nAll stations:")
for i, station in enumerate(sorted(stations)):
    print(f"  {i:2d}. {station}")