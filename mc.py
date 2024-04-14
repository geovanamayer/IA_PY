from collections import deque

# Define a classe que representa um estado do problema
class Estado:
    def __init__(self, m, c, lado_barco):
        self.m = m  # Número de missionários na margem
        self.c = c  # Número de canibais na margem
        self.lado_barco = lado_barco  # Lado do rio onde está o barco
    
    def __eq__(self, other):
        return self.m == other.m and self.c == other.c and self.lado_barco == other.lado_barco
    
    def __hash__(self):
        return hash((self.m, self.c, self.lado_barco))
    
    def __str__(self):
        return f"Missionários: {self.m}, Canibais: {self.c}, Barco: {'Esquerda' if self.lado_barco == 0 else 'Direita'}"

# Define uma função para verificar se um estado é válido
def estado_valido(estado):
    # Verifica se os canibais não superam os missionários em nenhuma margem
    if estado.m < estado.c and estado.m > 0:
        return False
    if 3 - estado.m < 3 - estado.c and 3 - estado.m > 0:
        return False
    return True

# Define uma função para gerar os estados sucessores a partir de um estado atual
def gerar_sucessores(estado):
    sucessores = []
    # Define todas as combinações possíveis de passageiros para atravessar o rio
    combinacoes = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]
    for c in combinacoes:
        novo_estado = Estado(estado.m - c[0] * (-1) ** estado.lado_barco, 
                             estado.c - c[1] * (-1) ** estado.lado_barco, 
                             1 - estado.lado_barco)
        if estado_valido(novo_estado):
            sucessores.append(novo_estado)
    return sucessores

# Define a função BFS para resolver o problema
def bfs(inicial, final):
    fila = deque([inicial])
    visitados = set()
    caminho = {}
    while fila:
        estado_atual = fila.popleft()
        if estado_atual == final:
            solucao = []
            while estado_atual != inicial:
                solucao.append(estado_atual)
                estado_atual = caminho[estado_atual]
            solucao.append(inicial)
            return solucao[::-1]
        visitados.add(estado_atual)
        for proximo_estado in gerar_sucessores(estado_atual):
            if proximo_estado not in visitados:
                fila.append(proximo_estado)
                caminho[proximo_estado] = estado_atual
    return None

# Define o estado inicial e final do problema
estado_inicial = Estado(3, 3, 0)  # Três missionários e três canibais na margem esquerda
estado_final = Estado(0, 0, 1)     # Todos os missionários e canibais na margem direita

# Resolve o problema usando BFS
caminho_solucao = bfs(estado_inicial, estado_final)

# Exibe o caminho da solução
if caminho_solucao:
    for i, estado in enumerate(caminho_solucao):
        print(f"Passo {i+1}: {estado}")
else:
    print("Não foi encontrada uma solução.")
