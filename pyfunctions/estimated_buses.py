import pandas as pd

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
    population_data = pd.read_csv('backend/resources/populations_by_census_tract.csv')
    row = population_data[population_data['CENSUS TRACT NUMBER'] == tractID]
    return row['Population, 2021'].item()


# Example use case
print(calculate_estimated_buses(5350576.17))