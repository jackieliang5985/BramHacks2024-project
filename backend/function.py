from backend.Data import gtfs_data
from numpy import inf
from test import result

# Assuming 'unique_wards' contains a list of ward IDs
unique_wards = result['census_tract_id'].drop_duplicates()
unique_wards = [float(unique) for unique in unique_wards]
def find_wards(all_wards, emergency_wards, offset):
    result = []
    for element in all_wards:
        # Check if element is not in emergency_wards and the absolute difference is less than or equal to the offset
        if element not in emergency_wards and any(abs(element - m) <= offset for m in emergency_wards):
            result.append(element)
    return result

def calculate_distance(coord1, coord2):
    """Calculate the Euclidean distance between two coordinates."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return abs(lat1 - lat2) + abs(lon1 - lon2)


def find_closest_distance(initial_coords, emergency_wards, all_wards, offset):
    """Find the closest bus stop to the initial coordinates that is near an emergency ward."""
    # Step 1: Find wards that are close to the emergency wards
    safe_zone_bus_stops = find_wards(all_wards, emergency_wards, offset)

    min_distance = inf
    closest_stop = None

    # Step 2: Extract bus stop data from 'stops.txt' (assuming it's in the format of latitude and longitude)
    stops_data = gtfs_data["stops.txt"]  # Assuming 'stops.txt' is the key in gtfs_data

    # Step 3: Loop through safe zone bus stops to find the closest one
    for spot in safe_zone_bus_stops:
        # Get latitude and longitude for the bus stop corresponding to the ward
        stop_data = [result['stop_id'] == spot]  # Assuming 'ward' corresponds to 'stop_id'

        if not stop_data == []:
            stop_coords = (result['stop_lat'].values[0], result['stop_lon'].values[0])

            # Calculate distance from initial coordinates to bus stop coordinates
            distance = calculate_distance(initial_coords, stop_coords)

            # Update minimum distance and closest stop
            if distance < min_distance:
                min_distance = distance
                closest_stop = result['stop_id'].values[0]

    return closest_stop
# Example of usage
emergency_wards = [5350576.69]  # Replace this with actual emergency ward IDs
k = find_closest_distance((43.765355,-79.724787), emergency_wards, unique_wards, 0.05)

print(k)
