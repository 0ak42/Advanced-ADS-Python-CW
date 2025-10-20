#Task 2A
#Oskar Kane
#Jeet Nadiapara
#20/10/25-

#Helpful tips/notes (remove at final)
#Chapter 20-22

####Basic structure####
#1-fetch data and libraries needed
import sys
import os

from utils.data_api import (
    init_index, is_operational, get_station_id, get_station_name, create_edge, get_edge_info, get_all_stations
)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clrsPython.Chapter22.dijkstra import dijkstra

#2-Data input for both stations (currently fixed for testing
StartStation="LineTwo_One"
EndStation="LineThree_Five"

#3-Format data (not needed currently as fixed data)

#4-Only look at data with 4 columns
#If position 3 is empty go next

#5 create graph with csv data

#6-Dijkstra library import

#def dijkstra(G, s):
#Arguments:
#G -- a directed, weighted graph
#s -- index of source vertex
#Returns:
#d -- distances from source vertex s
#pi -- predecessors

#7-Format output (fetch from data maybe)

