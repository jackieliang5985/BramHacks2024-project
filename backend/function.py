
from numpy import inf
from test import result


import pandas as pd
from shapely.geometry import Point
import geopandas as gpd


def find_stops_in_danger_tract(danger_tract_id, bus_stops_data, tract_column='census_tract_id', num_stops=5):
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



# Assuming 'unique_wards' contains a list of ward IDs
unique_wards = result['census_tract_id'].drop_duplicates()
unique_wards = [float(unique) for unique in unique_wards]

# def find_wards(all_wards, emergency_wards, offset):
#     result = []
#     for element in all_wards:
#         # Check if element is not in emergency_wards and the absolute difference is less than or equal to the offset
#         if element not in emergency_wards and any(abs(element - m) <= offset for m in emergency_wards):
#             result.append(element)
#     return result


def find_nearby_safe_stops(danger_tract_id, bus_stops_data, tract_column='census_tract_id'):
    """
    Finds five random bus stops from surrounding tracts where the tract ID differs by ±0.1 from the given danger tract.

    Parameters:
        danger_tract_id (float): The tract ID of the danger area.
        bus_stops_data (DataFrame): DataFrame containing bus stops and associated tract IDs.
        tract_column (str): Name of the column in bus_stops_data that contains the tract ID.

    Returns:
        DataFrame: A DataFrame with five random stops from surrounding tracts.
    """
    # Ensure the tract_column is converted to float
    bus_stops_data[tract_column] = pd.to_numeric(bus_stops_data[tract_column], errors='coerce')

    # Calculate tract ID range
    min_tract_id = danger_tract_id - 0.1
    max_tract_id = danger_tract_id + 0.1

    # Filter stops in surrounding tracts
    surrounding_stops = bus_stops_data[
        (bus_stops_data[tract_column] != danger_tract_id) &
        (bus_stops_data[tract_column] >= min_tract_id) &
        (bus_stops_data[tract_column] <= max_tract_id)
        ]

    # Randomly select 5 stops if there are more than 5, otherwise return all
    if len(surrounding_stops) >= 5:
        safe_stops = surrounding_stops.sample(n=5)
    else:
        safe_stops = surrounding_stops

    # Print 5 random stops and their tract numbers
    print("Safe stops (not in danger tract):")
    print(safe_stops[['stop_id', 'stop_name', 'stop_lat', 'stop_lon', tract_column]].to_string(index=False))

    return safe_stops[['stop_id', 'stop_name', 'stop_lat', 'stop_lon', tract_column]]

print(find_nearby_safe_stops(5350576.69, result))
#
# def calculate_distance(coord1, coord2):
#     """Calculate the Euclidean distance between two coordinates."""
#     lat1, lon1 = coord1
#     lat2, lon2 = coord2
#     return abs(lat1 - lat2) + abs(lon1 - lon2)

#
# def find_closest_distance(initial_coords, emergency_wards, all_wards, offset):
#     """Find the closest bus stop to the initial coordinates that is near an emergency ward."""
#     # Step 1: Find wards that are close to the emergency wards
#     safe_zone_bus_stops = find_wards(all_wards, emergency_wards, offset)
#
#     min_distance = inf
#     closest_stop = []
#
#     # Step 3: Loop through safe zone bus stops to find the closest one
#     for ward in safe_zone_bus_stops:
#         # Get latitude and longitude for the bus stop corresponding to the ward
#         stop_data = get_stops(ward)  # Assuming 'ward' corresponds to 'stop_id'
#         stop_coords = (result['stop_lat'].values[0], result['stop_lon'].values[0])
#
#         # Calculate distance from initial coordinates to bus stop coordinates
#         for i in initial_coords:
#             distance = calculate_distance(i, stop_coords)
#
#         # Update minimum distance and closest stop
#             if distance < min_distance:
#                 min_distance = distance
#                 closest_stop.append(result['stop_id'].values[0])
#         min_distance = inf
#
#     return closest_stop
# Example of usage
# emergency_wards = [5350576.69]  # Replace this with actual emergency ward IDs
# k = find_closest_distance(find_stops_in_danger_tract(5350576.69, result, "census_tract_id"), emergency_wards, unique_wards, 0.05)
#
# print(k)
