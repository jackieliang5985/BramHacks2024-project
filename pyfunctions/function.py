from numpy import inf
import math
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd


# Load the bus stops data once to avoid repeated loading in each function
bus_stops_data = pd.read_csv('backend/resources/bus_stops_with_census_tracts.csv')

def find_stops_in_danger_tract(danger_tract_id, num_stops=5):
    """
    Finds a specified number of bus stops inside a given danger tract.

    Parameters:
        danger_tract_id (float): The tract ID of the danger area.
        num_stops (int): The number of stops to return inside the danger tract.

    Returns:
        List of tuples: A list of coordinates (latitude, longitude) of bus stops in the danger tract.
    """
    tract_column = 'census_tract_id'
    
    # Ensure the tract_column is converted to float
    bus_stops_data[tract_column] = pd.to_numeric(bus_stops_data[tract_column], errors='coerce')

    # Filter stops inside the danger tract
    stops_in_danger_tract = bus_stops_data[bus_stops_data[tract_column] == danger_tract_id]

    # If fewer stops are available than requested, return all stops in the tract
    selected_stops = stops_in_danger_tract if len(stops_in_danger_tract) <= num_stops else stops_in_danger_tract.sample(
        n=num_stops)

    # Extract latitude and longitude
    lat = selected_stops['stop_lat'].tolist()
    lon = selected_stops['stop_lon'].tolist()

    coords = list(zip(lat, lon))
    return coords


def find_wards(all_wards, emergency_wards, offset):
    result = []
    for element in all_wards:
        # Check if element is not in emergency_wards and the absolute difference is less than or equal to the offset
        if element not in emergency_wards and any(abs(float(element) - m) <= offset for m in emergency_wards):
            result.append(element)
    return result


def all_wards():
    # Load unique census tract IDs from the preloaded bus_stops_data
    return bus_stops_data['census_tract_id'].unique().tolist()


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
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance


# Example of usage
emergency_wards = [5350576.69]  # Replace this with actual emergency ward IDs
allwards = all_wards()

# Find 5 random bus stops in the specified danger tract
major_stops = find_stops_in_danger_tract(5350576.69)

# Find wards near the emergency wards within the given offset
close_wards = find_wards(allwards, emergency_wards, 0.1)

# Find 1 random bus stop in each safe ward (close ward)
bus_stop_coords = [find_stops_in_danger_tract(float(safe), 1) for safe in close_wards]
print(bus_stop_coords)