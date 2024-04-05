#!/usr/bin/env python3

import itertools
import googlemaps

def calculate_distance_matrix(client_key, addresses):
    gmaps = googlemaps.Client(key=client_key)
    return gmaps.distance_matrix(addresses, addresses, mode="driving")

def find_optimal_route(distance_matrix):
    N = len(distance_matrix['destination_addresses'])
    permutations = list(itertools.permutations(range(1, N)))  # Skipping the first address which is the depot

    shortest_distance = None
    best_route = None

    for permutation in permutations:
        route = [0] + list(permutation)
        route_distance = 0

        for i in range(len(route)-1):
            origin_idx = route[i]
            destination_idx = route[i+1]
            route_distance += distance_matrix['rows'][origin_idx]['elements'][destination_idx]['distance']['value']

        if shortest_distance is None or route_distance < shortest_distance:
            shortest_distance = route_distance
            best_route = [distance_matrix['destination_addresses'][i] for i in route]

    return best_route, shortest_distance

# Example usage:
def main():
    API_KEY = 'Your Google Maps API Key Here'
    # A list of delivery addresses with the first being the depot or starting point
    addresses = [
        'Starting Location Address',
        'Delivery Location Address 1',
        'Delivery Location Address 2',
        'Delivery Location Address 3',
        # add more addresses as needed
    ]

    distance_matrix = calculate_distance_matrix(API_KEY, addresses)
    best_route, distance = find_optimal_route(distance_matrix)
    
    print("Optimal Route: ", best_route)
    print("Total Distance (in meters): ", distance)

if __name__ == "__main__":
    main()
