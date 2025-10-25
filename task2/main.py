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
"""
COMP1828 - Task 2(a)
Manual vs Code-Based Execution of a Shortest Path Algorithm
-----------------------------------------------------------
Implements Dijkstra's algorithm using the mandatory CLRS Python library (Chapter 22)
to find the shortest journey between two stations.

Dataset: Artificial example with 5 stations represented by integers (0–4)
Algorithm: Dijkstra’s Algorithm
Data Structure: Weighted adjacency list
"""

# === Step 1: Import from CLRS Library ===
# Assumes clrsPython is already extracted and accessible in sys.path.

from clrsPython.Chapter_22.dijkstra import dijkstra
from clrsPython.Utility_functions.adjacency_list_graph import AdjacencyListGraph


# === Step 2: Create a Simple Artificial Tube Network Dataset ===
# 0 --(4)-- 1 --(2)-- 2
#  |         |
# (1)       (3)
#  |         |
# 3 --(5)-- 4

edges = [
    (0, 1, 4),
    (0, 3, 1),
    (1, 2, 2),
    (1, 4, 3),
    (3, 4, 5)
]


# === Step 3: Build the Graph Using CLRS Data Structures ===
graph = AdjacencyListGraph(directed=False)
for u, v, w in edges:
    graph.add_edge(u, v, w)


# === Step 4: Run Dijkstra's Algorithm ===
source, destination = 0, 4
distance, predecessor = dijkstra(graph, source)


# === Step 5: Extract Shortest Path and Total Journey Time ===
def get_path(predecessor, target):
    """Reconstructs path from source to target using predecessor map."""
    path = []
    while target is not None:
        path.insert(0, target)
        target = predecessor.get(target)
    return path


shortest_path = get_path(predecessor, destination)
shortest_time = distance[destination]


# === Step 6: Output Results ===
print("=== Task 2(a): Dijkstra's Shortest Path (CLRS Implementation) ===")
print(f"Shortest path from station {source} to {destination}: {shortest_path}")
print(f"Total journey time: {shortest_time} minutes")


# === Notes for Coursework Report ===
# • Manually apply Dijkstra's algorithm to the same dataset.
# • Confirm that the manual path and time match the code results.
# • Example expected output:
#   Shortest path from station 0 to 4: [0, 1, 4]
#   Total journey time: 7 minutes
# • Explain any differences in your report.

if __name__ == "__main__":
    pass
