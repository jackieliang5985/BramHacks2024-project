from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import math
from numpy import inf
from django.http import JsonResponse

# Load the bus stops data
bus_stops_data = pd.read_csv('backend/resources/bus_stops_with_census_tracts.csv')
population_data = pd.read_csv('backend/resources/populations_by_census_tract.csv')

@api_view(['GET'])
def find_stops_in_danger_tract_view(request):
    danger_tract_id = float(request.query_params.get('danger_tract_id'))
    num_stops = int(request.query_params.get('num_stops', 5))
    
    tract_column = 'census_tract_id'
    bus_stops_data[tract_column] = pd.to_numeric(bus_stops_data[tract_column], errors='coerce')
    stops_in_danger_tract = bus_stops_data[bus_stops_data[tract_column] == danger_tract_id]

    selected_stops = stops_in_danger_tract if len(stops_in_danger_tract) <= num_stops else stops_in_danger_tract.sample(n=num_stops)
    lat = selected_stops['stop_lat'].tolist()
    lon = selected_stops['stop_lon'].tolist()
    coords = list(zip(lat, lon))

    return Response({"coordinates": coords})


@api_view(['GET'])
def find_wards_view(request):
    all_wards = request.query_params.getlist('all_wards', type=float)
    emergency_wards = request.query_params.getlist('emergency_wards', type=float)
    offset = float(request.query_params.get('offset', 0.1))
    
    result = []
    for element in all_wards:
        if element not in emergency_wards and any(abs(element - m) <= offset for m in emergency_wards):
            result.append(element)
    return Response({"nearby_wards": result})


@api_view(['GET'])
def all_wards_view(request):
    wards = bus_stops_data['census_tract_id'].unique().tolist()
    return Response({"all_wards": wards})

@api_view(['GET'])
def estimated_buses_view(request, tractID):
    """
    API view to calculate the estimated number of buses needed for evacuation.
    """
    try:
        buses = calculate_estimated_buses(float(tractID))
        return JsonResponse({'tractID': tractID, 'estimated_buses': buses})
    except ValueError:
        return JsonResponse({'error': 'Invalid tractID'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_population_by_tract(tractID: float) -> int:
    """
    Get population of a specific census tract.
    """
    row = population_data[population_data['CENSUS TRACT NUMBER'] == tractID]
    return row['Population, 2021'].item()

def calculate_estimated_buses(tractID: float) -> int:
    """
    Calculate estimated number of buses required for evacuation.
    """
    population = get_population_by_tract(tractID)
    population = population // 2        # assume 50% of the population will take car
    buses = population // 93            # assume a bus can carry up to 93 people
    return buses
