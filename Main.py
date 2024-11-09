import os
import pandas as pd
import requests

# Loading GTS files

def load_gtfs_data(folder_path):
    # Load each relevant file into a DataFrame
    gtfs_files = {}
    files = ["stops.txt", "routes.txt", "trips.txt", "stop_times.txt"]

    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.exists(file_path):
            gtfs_files[file] = pd.read_csv(file_path)

    return gtfs_files


gtfs_folder_path = "Google_Transit.zip"
gtfs_data = load_gtfs_data(gtfs_folder_path)

# Display loaded schedule data
print("Stops Data:\n", gtfs_data["stops.txt"].head())
print("Routes Data:\n", gtfs_data["routes.txt"].head())
print("Trips Data:\n", gtfs_data["trips.txt"].head())
print("Stop Times Data:\n", gtfs_data["stop_times.txt"].head())


def fetch_realtime_data(endpoint):
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None

trip_updates_url = "https://nextride.brampton.ca:81/API/TripUpdates?format=json"
vehicle_positions_url = "https://nextride.brampton.ca:81/API/VehiclePositions?format=json"
service_alerts_url = "https://nextride.brampton.ca:81/API/ServiceAlerts?format=json"
trip_updates = fetch_realtime_data(trip_updates_url)
vehicle_positions = fetch_realtime_data(vehicle_positions_url)
service_alerts = fetch_realtime_data(service_alerts_url)


# Pharsing through Data, i need to see it.
if trip_updates: # trip_id = specific buss, route_id = tranist route, stop_id =a specific stop along the route
    # important for arrival and departure delays.
    print("\nTrip Updates:")
    for entity in trip_updates.get("entity", []):
        trip_update = entity.get("trip_update")
        if not trip_update:
            continue

        trip = trip_update.get("trip", {})
        trip_id = trip.get("trip_id", "No trip ID")
        route_id = trip.get("route_id", "No route ID")
        print(f"Trip ID: {trip_id}, Route ID: {route_id}")

        stop_time_updates = trip_update.get("stop_time_update")
        if stop_time_updates:
            for stop_time_update in stop_time_updates:
                stop_id = stop_time_update.get("stop_id", "No stop ID")

                arrival = stop_time_update.get("arrival") or {}
                arrival_delay = arrival.get("delay", "No arrival delay")

                departure = stop_time_update.get("departure") or {}
                departure_delay = departure.get("delay", "No departure delay")

                print(f"  Stop ID: {stop_id}, Arrival Delay: {arrival_delay}, Departure Delay: {departure_delay}")
        else:
            print("No stop_time_update available for this trip.")

# if vehicle_positions:
#     print("\nVehicle Positions:")
#     for entity in vehicle_positions.get("entity", []):
#         vehicle = entity.get("vehicle")
#         if vehicle:
#             vehicle_id = vehicle.get("vehicle", {}).get("id")
#             latitude = vehicle.get("position", {}).get("latitude")
#             longitude = vehicle.get("position", {}).get("longitude")
#             print(f"Vehicle ID: {vehicle_id}, Latitude: {latitude}, Longitude: {longitude}")


if service_alerts:
    print("\nService Alerts:")
    for entity in service_alerts.get("entity", []):
        alert = entity.get("alert")
        if alert:
            header_text = alert.get("header_text", {}).get("translation", [{}])[0].get("text", "No text")
            print(f"Alert: {header_text}")
