import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

# Load bus stops data
bus_stops_df = pd.read_csv('../Google_Transit/stops.txt', sep=',')

# Create geometry for bus stops
geometry = [Point(xy) for xy in zip(bus_stops_df['stop_lon'], bus_stops_df['stop_lat'])]
bus_stops_gdf = gpd.GeoDataFrame(bus_stops_df, geometry=geometry)

# Load census tracts data
census_tracts_gdf = gpd.read_file('../Google_Transit/Census_tracts.geojson')

# Ensure both GeoDataFrames use the same Coordinate Reference System (CRS)
bus_stops_gdf.set_crs(epsg=4326, inplace=True)
census_tracts_gdf.set_crs(epsg=4326, inplace=True)
bus_stops_gdf = bus_stops_gdf.to_crs(census_tracts_gdf.crs)

# Perform spatial join to associate bus stops with census tracts
bus_stops_with_tracts = gpd.sjoin(bus_stops_gdf, census_tracts_gdf, how='left')

# Convert CTUID column to float to avoid TypeError during comparisons
bus_stops_with_tracts['CTUID'] = pd.to_numeric(bus_stops_with_tracts['CTUID'], errors='coerce')

# Create final DataFrame with bus stops and their census tract IDs
result = bus_stops_with_tracts[['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'CTUID']]
result = result.rename(columns={'CTUID': 'census_tract_id'}).dropna(subset=['census_tract_id'])

# Save to CSV
result.to_csv('bus_stops_with_census_tracts.csv', index=False)


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
    print(f"Stops inside danger tract {danger_tract_id}:")
    print(selected_stops[['stop_id', 'stop_name', 'stop_lat', 'stop_lon', tract_column]].to_string(index=False))

    return selected_stops[['stop_id', 'stop_name', 'stop_lat', 'stop_lon', tract_column]]

if __name__ == "__main__":
    danger_tract_id = 5350576.99
    num_stops = 25

    danger_stops = find_stops_in_danger_tract(danger_tract_id, result, tract_column='census_tract_id', num_stops=num_stops)
