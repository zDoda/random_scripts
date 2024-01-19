#!/usr/bin/env python3

import numpy as np
from scipy.spatial.distance import pdist, squareform
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # Array of distances between locations (e.g., [ [0, 2, 9], [1, 0, 6], [2, 7, 0] ])
    # This should be replaced by actual distances or computed using a distance function
    data['distance_matrix'] = [
        #TODO: Add the real or computed distance matrix here
    ] 
    data['num_vehicles'] = 1 # Number of vehicles, can be adjusted
    data['depot'] = 0 # Index of the depot node
    return data

def create_distance_callback(data):
    """Creates callback to return distance between points."""
    distances = data['distance_matrix']
    def distance_callback(from_index, to_index):
        return distances[from_index][to_index]
    return distance_callback

def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    transit_callback_index = routing.RegisterTransitCallback(create_distance_callback(data))

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {}'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    route_distance = 0
    route = []
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    route.append(manager.IndexToNode(index))
    print('Route for vehicle 0:', route)
    print('Distance of the route:', route_distance, 'meters')

if __name__ == '__main__':
    main()
