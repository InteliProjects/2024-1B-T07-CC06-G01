# Execute o comando 'pip install -r ./requirements.txt ' no terminal para baixar localmente as dependências necessárias

import json
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
import argparse

def length(point1, point2):
    """
    Calcula a distância Euclidiana entre dois pontos.

    Args:
        point1 (tuple): Coordenadas do primeiro ponto.
        point2 (tuple): Coordenadas do segundo ponto.

    Returns:
        float: Distância Euclidiana entre os dois pontos.
    """
    return np.linalg.norm(np.array(point1) - np.array(point2))

def total_length_kdtree(solution, locations):
    """
    Calcula o comprimento total de um caminho de solução usando KDTree.

    Args:
        solution (list): Lista de índices representando o caminho de solução.
        locations (list): Lista de coordenadas dos locais.

    Returns:
        float: Comprimento total do caminho.
    """
    total = 0
    for i in range(len(solution) - 1):
        total += length(locations[solution[i]], locations[solution[i + 1]])
    total += length(locations[solution[-1]], locations[solution[0]])
    return total

def nearest_neighbor_kdtree(locations):
    """
    Gera um caminho do vizinho mais próximo usando KDTree.

    Args:
        locations (list): Lista de coordenadas dos locais.

    Returns:
        list: Caminho dos índices representando a rota do vizinho mais próximo.
    """
    tree = KDTree(locations)
    size = len(locations)
    path = [0]
    visited = [False] * size
    visited[0] = True
    current_index = 0

    for _ in range(size - 1):
        distances, indices = tree.query(locations[current_index], k=size)
        for idx in indices:
            if not visited[idx]:
                path.append(idx)
                visited[idx] = True
                current_index = idx
                break

    path.append(0)
    return path

def create_data_model(locations, coordinates):
    """
    Cria o modelo de dados para roteamento com ORTools.

    Args:
        locations (list): Lista de coordenadas dos locais.
        coordinates (list): Lista de coordenadas como tuplas.

    Returns:
        dict: Dicionário do modelo de dados para roteamento com ORTools.
    """
    data = {}
    data["locations"] = locations
    data["coordinates"] = coordinates
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

def compute_euclidean_distance_matrix(locations):
    """
    Computa a matriz de distância Euclidiana entre locais.

    Args:
        locations (list): Lista de coordenadas dos locais.

    Returns:
        dict: Matriz de distância onde as chaves são índices e os valores são dicionários
              com distâncias para outros nós.
    """
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
    """
    Imprime detalhes da solução obtida com ORTools.

    Args:
        manager: Gerenciador de índices de roteamento.
        routing: Modelo de roteamento.
        solution: Objeto de solução contendo a solução computada.
    """
    print(f"Valor da Função Objetivo: {solution.ObjectiveValue()}")
    index = routing.Start(0)
    plan_output = "Rota:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)
    plan_output += f"Distância Total: {route_distance}m\n"

def return_solution(manager, routing, solution, coordinates):
    """
    Prepara os detalhes da solução para retorno como JSON.

    Args:
        manager: Gerenciador de índices de roteamento.
        routing: Modelo de roteamento.
        solution: Objeto de solução contendo a solução computada.
        coordinates (list): Lista de coordenadas como tuplas.

    Returns:
        dict: Dicionário contendo os detalhes da solução.
    """
    response = {}
    response['objective_value'] = solution.ObjectiveValue()
    index = routing.Start(0)
    route_distance = 0
    route = []
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    route.append(manager.IndexToNode(index))
    response['route'] = route
    # Cálculo do tempo para percorrer a rota: distância / velocidade em metros por minuto + tempo de parada em cada ponto
    response['time_taken'] = (route_distance / 83.33) + (len(route) * 2)
    response['coordinates'] = coordinates
    return response

def main(locations, coordinates):
    """
    Função principal para resolver o problema de roteamento usando ORTools.

    Args:
        locations (list): Lista de locais com coordenadas em metros.
        coordinates (list): Lista de coordenadas como tuplas.

    Returns:
        dict: Detalhes da solução.
    """
    data = create_data_model(locations, coordinates)
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
    # Carrega os dados de um arquivo CSV
    data = pd.read_csv('../Atlanticos/Atlanticos.Server/bin/Debug/net8.0/CsvFiles/data.csv', sep=';')

    # Cria uma cópia do DataFrame
    clustered_data = data.copy()

    # Conversão das coordenadas de latitude e longitude para metros usando NumPy
    x = clustered_data['LATITUDE'].values * 10000000 / 90  # 90 graus == 10.000 km
    k = np.cos(clustered_data['LATITUDE'].values * np.pi / 180.0)
    y = clustered_data['LONGITUDE'].values * k * 10000000 / 90  # 90 graus == 10.000 km

    # Cálculo dos valores mínimos
    minx1 = np.min(x)
    minx2 = np.min(y)

    # Ajuste dos valores relativos ao mínimo encontrado
    x_metros = (x - minx1).astype(int)
    y_metros = (y - minx2).astype(int)

    # Adição de colunas ao DataFrame
    clustered_data['x_metros'] = x_metros
    clustered_data['y_metros'] = y_metros

    # Pegar dados de input
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_clusters', type=int, help='Número de clusters') # Número de clusters
    args = parser.parse_args()

    result_json = {}
    # Inicializa a coluna 'ROUTE_NUM' no DataFrame
    clustered_data['ROUTE_NUM'] = -1  # Inicializado com -1 para pontos não processados

    if args.n_clusters:
        print("Iniciando...")
        response_list = []
        # Defina o número de clusters
        n_clusters = args.n_clusters

        # Agrupamento dos dados usando KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(clustered_data[['x_metros', 'y_metros']])
        clustered_data['CLUSTER'] = kmeans.labels_

        for cluster in range(n_clusters):
            filter_data = clustered_data[clustered_data['CLUSTER'] == cluster]
            index = list(filter_data.index)
            coordinates = list(zip(filter_data['LATITUDE'], filter_data['LONGITUDE']))
            locations = list(zip(filter_data['x_metros'], filter_data['y_metros']))
            if locations:
                response = main(locations, coordinates)
                for i in range(len(response['route']) - 1):
                    clustered_data.loc[index[i], 'ROUTE_NUM'] = i
                response_list.append(response)

        best_response_list = response_list
    else:
        # Quando o argumento não é fornecido, é usado um grid search para encontrar o melhor valor
        grid_clusters = [30, 40, 50, 60]

        best_total_distance = float('inf')
        best_n_clusters = 0
        best_response_list = []

        for n_clusters in grid_clusters:
            print(f"Processando {n_clusters} clusters...")
            response_list = []
            clustered_data['ROUTE_NUM'] = -1  # Reinicializa para pontos não processados

            # Agrupamento dos dados usando KMeans
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(clustered_data[['x_metros', 'y_metros']])
            clustered_data['CLUSTER'] = kmeans.labels_

            for cluster in range(n_clusters):
                filter_data = clustered_data[clustered_data['CLUSTER'] == cluster]
                index = list(filter_data.index)
                coordinates = list(zip(filter_data['LATITUDE'], filter_data['LONGITUDE']))
                locations = list(zip(filter_data['x_metros'], filter_data['y_metros']))
                if locations:
                    response = main(locations, coordinates)
                    for i in range(len(response['route']) - 1):
                        clustered_data.loc[index[i], 'ROUTE_NUM'] = i
                    response_list.append(response)

            total_distance = sum([response['objective_value'] for response in response_list])
            if total_distance < best_total_distance:
                best_total_distance = total_distance
                best_response_list = response_list
                best_n_clusters = n_clusters
            
        print(f"Melhor número de clusters: {best_n_clusters}")

    # Salvando os resultados em json
    result_json['response'] = best_response_list

    with open('./outputs/JSON/ORtools_output.json', 'w') as f:
        json.dump(result_json, f)

    # Opcionalmente salva os resultados em CSV
    clustered_data.to_csv('./outputs/CSV/ORtools_output.csv', sep=';', index=False)

    print("Processo finalizado.")