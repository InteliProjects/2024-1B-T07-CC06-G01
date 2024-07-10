# Importa as bibliotecas padrões para se realizar a testagem
import unittest
import numpy as np
from scipy.spatial import KDTree
import math


# Função com o cálculo da distância entre os pontos
def length(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))


# Função que retorna o total da distância percorrida na solução
def total_length_kdtree(solution, locations):
    total = 0
    for i in range(len(solution) - 1):
        total += length(locations[solution[i]], locations[solution[i + 1]])
    total += length(locations[solution[-1]], locations[solution[0]])
    return total


# Calcula o vizinho mais próximo disponivel
def nearest_neighbor_kdtree(locations):
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


# calcula a matriz das distâncias euclidianas entre os pontos
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


# Cria um modelo para ser utilizado como teste
def create_data_model(locations, coordinates):
    data = {}
    data["locations"] = locations
    data["coordinates"] = coordinates
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


# faz a testagem do algoritmo com valores de teste e verifica se está correto
class TestAlgorithm1(unittest.TestCase):

    def test_length(self):
        self.assertEqual(length([0, 0], [3, 4]), 5.0)
        self.assertEqual(length([1, 1], [4, 5]), 5.0)
        self.assertEqual(length([2, 3], [2, 3]), 0.0)

    def test_total_length_kdtree(self):
        locations = [(0, 0), (3, 4), (6, 8)]
        solution = [0, 1, 2, 0]
        self.assertAlmostEqual(total_length_kdtree(solution, locations), 20.0)

    def test_nearest_neighbor_kdtree(self):
        locations = [(0, 0), (3, 4), (6, 8)]
        expected_path = [0, 1, 2, 0]
        self.assertEqual(nearest_neighbor_kdtree(locations), expected_path)

    def test_compute_euclidean_distance_matrix(self):
        locations = [(0, 0), (3, 4)]
        expected_matrix = {
            0: {0: 0, 1: 5},
            1: {0: 5, 1: 0}
        }
        self.assertEqual(compute_euclidean_distance_matrix(locations), expected_matrix)

    def test_create_data_model(self):
        locations = [(0, 0), (3, 4)]
        coordinates = [(10.0, 20.0), (30.0, 40.0)]
        data = create_data_model(locations, coordinates)
        self.assertEqual(data['locations'], locations)
        self.assertEqual(data['coordinates'], coordinates)
        self.assertEqual(data['num_vehicles'], 1)
        self.assertEqual(data['depot'], 0)


if __name__ == '__main__':
    unittest.main()
