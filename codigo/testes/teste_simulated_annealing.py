# ESSE CÓDIGO NÃO RESOLVE O PROBLEMA NA PRÁTICA, MAS TENTA
# O OBJETIVO É DE DESENVOLVER UMA ROTEIRIZAÇÃO PARA DIVERSOS LEITURISTAS
# FOI TESTADO, MAS OS RESULTADOS NÃO FORAM APURADOS
# POSSIVELMENTE AJUDA NO DESENVOLVIMENTO

# literalmente só um teste mesmo

# Traz as bibliotecas a serem utilizadas
import numpy as np
import random
import math
import csv


# Essa função faz uma leitura da amostragem,
# criando um dataframe com apenas 2 características:
# Longitude e Latitude
def cria_df(amostra):
    df = []
    with open(amostra, 'r', newline='') as file:
        arquivo = csv.DictReader(file, delimiter=';')
        for row in arquivo:
            latitude = float(row['LATITUDE'])
            longitude = float(row['LONGITUDE'])
            df.append([latitude, longitude])
    return df  # retorna o novo dataframe com as informações adicionadas


# Calcula a distância algébrica dos pontos
def distancia(ponto1, ponto2):
    return math.sqrt((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2)


# É a somatória total das distâncias utilizadas na rota
# O objetivo é de demonstrar a distância total (em diferença de latitude)
def distancia_total(rota, distancias):
    total = 0
    for cac in range(len(rota) - 1):  # Passa por cada um dos itens da lista distancias
        total += distancias[rota[cac]][rota[cac + 1]]  # Acresce ao total
    total += distancias[rota[-1]][rota[0]]  # Acresce ao total
    return total  # Devolve a quantidade total de distância


# Cria uma solução de TSP com dados aleatórios,
# ela servirá de base para comparação com outros resultados
def soluble_inicial(leitores, pintos):
    n_pontos = len(pintos)
    soluc = []
    for iteracao in range(leitores):
        rotas = [0]  # Começa como uma lista com um item
        while len(rotas) < n_pontos:  # Itera para cada um dos pontos
            prox_p = random.choice([p for p in range(n_pontos) if p not in rotas])
            rotas.append(prox_p)  # Adiciona a rota "sorteada" à lista de rotas
        rotas.append(0)  # Returna ao ponto 0, marcando a virada de rota
        soluc.append(rotas)
    return soluc


# Retorna uma nova solução onde se trocam 2 pontos
# Ela vai ser testada com a solução antiga, para verificar se é melhor.
def neighbour(solucao):
    nova_soluble = solucao.copy()
    # Seleciona duas rotas aleatórias e troca um ponto entre elas
    rota1, rota2 = random.sample(range(len(solucao)), 2)
    ponto1 = random.choice(solucao[rota1][1:-1])

    nova_soluble[rota1].remove(ponto1)
    index = random.randint(1, len(solucao[rota2]) - 1)
    nova_soluble[rota2].insert(index, ponto1)

    return nova_soluble


# Faz uma verificação da aceitação probabilística do custo atual.
# Compara os valores e a "temperatura" para verificar a aceitação
def aceitacao(custo_atual, custo, temperatura):
    if custo < custo_atual:
        return 1.0
    return math.exp((custo_atual - custo) / temperatura)


# Nesta função, ocorre o simulated annealing (recozimento simulado, em português [nome esquisito, mas que
# se refere a um processo físico de recozimento que confere na insistência de cozimento de uma substância
# em busca de uma melhora da sua qualidade, semelhantemente ao que ocorreu no código])

# Ele reavalia o resultado atual (que genericamente é ruim) com a ideia de chegar perto de um
# resultado aceitável para a solução, progressivamente se afastando de resultados que não se
# aproximam dessa métrica e chegando a ideias mais aceitáveis e as substituindo na solução atual.
# Assim, se melhora uma solução progressivamente. Isso ocorre na busca por vizinhos bem próximos (valores similares)

# Foi feito isso para as distâncias, tentando se diminuir progressivamente
def simulated_annealing(distancias, n_leiturista, pontos, temperatura_inicial=1000, resfriamento=0.99,
                        parada=0.1):
    soluc_atual = soluble_inicial(n_leiturista, pontos)
    custo_atual = sum([distancia_total(route, distancias) for route in soluc_atual])
    temperatura = temperatura_inicial

    while temperatura > parada:
        nova_soluc = neighbour(soluc_atual)
        novo_custo = sum([distancia_total(route, distancias) for route in nova_soluc])
        if aceitacao(custo_atual, novo_custo, temperatura) > random.random():
            soluc_atual = nova_soluc
            custo_atual = novo_custo
        temperatura *= resfriamento

    return soluc_atual, custo_atual


# Roda o código com as variáveis endereçadas
# O número de leituristas é um parâmetro que pode ser mudado, por exemplo
if __name__ == "__main__":
    arq = "AMOTRA_MENOR.csv"
    leituristas = 10  # Número de leituristas
    data = cria_df(arq)
    dist = np.zeros((len(data), len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            dist[i][j] = distancia(data[i], data[j])
    solution, custo = simulated_annealing(dist, leituristas, data)
    print("Melhor solução: ", solution)
    print("Custo total:", custo)
