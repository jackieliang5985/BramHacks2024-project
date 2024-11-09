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


# Path to your unzipped GTFS folder
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

trip_updates_url = "https://transitapi.brampton.ca/TripUpdates/TripUpdates.json"
vehicle_positions_url = "https://transitapi.brampton.ca/VehiclePositions/VehiclePositions.json"
service_alerts_url = "https://transitapi.brampton.ca/ServiceAlerts/ServiceAlerts.json"
trip_updates = fetch_realtime_data(trip_updates_url)
vehicle_positions = fetch_realtime_data(vehicle_positions_url)
service_alerts = fetch_realtime_data(service_alerts_url)


# Pharsing through Data, i need to see it.
if trip_updates:
    print("\nTrip Updates:")
    for entity in trip_updates.get("entity", []):
        trip_update = entity.get("trip_update")
        if trip_update:
            trip_id = trip_update["trip"].get("trip_id")
            print(f"Trip ID: {trip_id}")
            for stop_time_update in trip_update.get("stop_time_update", []):
                stop_id = stop_time_update.get("stop_id")
                arrival_time = stop_time_update.get("arrival", {}).get("time")
                departure_time = stop_time_update.get("departure", {}).get("time")
                print(f"  Stop ID: {stop_id}, Arrival Time: {arrival_time}, Departure Time: {departure_time}")


if vehicle_positions:
    print("\nVehicle Positions:")
    for entity in vehicle_positions.get("entity", []):
        vehicle = entity.get("vehicle")
        if vehicle:
            vehicle_id = vehicle.get("vehicle", {}).get("id")
            latitude = vehicle.get("position", {}).get("latitude")
            longitude = vehicle.get("position", {}).get("longitude")
            print(f"Vehicle ID: {vehicle_id}, Latitude: {latitude}, Longitude: {longitude}")


if service_alerts:
    print("\nService Alerts:")
    for entity in service_alerts.get("entity", []):
        alert = entity.get("alert")
        if alert:
            header_text = alert.get("header_text", {}).get("translation", [{}])[0].get("text", "No text")
            print(f"Alert: {header_text}")
