import json
import pandas as pd
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math

# Load data from CSV file
data = pd.read_csv('AMOTRA_MENOR.csv', sep=';')

# Create a copy of the DataFrame
processed_data = data.copy()

# Convert latitude and longitude coordinates to meters using NumPy
x = processed_data['LATITUDE'].values * 10000000 / 90  # 90 degrees == 10,000 km
k = np.cos(processed_data['LATITUDE'].values * np.pi / 180.0)
y = processed_data['LONGITUDE'].values * k * 10000000 / 90  # 90 degrees == 10,000 km

# Calculate minimum values
minx1 = np.min(x)
minx2 = np.min(y)

# Adjust values relative to the minimum found
x_metros = (x - minx1).astype(int)
y_metros = (y - minx2).astype(int)

# Add columns to the DataFrame
processed_data['x_metros'] = x_metros
processed_data['y_metros'] = y_metros

def length(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def create_data_model(locations, coordinates, num_vehicles):
    data = {}
    data["locations"] = locations
    data["coordinates"] = coordinates
    data["num_vehicles"] = num_vehicles
    data["depot"] = 0
    return data

def compute_euclidean_distance_matrix(locations):
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distances[from_counter][to_counter] = int(
                    math.hypot((from_node[0] - to_node[0]), (from_node[1] - to_node[1]))
                )
    return distances

def print_solution(manager, routing, solution):
    print(f"Objective Function Value: {solution.ObjectiveValue()}")
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} ->"
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        plan_output += f" {manager.IndexToNode(index)}\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        print(plan_output)

def return_solution(manager, routing, solution, coordinates):
    response = {}
    response['objective_value'] = solution.ObjectiveValue()
    response['routes'] = []
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        route.append(manager.IndexToNode(index))
        response['routes'].append({
            'route': route,
            'distance': route_distance,
            'coordinates': [coordinates[i] for i in route]
        })
    return response

def main(locations, coordinates, num_vehicles):
    data = create_data_model(locations, coordinates, num_vehicles)
    manager = pywrapcp.RoutingIndexManager(
        len(data["locations"]), data["num_vehicles"], data["depot"]
    )
    routing = pywrapcp.RoutingModel(manager)
    distance_matrix = compute_euclidean_distance_matrix(data["locations"])

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(manager, routing, solution)
        return return_solution(manager, routing, solution, coordinates)

if __name__ == "__main__":
    print("Starting VRP OR-Tools...")
    coordinates = list(zip(processed_data['LATITUDE'], processed_data['LONGITUDE']))
    locations = list(zip(processed_data['x_metros'], processed_data['y_metros']))
    num_vehicles = 10
    if locations:
        result = main(locations, coordinates, num_vehicles)
        with open('result_vrp.json', 'w') as f:
            json.dump(result, f)
    print("Process completed.")
