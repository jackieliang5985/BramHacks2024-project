from backend.Data import gtfs_data
from numpy import inf
from test import result
import math

import pandas as pd
from shapely.geometry import Point
import geopandas as gpd


def find_stops_in_danger_tract(danger_tract_id, bus_stops_data, tract_column='census_tract_id', num_stops = 5):
    """
    Finds a specified number of bus stops inside a given danger tract.

    Parameters:
        danger_tract_id (float): The tract ID of the danger area.
        bus_stops_data (DataFrame): DataFrame containing bus stops and associated tract IDs.
        tract_column (str): Name of the column in bus_stops_data that contains the tract ID.
        num_stops (int): The number of stops to return inside the danger tract.

    Returns:
        DataFrame: A DataFrame with the specified number of stops from the danger tract.
    """
    # Ensure the tract_column is converted to float
    bus_stops_data[tract_column] = pd.to_numeric(bus_stops_data[tract_column], errors='coerce')

    # Filter stops inside the danger tract
    stops_in_danger_tract = bus_stops_data[bus_stops_data[tract_column] == danger_tract_id]

    # If fewer stops are available than requested, return all stops in the tract
    selected_stops = stops_in_danger_tract if len(stops_in_danger_tract) <= num_stops else stops_in_danger_tract.sample(
        n=num_stops)

    # Print the selected stops and their details
    # print(f"Stops inside danger tract {danger_tract_id}:")
    # print(selected_stops[['stop_id']].to_string(index=False))
    # stopids = selected_stops['stop_lat', 'stop_lon'].tolist()
    lat = selected_stops['stop_lat'].tolist()
    lon = selected_stops['stop_lon'].tolist()

    coords = list(zip(lat, lon))
    # print(stopids)
    print(coords)

    return coords




def find_wards(all_wards, emergency_wards, offset):
    result = []
    for element in all_wards:
        # Check if element is not in emergency_wards and the absolute difference is less than or equal to the offset
        if element not in emergency_wards and any(abs(element - m) <= offset for m in emergency_wards):
            result.append(element)
    return result

def all_wards(bus_stops_data):
    return result['census_tract_id'].unique().tolist()
    

def calculate_distance(coord1, coord2):
    # Radius of Earth in kilometers
    R = 6371.0

    # Unpack latitude and longitude of both coordinates
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance


# def find_closest_distance(initial_coords, emergency_wards, all_wards, offset):
#     """Find the closest bus stop to the initial coordinates that is near an emergency ward."""
#     # Step 1: Find wards that are close to the emergency wards
#     safe_zone_bus_stops = find_wards(all_wards, emergency_wards, offset)

#     min_distance = inf
#     closest_stop = []

#     stops_data = gtfs_data["stops.txt"]  # Assuming 'stops.txt' is the key in gtfs_data

#     # Step 3: Loop through safe zone bus stops to find the closest one
#     for spot in safe_zone_bus_stops:
#         # Get latitude and longitude for the bus stop corresponding to the ward
#         stop_data = [result['stop_id'] == spot]  # Assuming 'ward' corresponds to 'stop_id'
#         if not stop_data == []:
#             stop_coords = (result['stop_lat'].values[0], result['stop_lon'].values[0])

#             # Calculate distance from initial coordinates to bus stop coordinates
#             for i in initial_coords:
#                 distance = calculate_distance(i, stop_coords)

#             # Update minimum distance and closest stop
#                 if distance < min_distance:
#                     min_distance = distance
#                     closest_stop.append(result['stop_id'].values[0])
#             min_distance = inf

#     return closest_stop

# def find_closest_distance(initial_coords, emergency_wards):

# Example of usage



emergency_wards = [5350576.69]  # Replace this with actual emergency ward IDs
allwards = all_wards(result)
major_stops = find_stops_in_danger_tract(5350576.69, result, "census_tract_id")
bus_stop_coords = [find_stops_in_danger_tract(safe, result, "census_tract_id", 1) for safe in emergency_wards]
close_wards = 
k = find_closest_distance(major_stops, emergency_wards, unique_wards, 0.05)


print(k)
