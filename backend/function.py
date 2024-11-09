from backend.Data import gtfs_data
from numpy import inf

def calculate_distance(coord1, coord2):
    """Calculate the Euclidean distance between two coordinates."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return abs(lat1 - lat2) + abs(lon1 - lon2)


def find_closest_distance(initial_coords, bus_stops):
    """Given a set of bus stop coordinates, find the closest one to the initial coordinates."""
    min_distance = inf
    closest_stop = None
    stops_data = gtfs_data["stops.txt"]

    for stop_coords in bus_stops:
        # Find the stop with matching coordinates in the DataFrame
        stop_data = stops_data[(stops_data['stop_lat'] == stop_coords[0]) & (stops_data['stop_lon'] == stop_coords[1])]

        if not stop_data.empty:
            # Calculate the distance
            distance = calculate_distance(initial_coords, stop_coords)
            if distance < min_distance:
                min_distance = distance
                closest_stop = stop_data.iloc[0]

    return closest_stop if closest_stop is not None else "No close stop found"
