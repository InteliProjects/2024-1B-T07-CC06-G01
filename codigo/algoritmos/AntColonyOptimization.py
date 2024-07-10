# Execute o comando 'pip install -r ./requirements.txt ' no terminal para baixar localmente as dependências necessárias

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from numpy.random import choice as np_choice
import json
import os
import argparse

class AntColony:
    """
    Classe que implementa a otimização de colônia de formigas para encontrar o caminho mais curto em um conjunto de pontos.

    Attributes:
        distances (numpy.ndarray): Matriz de distâncias entre os pontos.
        n_ants (int): Número de formigas na simulação.
        n_best (int): Número de melhores caminhos para atualizar o feromônio.
        n_iterations (int): Número de iterações da simulação.
        decay (float): Taxa de evaporação do feromônio.
        alpha (int): Peso do feromônio na escolha do caminho.
        beta (int): Peso da heurística do inverso da distância na escolha do caminho.
    """

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        """
        Inicializa a classe AntColony com os parâmetros especificados.
        """
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        """
        Executa o algoritmo de colônia de formigas para encontrar o caminho mais curto.
        Returns:
            tuple: Retorna o caminho mais curto encontrado e sua distância.
        """
        shortest_path = []
        all_time_shortest_path = (None, np.inf)
        for i in range(self.n_iterations):
            print(f"Iteration {i+1}/{self.n_iterations}")
            all_paths = self.gen_all_paths()
            path, dist = min(all_paths, key=lambda x: x[1])
            self.update_pheromone(all_paths, shortest_path)
            if dist < all_time_shortest_path[1]:
                all_time_shortest_path = (path, dist)
                shortest_path = path
            self.pheromone *= self.decay
            print(f"Current shortest path: {shortest_path}")
        return shortest_path, all_time_shortest_path[1]

    def update_pheromone(self, all_paths, shortest_path):
        """
        Atualiza a matriz de feromônio com base nos caminhos encontrados.
        """
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, _ in sorted_paths[:self.n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        """
        Calcula a distância total de um caminho.
        """
        total_dist = np.sum(self.distances[path])
        return total_dist

    def gen_all_paths(self):
        """
        Gera todos os caminhos possíveis que as formigas podem percorrer.
        """
        all_paths = []
        for _ in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        """
        Gera um único caminho iniciando de um ponto.
        """
        path = [start]
        visited = set([start])
        prev = start
        for _ in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append(move)
            visited.add(move)
            prev = move
        path.append(start)
        return path

    def pick_move(self, pheromone, dist, visited):
        """
        Escolhe o próximo movimento com base na distribuição de probabilidade calculada a partir do feromônio e da distância.
        """
        pheromone = np.copy(pheromone)
        dist = np.where(dist == 0, 1e-9, dist)
        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
        available_indices = [i for i in self.all_inds if i not in visited]
        if not available_indices:
            return np.random.choice(self.all_inds)
        row = row[available_indices]
        if np.any(np.isnan(row)) or np.any(np.isinf(row)) or np.sum(row) == 0:
            return np.random.choice(available_indices)
        norm_row = row / row.sum()
        move = np_choice(available_indices, 1, p=norm_row)[0]
        return move

def create_matrix(locations):
    """
    Cria uma matriz de distâncias a partir de coordenadas de locais.
    """
    distances = np.zeros((len(locations), len(locations)))
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            dist = np.linalg.norm(np.array(locations[i]) - np.array(locations[j]))
            distances[i, j] = distances[j, i] = dist
    return distances

def convert_numpy_types(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_clusters', type=int, help='Número de clusters')
    args = parser.parse_args()

    print("Starting...")
    result_json = {}
    response_list = []

    # Parâmetros fixos para o algoritmo de colônia de formigas
    n_ants = 10
    n_best = 5
    n_iterations = 100
    decay = 0.95

    # Carregando os dados
    data = pd.read_csv('../Atlanticos/Atlanticos.Server/bin/Debug/net8.0/CsvFiles/data.csv', sep=';')

    # Criando uma cópia do DataFrame
    clustered_data = data.copy()

    # Convertendo as coordenadas para metros
    x = clustered_data['LATITUDE'].values * 10000000 / 90  # 90 degrees == 10,000 km
    k = np.cos(clustered_data['LATITUDE'].values * np.pi / 180.0)
    y = clustered_data['LONGITUDE'].values * k * 10000000 / 90  # 90 degrees == 10,000 km

    # Calculando valores mínimos
    minx1 = np.min(x)
    minx2 = np.min(y)

    # Ajustando os valores baseado nos valores mínimos encontrados
    x_metros = (x - minx1).astype(int)
    y_metros = (y - minx2).astype(int)

    # Adicionando colunas de metros aos dados clusterizados
    clustered_data['x_metros'] = x_metros
    clustered_data['y_metros'] = y_metros

    # Pegar dados de input
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
            print(f"Processing cluster {cluster}")
            filter_data = clustered_data[clustered_data['CLUSTER'] == cluster]
            index = list(filter_data.index)
            coordinates = list(zip(filter_data['LATITUDE'], filter_data['LONGITUDE']))
            locations = list(zip(filter_data['x_metros'], filter_data['y_metros']))
            if len(locations) > 1:
                distances = create_matrix(locations)

                ant_colony = AntColony(distances, n_ants=n_ants, n_best=n_best, n_iterations=n_iterations, decay=decay)
                shortest_path, total_distance = ant_colony.run()

                route = []
                for idx, start in enumerate(shortest_path[:-1]):
                    end = shortest_path[idx + 1]
                    clustered_data.loc[index[start], 'ROUTE_NUM'] = idx
                    route.append({
                        "start": index[start],
                        "end": index[end]
                    })

                response_list.append({
                    "cluster": cluster,
                    "route": route,
                    "total_distance": total_distance
                })

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
                print(f"Processing cluster {cluster}")
                filter_data = clustered_data[clustered_data['CLUSTER'] == cluster]
                index = list(filter_data.index)
                coordinates = list(zip(filter_data['LATITUDE'], filter_data['LONGITUDE']))
                locations = list(zip(filter_data['x_metros'], filter_data['y_metros']))
                if len(locations) > 1:
                    distances = create_matrix(locations)

                    ant_colony = AntColony(distances, n_ants=n_ants, n_best=n_best, n_iterations=n_iterations, decay=decay)
                    shortest_path, total_distance = ant_colony.run()

                    route = []
                    for idx, start in enumerate(shortest_path[:-1]):
                        end = shortest_path[idx + 1]
                        clustered_data.loc[index[start], 'ROUTE_NUM'] = idx
                        route.append({
                            "start": index[start],
                            "end": index[end]
                        })

                    response_list.append({
                        "cluster": cluster,
                        "route": route,
                        "total_distance": total_distance
                    })

            total_distance = sum([response['total_distance'] for response in response_list])
            if total_distance < best_total_distance:
                best_total_distance = total_distance
                best_response_list = response_list
                best_n_clusters = n_clusters
            
        print(f"Melhor número de clusters: {best_n_clusters}")

    # Salvando os resultados em json
    result_json['response'] = best_response_list

    with open('./outputs/JSON/ACO_output.json', 'w') as f:
        json.dump(result_json, f, default=convert_numpy_types)

    # Opcionalmente salva os resultados em CSV
    clustered_data.to_csv('./outputs/CSV/ACO_output.csv', sep=';', index=False)

    print("Processo finalizado.")

