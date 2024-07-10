Foram criados testes unitários para testar duas rotas: ClusterORToolsController e KMeansAlgorithmController.

A rota ClusterORToolsController clusteriza os dados e roda o algoritmo do OR-Tools em cada um dos clusters.

A rota KMeansAlgorithmController também clusteriza os dados e depois roda o algoritmo de nearest neighbor em cada um dos clusters.

Os testes unitários rodam as rotas e verificam o status code de retorno, além disso, também é verificado se a resposta é um json válido.