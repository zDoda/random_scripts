#!/usr/bin/env python3

import pandas as pd
from itertools import permutations
from haversine import haversine, Unit

def load_delivery_locations(file_path):
    return pd.read_csv(file_path)

def calculate_distance(coord1, coord2):
    return haversine(coord1, coord2, unit=Unit.KILOMETERS)

def find_optimal_route(locations):
    min_route = None
    min_distance = float('inf')
    for perm in permutations(locations):
        current_distance = 0
        for i in range(len(perm) - 1):
            current_distance += calculate_distance(perm[i], perm[i + 1])
        if current_distance < min_distance:
            min_distance = current_distance
            min_route = perm
    return min_route, min_distance

def main():
    file_path = 'delivery_locations.csv' # path to a CSV file containing delivery locations
    delivery_data = load_delivery_locations(file_path)

    # Assume the CSV has 'latitude' and 'longitude' columns for each delivery location
    locations = [(row['latitude'], row['longitude']) for _, row in delivery_data.iterrows()]
    
    optimal_route, total_distance = find_optimal_route(locations)
    
    print('Optimal delivery route:')
    for location in optimal_route:
        print(location)
    print('Total distance for this route: {:.2f} km'.format(total_distance))

if __name__ == "__main__":
    main(