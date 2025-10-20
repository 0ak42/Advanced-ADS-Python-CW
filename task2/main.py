import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

#Task 2
#Oskar Kane
#Jeet Nadiapara
#20/10/25
#from clrsPython.Chapter22.dijkstra import dijkstra
#Helpful tips/notes (remove at final)
#Chapter 20-22

#Basic structure#
#1-fetch data
#2-Data input for both stations
#3-Format data (if needed)
#4-Only look at data with 4 columns
#5-Dijkstras library import
#6-Format output (fetch from data maybe)



from utils.data_api import (
     init_index, is_operational, get_station_id, get_station_name, activate_station,
     deactivate_station, insert_station, is_station_active, delete_station_by_name, create_edge, get_edge_info,
    get_all_stations
)

# importing from the given libraries
from collections import defaultdict
import heapq

# importing from given API
from utils.data_api import (
    insert_station, create_edge, get_station_id, get_station_name,
    get_all_stations, activate_station, is_station_active
)

# --- Helpers to be robust to different create_edge signatures ---
def safe_get_station_id(name):
    """
    Try to get station ID via get_station_id; if not available or fails,
    fall back to returning the name (some implementations accept names).
    """
    try:
        return get_station_id(name)
    except Exception:
        return name

def safe_create_edge(a_name, b_name, weight):
    """
    Try to call create_edge with IDs first, otherwise with names.
    If your create_edge requires a different signature adapt here.
    """
    a_id = safe_get_station_id(a_name)
    b_id = safe_get_station_id(b_name)
    try:
        # try calling with ids/numeric ids (common signature: create_edge(u_id, v_id, weight))
        create_edge(a_id, b_id, weight)
    except TypeError:
        # try calling with names
        create_edge(a_name, b_name, weight)
    except Exception:
        # If create_edge exists but raises other exceptions (e.g., station not found),
        # re-raise to inform the user so they can correct environment.
        raise

# --- Build the small dataset: A, B, C, D, E ---
stations = ["A", "B", "C", "D", "E"]
for s in stations:
    try:
        insert_station(s)
    except Exception:
        # If station already exists or insert signature different, ignore/continue
        pass

# adjacency list we will use for Dijkstra (local copy)
adj = defaultdict(list)

# edges list (undirected)
edges = [
    ("A", "B", 2),
    ("A", "C", 5),
    ("B", "C", 1),
    ("B", "D", 2),
    ("C", "E", 5),
    ("D", "E", 3),
]

# add edges to API and to local adjacency
for u, v, w in edges:
    # attempt to create edge via API (wrapper tolerant to signature)
    try:
        safe_create_edge(u, v, w)
    except Exception as e:
        # If your library doesn't expose create_edge or you prefer not to call it,
        # we still proceed building local adjacency for the algorithm.
        print(f"Warning (create_edge failed or skipped for {u}-{v}): {e}")

    # add both directions for undirected route planner
    adj[u].append((v, w))
    adj[v].append((u, w))

# --- Dijkstra implementation ---
def dijkstra(start, goal, adjacency):
    # priority queue of (distance, node)
    pq = [(0, start)]
    dist = {start: 0}
    prev = {start: None}
    visited = set()

    while pq:
        d, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            break

        for neighbor, weight in adjacency.get(node, []):
            if neighbor in visited:
                continue
            nd = d + weight
            if neighbor not in dist or nd < dist[neighbor]:
                dist[neighbor] = nd
                prev[neighbor] = node
                heapq.heappush(pq, (nd, neighbor))

    # Reconstruct path
    if goal not in dist:
        return None, float('inf')  # no path
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return path, dist[goal]

# Run for A -> E
path, total = dijkstra("A", "E", adj)
print("Shortest path (A -> E):", path)
print("Total duration (minutes):", total)

# Verification vs manual
manual_expected_path = ["A", "B", "D", "E"]
manual_expected_total = 7
print("Manual expected path:", manual_expected_path, "total:", manual_expected_total)
if path == manual_expected_path and total == manual_expected_total:
    print("VERIFICATION: manual and code results MATCH ✅")
else:
    print("VERIFICATION: mismatch (see above).")