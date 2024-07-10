# Import padrão das bibliotecas

import unittest
import numpy as np
from scipy.spatial import KDTree


# Função que calcula a distância euclidiana entre os pontos
def length(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))


# calcula a distância total percorrida na árvore
def total_length_kdtree(solution, locations):
    total = 0
    for i in range(len(solution) - 1):
        total += length(locations[solution[i]], locations[solution[i + 1]])
    total += length(locations[solution[-1]], locations[solution[0]])  # Completa o tour
    return total


# calcula o vizinho mais próximo, pensando no total de localidades
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

    path.append(0)  # Completa o tour retornando ao início
    return path


# cria os dados de teste para as próximas etapas
def create_data_model(locations, coordinates):
    data = {}
    data["locations"] = locations
    data["coordinates"] = coordinates
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


# calcula todas as informações para percorrer o caminho
def return_solution(solution, total_distance, coordinates):
    response = {}
    response['funcao_objetivo'] = total_distance
    response['rota'] = solution
    # Tempo para percorrer a rota: distância sobre velocidade metros por minutos + tempo de parada em cada ponto
    response['tempo_percorrido'] = (total_distance / 83.33) + (len(solution) * 2)
    response['coordinates'] = coordinates
    return response


# Teste Unitário
class TestAlgorithm2(unittest.TestCase):

    def test_length(self):
        self.assertAlmostEqual(length([0, 0], [3, 4]), 5.0)
        self.assertAlmostEqual(length([1, 1], [4, 5]), 5.0)
        self.assertAlmostEqual(length([2, 3], [2, 3]), 0.0)

    def test_total_length_kdtree(self):
        locations = [(0, 0), (3, 4), (6, 8)]
        solution = [0, 1, 2, 0]
        self.assertAlmostEqual(total_length_kdtree(solution, locations), 20.0)

    def test_nearest_neighbor_kdtree(self):
        locations = [(0, 0), (3, 4), (6, 8)]
        expected_path = [0, 1, 2, 0]
        self.assertEqual(nearest_neighbor_kdtree(locations), expected_path)

    def test_create_data_model(self):
        locations = [(0, 0), (3, 4)]
        coordinates = [(10.0, 20.0), (30.0, 40.0)]
        data = create_data_model(locations, coordinates)
        self.assertEqual(data['locations'], locations)
        self.assertEqual(data['coordinates'], coordinates)
        self.assertEqual(data['num_vehicles'], 1)
        self.assertEqual(data['depot'], 0)

    def test_return_solution(self):
        solution = [0, 1, 2, 0]
        total_distance = 20.0
        coordinates = [(10.0, 20.0), (30.0, 40.0), (50.0, 60.0)]
        response = return_solution(solution, total_distance, coordinates)
        self.assertEqual(response['funcao_objetivo'], total_distance)
        self.assertEqual(response['rota'], solution)
        self.assertAlmostEqual(response['tempo_percorrido'], (total_distance / 83.33) + (len(solution) * 2))
        self.assertEqual(response['coordinates'], coordinates)


if __name__ == '__main__':
    unittest.main()
