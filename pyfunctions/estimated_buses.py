import pandas as pd

POPULATION_DATA = pd.read_csv('backend/resources/populations_by_census_tract.csv')

def calculate_estimated_buses(tractID: float) -> int:
    """
    Return the estimated number of buses required to evacuate people residing
    in the given census tract.
    """
    population = get_population_by_tract(tractID)
    population = population // 2        # assume 50% of the population will take car
    buses = population // 93            # assume a bus can carry up to 93 people
    return buses


def get_population_by_tract(tractID: float) -> int:
    row = POPULATION_DATA[POPULATION_DATA['CENSUS TRACT NUMBER'] == tractID]
    return row['Population, 2021'].item()


def total_people_affected(tracts: list) -> int:
    total = 0
    for tractID in tracts:
        total += get_population_by_tract(tractID)
    return total

def total_buses(tracts: list) -> int:
    total = 0
    for tractID in tracts:
        total += calculate_estimated_buses(tractID)
    return total


# Example use case
print(calculate_estimated_buses(5350576.17))
print(total_people_affected([5350573.09, 5350576.29]))
print(total_buses([5350573.09, 5350576.29]))