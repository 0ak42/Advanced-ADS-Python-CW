"""Mainly to be used for testing APIs and the data structures introduced by task1"""

from data_extract import read_csv_file
from module_wrapper import build_index_from_rows
from utils.data_api import (
    init_index, is_operational, get_station_id, get_station_name, activate_station, 
    deactivate_station, insert_station, is_station_active, delete_station_by_name, create_edge, get_edge_info,
    get_all_stations
)
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

station_rows, edge_rows = read_csv_file()
hashtable, records_by_id = build_index_from_rows(station_rows, edge_rows)

print("--------------------------------\n")
print("Testing the data API:\n")
init_index()
stationName = "Victoria"
print(f"Is {stationName} operational: " + str(is_operational(stationName)))
sid = get_station_id("Oxford Circus")
print("Station name: " + str(get_station_name(sid)))
stationName = "HelloWorldStation"
print(f"Is {stationName} operational: " + str(is_operational(stationName)))

print("--------------------------------\n")
print("\nTesting the station active API:\n")
stationName = "Baker Street"
print(f"Is {stationName} active: {is_station_active(stationName)}")
deactivate_station(stationName)
print(f"Is {stationName} active: {is_station_active(stationName)}")
activate_station(stationName)
print(f"Is {stationName} active: {is_station_active(stationName)}")

print("--------------------------------\n")
print("\nTesting the station insert API:\n")
stationName = "HelloWorldStation"
print(f"Is {stationName} active: {is_station_active(stationName)}")
insert_station(stationName)
print(f"Is {stationName} active: {is_station_active(stationName)}")

print("--------------------------------\n")
print("\nTesting the edge create API:\n")

edge_a = "HelloWorldStation"
edge_b = "Oxford Circus"
edge_time = 3
edge_line = "TestLine"

# Ensure stations exist (HelloWorldStation inserted above; Oxford Circus exists in dataset)
created = create_edge(edge_a, edge_b, edge_time, line=edge_line, create_missing=True)
print(f"\nCreated edge between {edge_a} and {edge_b}: {created}")

ab = get_edge_info(edge_a, edge_b)
ba = get_edge_info(edge_b, edge_a)
print(f"Neighbor from {edge_a} to {edge_b}: [Line: {ab[1]}, Time: {ab[0]}]")
print(f"Neighbor from {edge_b} to {edge_a}: [Line: {ba[1]}, Time: {ba[0]}]")
# Basic checks
print("Edge time correct:", (ab and ab[0] == edge_time) and (ba and ba[0] == edge_time))
print("Edge line recorded:", (ab and ab[1] == edge_line) and (ba and ba[1] == edge_line))

print("--------------------------------\n")
print("\nTesting the station delete API:\n")
stationName = "HelloWorldStation"
print(f"Is {stationName} active: {is_station_active(stationName)}")
delete_station_by_name(stationName)
print(f"Is {stationName} active: {is_station_active(stationName)}")


print("--------------------------------\n")
print("\nRecords by id:\n")
StationsToAdd = ["A", "B", "C", "D", "E"]
for station in StationsToAdd:
    insert_station(station)

all_stations = dict(get_all_stations())
for sid, name in get_all_stations():
    print(str(sid) + " " + str(name))
print("--------------------------------")