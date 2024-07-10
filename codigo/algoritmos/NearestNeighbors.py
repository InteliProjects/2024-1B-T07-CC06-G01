# Execute o comando 'pip install -r ./requirements.txt ' no terminal para baixar localmente as dependências necessárias

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
import json
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
    Calcula o comprimento total de um caminho usando KD-Tree.

    Args:
        solution (list): Lista de índices representando o caminho de solução.
        locations (list): Lista de coordenadas dos locais.

    Returns:
        float: Comprimento total do caminho.
    """
    total = 0
    for i in range(len(solution) - 1):
        total += length(locations[solution[i]], locations[solution[i + 1]])
    total += length(locations[solution[-1]], locations[solution[0]])  # Adiciona a distância do último para o primeiro para completar o tour
    return total

def nearest_neighbor_kdtree(locations):
    """
    Encontra o caminho do vizinho mais próximo usando KD-Tree.

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

    path.append(0)  # Para completar o tour retornando ao início
    return path

def create_data_model(locations, coordinates):
    """
    Cria o modelo de dados para o problema de roteamento.

    Args:
        locations (list): Lista de locais com coordenadas em metros.
        coordinates (list): Lista de coordenadas como tuplas.

    Returns:
        dict: Dicionário do modelo de dados para o problema de roteamento.
    """
    data = {}
    data["locations"] = locations
    data["coordinates"] = coordinates
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

def print_solution(solution, total_distance, coordinates):
    """
    Imprime os detalhes da solução.

    Args:
        solution (list): Lista de índices representando o caminho de solução.
        total_distance (float): Distância total do caminho.
        coordinates (list): Lista de coordenadas como tuplas.
    """
    print(f"Valor da Função Objetivo: {total_distance}")
    plan_output = "Rota:\n"
    for index in solution:
        plan_output += f" {index} ->"
    plan_output += f" {solution[0]}\n"
    print(plan_output)
    print(f"Distância Total: {total_distance}m\n")

def return_solution(solution, total_distance, coordinates):
    """
    Prepara os detalhes da solução para retorno como JSON.

    Args:
        solution (list): Lista de índices representando o caminho de solução.
        total_distance (float): Distância total do caminho.
        coordinates (list): Lista de coordenadas como tuplas.

    Returns:
        dict: Dicionário contendo os detalhes da solução.
    """
    response = {}
    response['objective_value'] = total_distance
    response['route'] = solution
    # Calcula o tempo para percorrer a rota: distância / velocidade em metros por minuto + tempo de parada em cada ponto
    response['time_taken'] = (total_distance / 83.33) + (len(solution) * 2)
    response['coordinates'] = coordinates
    response['exceeds_time'] = response['time_taken'] > 360  # 6 horas em minutos
    return response

# Função para converter tipos NumPy para serialização JSON
def convert_numpy_types(obj):
    """
    Converte tipos NumPy para tipos nativos Python para serialização JSON.

    Args:
        obj: Objeto a ser convertido.

    Returns:
        Object: Objeto convertido com tipos nativos Python.
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    else:
        return obj

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
    # Inicializa a coluna 'NUM_ROTA' no DataFrame
    clustered_data['NUM_ROTA'] = -1  # Inicializado com -1 para pontos não processados

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
                nearest_neighbor_path = nearest_neighbor_kdtree(locations)
                total_path_length = total_length_kdtree(nearest_neighbor_path, locations)
                response = return_solution(nearest_neighbor_path, total_path_length, coordinates)
                for i in range(len(response['route']) - 1):
                    clustered_data.loc[index[i], 'NUM_ROTA'] = i
                response_list.append(response)

        best_response_list = response_list
    else:
        # Quando o argumento não é fornecido, é usado um grid search para encontrar o melhor valor
        grid_clusters = range(30, 60) # Grid de clusters para busca de 30 a 60
        grid_clusters = [x * 22 for x in grid_clusters]

        best_total_distance = float('inf')
        best_n_clusters = 0
        best_response_list = []

        for n_clusters in grid_clusters:
            print(f"Processando {n_clusters} clusters...")
            response_list = []
            clustered_data['NUM_ROTA'] = -1  # Reinicializa para pontos não processados

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
                    nearest_neighbor_path = nearest_neighbor_kdtree(locations)
                    total_path_length = total_length_kdtree(nearest_neighbor_path, locations)
                    response = return_solution(nearest_neighbor_path, total_path_length, coordinates)
                    for i in range(len(response['route']) - 1):
                        clustered_data.loc[index[i], 'NUM_ROTA'] = i
                    response_list.append(response)

            total_distance = sum([response['objective_value'] for response in response_list])
            exceeds_time = any([response['exceeds_time'] for response in response_list])
        
            if total_distance < best_total_distance and not exceeds_time:
                best_total_distance = total_distance
                best_response_list = response_list
                best_n_clusters = n_clusters
            
        print(f"Melhor número de clusters: {best_n_clusters}")

    # Salvando os resultados em json
    result_json['response'] = best_response_list

    with open('./outputs/JSON/NN_output.json', 'w') as f:
        json.dump(result_json, f, default=convert_numpy_types)

    # Opcionalmente salva os resultados em CSV
    clustered_data.to_csv('./outputs/CSV/NN_output.csv', sep=';', index=False)

    print("Processo finalizado.")
