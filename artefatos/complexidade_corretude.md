
# Complexidade e corretude do algoritmo

## Introdução

&emsp;&emsp;Neste documento, são apresentados os algoritmos propostos e aplicados computacionalmente para a execução da solução esperada pela empresa parceira (Aegea). A problemática que cerceia este projeto está devidamente enunciada e referenciada nos demais arquivos que complementam este repositório, explicitando as nuances técnicas e o resultado aguardado.

&emsp;&emsp;Simplificando a questão, entretanto, entende-se que o objetivo dos códigos desenvolvidos é de, pensando em todas as localidades dos clientes da empresa em questão, conseguir percorrer todos os endereços com economia de tempo, distância e quantidade de colaboradores. Para que tal seja completo, foi idealizada matematicamente uma solução que está descrita em um arquivo deste mesmo repositório, na qual se verificam restrições e equações que delimitam a solução e permitem a busca pela solução ótima. Pensando nesta análise, foram desenvolvidos três algoritmos diferentes, que procuram resolver a problemática de maneira significativa: um deles pretende dividir todos os pontos em subconjuntos para facilitar a exploração e outros dois tentam organizar continuamente estas informações.

## Algoritmos Escolhidos
Para resolver o problema, foram adotados três algoritmos principais:

- *K-Means*: Utilizado para agrupar as localidades em clusters baseados em sua proximidade geográfica, facilitando a otimização das rotas dentro de cada grupo.
  
- *Nearest Neighbor com KDTree*: Aplicado para determinar a rota mais curta dentro de cada cluster, selecionando o vizinho mais próximo ainda não visitado em cada passo.

- *Ant Colony Optimization (ACO)*: Este algoritmo bio-inspirado simula o comportamento de formigas que buscam o menor caminho entre fontes de alimento e a colônia, ideal para problemas de roteamento e otimização combinatória.

&emsp;&emsp;O _K-means_ é um algoritmo de _clustering_ (agrupamento) que tem como objetivo dividir o conjunto total de indivíduos (neste caso, endereços) se baseando na distribuição de $n$ centróides dentre todos os pontos disponíveis, reunindo-os em $n$ grupos distintos baseando-se na proximidade com os núcleos mais próximos. É um problema computacionalmente difícil, entretanto, dependendo da aplicação algorítmica, converge rapidamente para ótimos locais que suficientemente auxiliam na resolução do problema.

&emsp;&emsp;O _Nearest Neighbor_ (ou, em tradução literal, Vizinho Mais Próximo) é uma heurística que busca resolver exemplos do Problema do Caixeiro Viajante através de uma estratégia gulosa: começando em um ponto arbitrário dentre todos os existentes, o código encontra aquele que, dentre todos os disponíveis, está mais próximo; este processo se repete de maneira recursiva, até que todos os pontos sejam visitados.  Para melhorar a eficiência na busca dos pontos mais próximos, pode-se utilizar uma estrutura de dados chamada KD-Tree, que permite a realização de consultas espaciais de maneira mais rápida e eficiente.

&emsp;&emsp;Esta implementação é simples encontra caminhos relativamente eficientes. Por outro lado, a heurística de _Nearest Neighbor_ geralmente encontra soluções sub-ótimas, ou seja, aquelas que, apesar de se aproximarem do resultado ideal, não o atingem. Isto ocorre pois as ações tomadas em cada uma das instâncias não levam em consideração o impacto destas a longo prazo. Em casos nos quais a quantidade de dados é elevada, esta situação se acentua, sendo que, constantemente, o algoritmo vai encontrar soluções mais distintas do resultado ótimo.

&emsp;&emsp;A utilização de KD-Tree ajuda a reduzir o tempo de execução do algoritmo, tornando a busca pelo vizinho mais próximo mais eficiente, especialmente em instâncias maiores. No entanto, mesmo com essa otimização, o Nearest Neighbor ainda mantém as suas limitações intrínsecas, como a dependência da cidade inicial e a incapacidade de capturar a estrutura global do problema. Portanto, enquanto a KD-Tree melhora a performance, ela não altera a natureza gananciosa do algoritmo, que continua propenso a gerar percursos sub-ótimos em comparação com outras técnicas mais avançadas.

&emsp;&emsp;Já o _Ant Colony Optimization_ é uma prática probabilística para resolução de problemas, inspirando-se no processo biológico de encontro de caminhos comuns pelas formigas. O algoritmo percorre por diversas instâncias semi-aleatórias, representando cada qual uma agente independente (uma formiga artificial). Estes manejam os diferentes parâmetros que ainda transitam dentre alguma solução existente, percorrendo os resultados encontrados em busca daquele que apresenta o melhor resultado dada a função objetivo. Este algoritmo foi inicialmente citado em 1992, na tese de doutorado de Marco Dorigo, e seu objetivo era de encontrar o melhor caminho dentro de um grafo a partir do caminho que formigas fazem entre sua casa e a fonte de alimento. Essa perspectiva se inspandiu e permitiu a criação de diversos outros algoritmos que seguem o mesmo formato. Esta não garante o resultado ótimo, por se tratar de uma presunção meta-heurística, entretanto atinge um resultado razoavelmente bom em comparação com outros algoritmos.

## Análise dos algoritmos escolhidos
### K-Means:
- *Complexidade*: A complexidade de tempo do K-Means é geralmente $(O(n \cdot k \cdot i))$, onde $(n)$ é o número de pontos (localidades), $(k)$ é o número de clusters, e $(i)$ é o número de iterações até a convergência. Esta complexidade pode variar com a implementação e a rapidez com que os centros dos clusters convergem.
  
- *Melhor caso*: Quando os pontos já estão naturalmente agrupados de maneira que a atribuição inicial aos clusters é próxima da configuração ideal, reduzindo o número de iterações necessárias.
  
- *Pior caso*: Ocorre quando os dados estão distribuídos de forma que os clusters iniciais estão muito distantes dos centros finais, exigindo múltiplas iterações para ajustar os centros dos clusters.

#### Invariante com justificativa

&emsp;&emsp;A fórmula da invariante tenta defender que  é que a soma das distâncias quadradas de cada ponto ao seu centroide mais próximo não aumenta a cada iteração. Assim, esta pode ser escrita como:

$$\sum_{i=1}^{n} \min_{1 \leq j \leq k} \| x_i - \mu_j \|^2 $$

Onde:
- $n$ é o número de pontos de dados.
- $k$ é o número de clusters.
- $x_i$ é o $i$-ésimo ponto de dados.
- $\mu_j$ é o centroide do $j$-ésimo cluster.
- $\| x_i - \mu_j \|^2$ é a distância quadrada entre o ponto $x_i$ e o centroide $\mu_j$.


#### Demonstração da corretude

&emsp;&emsp;Prova de Corretude do _K-Means_ por Indução

- Caso Base $(k = 1)$:

&emsp;&emsp;Com apenas um cluster, todos os pontos são atribuídos ao mesmo centroide. A soma das distâncias quadradas de cada ponto ao seu centroide mais próximo é mínima e não pode aumentar.

- Hipótese Indutiva:

&emsp;&emsp;Suponha que a invariante seja verdadeira para $(k = l)$, ou seja, para $(l)$ clusters:


$$\sum_{i=1}^{n} \min_{1 \leq j \leq l} | x_i - \mu_j |^2 \leq \sum_{i=1}^{n} \min_{1 \leq j \leq l-1} | x_i - \mu_j |^2$$


- Passo Indutivo (k = l + 1):

&emsp;&emsp;Na iteração do algoritmo K-Means que adiciona um novo cluster $(l+1)$, cada ponto $(x_i)$ é reatribuído ao centroide mais próximo entre os $(l+1)$ centroides existentes.

- Reatribuição de Pontos:

&emsp;&emsp;Um ponto $(x_i)$ pode ser reatribuído do cluster $(j)$ para o cluster $(l+1)$ se a distância quadrada entre ele e o centroide $(l+1)$ for menor do que a distância quadrada entre ele e o centroide $(j)$.

&emsp;&emsp;Essa reatribuição garante que a distância quadrada entre $(x_i)$ e seu centroide mais próximo não aumente.

- **Distância Quadrada Total**:

&emsp;&emsp;A soma das distâncias quadradas de todos os pontos aos seus centroides mais próximos pode ser dividida em duas partes:

1.  A soma das distâncias quadradas dos pontos que não foram reatribuídos (permanecem no cluster original); 

2. A soma das distâncias quadradas dos pontos reatribuídos ao novo cluster $(l+1)$.

&emsp;&emsp;A soma das distâncias quadradas dos pontos que não foram reatribuídos não aumenta, pois a reatribuição só ocorre se a distância quadrada diminuir.

&emsp;&emsp;A soma das distâncias quadradas dos pontos reatribuídos ao novo cluster $(l+1)$ é menor ou igual à soma das distâncias quadradas desses pontos aos seus centroides mais próximos antes da reatribuição. Isso ocorre porque a reatribuição só ocorre se a distância quadrada entre o ponto e o centroide $(l+1)$ for menor do que a distância quadrada entre ele e o centroide original.

&emsp;&emsp;Portanto, a soma das distâncias quadradas de todos os pontos aos seus centroides mais próximos não aumenta após a reatribuição.

&emsp;&emsp;Pelas etapas acima, provamos que a invariante se mantém para $(k = l+1)$, assumindo que ela seja verdadeira para $(k = l)$. Como foi demostrado no caso base, a invariante também é verdadeira para $(k = 1)$. Portanto, a invariante se mantém para todos os valores de $(k)$ (número de clusters), comprovando que a soma das distâncias quadradas de cada ponto ao seu centroide mais próximo não aumenta a cada iteração do algoritmo K-Means. Assim, verifica-se a integridade do algoritmo e da resposta esperada.

### Ant Colony Optimization (ACO):
- *Complexidade*: Geralmente expressa como $(O(m \cdot n^2 \cdot t))$, onde $(m)$ é o número de formigas, $(n)$ o número de cidades ou localidades, e $(t)$ o número de iterações. Cada formiga constrói uma solução completa por iteração, e a avaliação de cada movimento requer considerar todas as cidades ainda não visitadas.
  
- *Melhor caso*: Quando as formigas rapidamente convergem para um caminho ótimo, diminuindo a quantidade de iterações necessárias para a convergência da solução.
  
- *Pior caso*: Ocorre em espaços de busca grandes onde a distribuição inicial dos feromônios não favorece a convergência rápida, resultando em muitas iterações sem melhoria significativa na qualidade da solução.

#### Invariante com justificativa

&emsp;&emsp;A fórmula da invariante do laço para o algoritmo de otimização de rota baseado em formigas (_Ant Colony Optimization - ACO_) pode ser descrita da seguinte forma:

&emsp;&emsp;Seja $ P $ o conjunto de todas as formigas, $ T $ o conjunto de todas as iterações do algoritmo, e $\tau_{ij}^t$ o feromônio presente na aresta $(i, j)$ na iteração $t$. Se $L_k$ é o comprimento do caminho encontrado pela formiga $k$ e $L_{\text{global}}$ é o comprimento do caminho mais curto global encontrado até o momento, a invariante pode ser expressa matematicamente como:

$$
\tau_{ij}^t = (1 - \text{decay}) \cdot \tau_{ij}^{t-1} + \sum_{k \in P} \Delta \tau_{ij}^k
$$

&emsp;&emsp;Onde $\Delta \tau_{ij}^k$ é a quantidade de feromônio depositada pela formiga $k$ na aresta $(i, j)$ durante a iteração atual. 

&emsp;&emsp;Essa fórmula representa a atualização do feromônio em cada iteração, onde o feromônio evapora com uma taxa de decaimento $\text{decay}$ e é reforçado pelas formigas que percorrem os caminhos. O caminho mais curto global é atualizado sempre que um caminho mais curto é encontrado por alguma formiga durante uma iteração.

#### Demonstração da corretude

&emsp;&emsp;Prova de Corretude do _Ant Colony_ por Indução:

- **Caso Base** $(t = 1)$:

&emsp;&emsp;Na primeira iteração, antes que qualquer formiga explore o ambiente, o feromônio em todas as arestas é inicializado com um valor inicial constante $\tau_{(ij)_0}$
​
 &emsp;&emsp;Como não há formigas depositando feromônio ainda, a fórmula de atualização se resume a:

$$
\tau_{ij}^1 = \tau_{ij}^0
$$

&emsp;&emsp;Essa condição inicial garante que a invariante se mantenha no caso base.

- **Hipótese Indutiva:**

&emsp;&emsp;Presume-se que a invariante seja verdadeira para a iteração $t=l$, ou seja:

$$
\tau_{ij}^l = (1 - \text{decay}) \cdot \tau_{ij}^{l-1} + \sum_{k \in P} \Delta \tau_{ij}^k
$$

- **Passo Indutivo** $(t = l + 1)$:

&emsp;&emsp;Na iteração $t=l+1$, as formigas exploram o ambiente e depositam feromônio nas arestas que percorrem. A quantidade de feromônio depositada por cada formiga é proporcional ao comprimento do caminho percorrido e inversamente proporcional à intensidade do feromônio naquela aresta.

&emsp;&emsp;Após todas as formigas terem explorado o ambiente, a fórmula de atualização é aplicada para atualizar o feromônio em cada aresta:

$$
\tau_{ij}^{l+1} = (1 - \text{decay}) \cdot \tau_{ij}^l + \sum_{k \in P} \Delta \tau_{ij}^k
$$

&emsp;&emsp;Essa fórmula garante que o feromônio em cada aresta na iteração $l+1$ seja a soma do feromônio remanescente da iteração anterior (devido à evaporação) e do feromônio depositado pelas formigas durante a iteração atual.

&emsp;&emsp;Se uma formiga $k$ encontrar um caminho mais curto do que o caminho global $L_global$ durante a iteração $l+1$, o valor de $L_global$ é atualizado para o novo comprimento do caminho. Isso garante que a invariante também se mantenha para o caminho global.

&emsp;&emsp;Pelas etapas acima, provamos que a invariante se mantém para a iteração $t=l+1$, assumindo que ela seja verdadeira para a iteração $t=l$. Como foi demonstrado no caso base, a invariante também é verdadeira para a iteração $t=1$. Portanto, a invariante se mantém para todas as iterações do algoritmo de formigas, comprovando que a fórmula de atualização do feromônio garante que a quantidade de feromônio em cada aresta na iteração t seja dada pela fórmula acima.

### Nearest Neighbor com KDTree:
- *Complexidade*: A construção da KDTree possui uma complexidade de $(O(n \log n))$ e a busca do vizinho mais próximo pode ser realizada em $(O(\log n))$ por consulta. Portanto, para percorrer todos os pontos, a complexidade total seria $(O(n \log n))$.
  
- *Melhor caso*: Acontece quando os pontos estão distribuídos equitativamente, permitindo que cada consulta ao KDTree rapidamente identifique o vizinho mais próximo.
  
- *Pior caso*: Surge em configurações onde a distribuição espacial dos pontos não favorece a eficiência da KDTree, potencialmente aumentando a complexidade para $(O(n^2))$ em situações extremas.

#### Invariante com justificativa

&emsp;&emsp;Para o algoritmo do Vizinho Mais Próximo (Nearest Neighbor), a invariante do laço pode ser expressa da seguinte forma:

&emsp;&emsp;Seja $C_i$ o custo do caminho parcial após a $i$-ésima iteração do algoritmo, então a invariante do laço é:

$$C_i = \min_{\text{ponto } j \text{ não visitado}} \left( C_{i-1} + \text{distância}(i, j) \right)$$

Onde:
- $C_i$ é o custo do caminho parcial após a $i$-ésima iteração.
- $C_{i-1}$ é o custo do caminho parcial após a $(i-1)$-ésima iteração.
- $\text{distância}(i, j)$ é a distância entre os pontos $i$ e $j$.
- O mínimo é tomado sobre todos os pontos $j$ que ainda não foram visitados.

 &emsp;&emsp;A invariante do laço do algoritmo do Vizinho Mais Próximo afirma que, a cada iteração, o custo do caminho parcial ($C_i$) é igual ao menor custo possível para alcançar um ponto não visitado a partir do caminho parcial atual.

#### Demonstração da corretude

&emsp;&emsp;Prova de Corretude do _Nearest Neighbor com KDTree_ por Indução


**Prova:**

 - **Caso Base (i = 1):**

Na primeira iteração, o caminho parcial consiste apenas do ponto inicial. O custo do caminho parcial ($C_1$) é igual à distância entre o ponto inicial e o ponto mais próximo não visitado. Essa escolha garante que o custo do caminho parcial seja o menor possível, pois nenhum outro caminho com apenas um ponto pode ter um custo menor.

 - **Hipótese Indutiva:**

Suponha que a invariante seja verdadeira para \(i = l\), ou seja, para a \(l\)-ésima iteração:

$$C_l = \min_{\text{ponto } j \text{ não visitado}} \left( C_{l-1} + \text{distância}(l, j) \right)$$

- **Passo Indutivo (i = l + 1):**

Na iteração \(l + 1\), o algoritmo seleciona o ponto não visitado mais próximo do caminho parcial atual e o adiciona ao caminho. O custo do caminho parcial atualizado ($C_{l+1}$) é calculado como a soma do custo do caminho parcial anterior ($C_l$) e da distância entre o último ponto adicionado ao caminho e o novo ponto selecionado.

1. **Seleção do Ponto Próximo:**

   - A escolha do ponto não visitado mais próximo garante que o custo do caminho parcial seja o menor possível entre todas as extensões possíveis com apenas um ponto.

2. **Atualização do Custo:**

   - O cálculo de $C_{l+1}$ como a soma de $C_l$ e a distância entre o último ponto adicionado e o novo ponto selecionado garante que o custo do caminho parcial atualizado seja o menor possível, considerando a escolha do ponto mais próximo.

&emsp;&emsp;Pelas etapas acima, provamos que a invariante se mantém para \(i = l+1\), assumindo que ela seja verdadeira para \(i = l\). Como foi demonstrado no caso base, a invariante também é verdadeira para \(i = 1\). Portanto, a invariante se mantém para todas as iterações do algoritmo do Vizinho Mais Próximo, comprovando que a cada iteração o custo do caminho parcial ($C_i$) é igual ao menor custo possível para alcançar um ponto não visitado a partir do caminho parcial atual.

## Conclusão
&emsp;&emsp;A combinação desses algoritmos oferece uma abordagem robusta e adaptável para problemas de otimização de rotas, aproveitando tanto métodos de clusterização quanto estratégias bio-inspiradas. Cada algoritmo tem suas forças e limitações, e sua aplicação depende das características específicas do problema, como a quantidade de dados e a complexidade da distribuição geográfica das localidades.




# Referencias:

BECKER, A. et al. New directions in nearest neighbor searching with applications to lattice sieving. Proceedings of the Twenty-Seventh Annual ACM-SIAM Symposium on Discrete Algorithms. Anais...Philadelphia, PA: Society for Industrial and Applied Mathematics, 2016. . Acesso em: 3 jun. 2024


BEWLEY, A.; UPCROFT, B. Advantages of exploiting projection structure for segmenting dense 3D point clouds. Disponível em: <https://www.araa.asn.au/acra/acra2013/papers/pap148s1-file1.pdf>. Acesso em: 3 jun. 2024.


BLUM, M. et al. Time bounds for selection. Journal of computer and system sciences, v. 7, n. 4, p. 448–461, 1973.


HAVRAN, V.; BITTNER, J. On improving kd-trees for ray shooting. Disponível em: <https://dcgi.felk.cvut.cz/home/bittner/publications/wscg02.pdf>. Acesso em: 3 jun. 2024.


MOORE, A. W. An intoductory tutorial on kdtrees. Disponível em: <https://web.archive.org/web/20160303203122/http://www.autonlab.com/autonweb/14665/version/2/part/5/data/moore-tutorial.pdf?branch=main&language=en>. Acesso em: 3 jun. 2024.


VAIDYA, P. M. AnO(n logn) algorithm for the all-nearest-neighbors Problem. Discrete & computational geometry, v. 4, n. 2, p. 101–115, 1989.


WALD, I.; HAVRAN, V. On building fast kd-Trees for Ray Tracing, and on doing that in O(N log N). 2006 IEEE Symposium on Interactive Ray Tracing. Anais...IEEE, 2006. . Acesso em: 3 jun. 2024


WIKIPEDIA CONTRIBUTORS. Nearest neighbor search. Disponível em: <https://en.wikipedia.org/w/index.php?title=Nearest_neighbor_search&oldid=1211732798>.


WIKIPEDIA CONTRIBUTORS. k-d tree. Disponível em: <https://en.wikipedia.org/w/index.php?title=K-d_tree&oldid=1225343225>.


Disponível em: <https://www.baeldung.com/cs/k-d-trees>. Acesso em: 3 jun. 2024.

