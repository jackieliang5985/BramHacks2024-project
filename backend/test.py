import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
bus_stops_df = pd.read_csv('Google_Transit/stops.txt', sep=',')


geometry = [Point(xy) for xy in zip(bus_stops_df['stop_lon'], bus_stops_df['stop_lat'])]


bus_stops_gdf = gpd.GeoDataFrame(bus_stops_df, geometry=geometry)

census_tracts_gdf = gpd.read_file('Google_Transit/Census_tracts.geojson')
# Check CRS of both GeoDataFrames
print(bus_stops_gdf.crs)
print(census_tracts_gdf.crs)

bus_stops_gdf.set_crs(epsg=4326, inplace=True)
census_tracts_gdf.set_crs(epsg=4326, inplace=True)

bus_stops_gdf = bus_stops_gdf.to_crs(census_tracts_gdf.crs)

# Perform spatial join to associate bus stops with census tracts
bus_stops_with_tracts = gpd.sjoin(bus_stops_gdf, census_tracts_gdf, how='left')

# View the first few rows
print(bus_stops_with_tracts.head())

# Assuming 'CTUID' is the census tract ID field
# Adjust 'CTUID' to match the actual tract ID column name in your data
result = bus_stops_with_tracts[['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'CTUID']]

# Rename 'CTUID' to 'census_tract_id' for clarity
result = result.rename(columns={'CTUID': 'census_tract_id'})

result = result.dropna(subset=['census_tract_id'])

# Save the result to a new CSV file
result.to_csv('bus_stops_with_census_tracts.csv', index=False)
