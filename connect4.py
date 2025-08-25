# tabuleiro --------------------------------------------------------------------------------------

import numpy as np
import random


matriz = np.full((6, 7), '-', dtype=str)

def matrizorganizada(matrix): # organiza a matriz para ficar mais colorida
    print("")
    colunas = np.arange(7).reshape(1, 7)
    matrizcompleta = np.vstack((colunas, matrix))
    for i in matrizcompleta:
        for item in i:
            if item == 'X':
                print("\033[91m" + item, end=' ') # vermelho
            elif item == 'O':
                print("\033[94m" + item, end=' ') # azul
            else:
                print("\033[0m" + item, end=' ') # cinzento
        print("\033[0m") # resetar cor

# input de jogadas --------------------------------------------------------------------------------
def userinput():
    while True:
        try:
            jogada = int(input("Jogador 1: "))
            if 0 <= jogada <= 6:
                if turno(jogada, 'X', matriz) is False:
                    print("Coluna inválida")
                else:
                    break
            else:
                print("Número inválido")
        except ValueError:
            print("Input inválido")

def user2input():
    while True:
        try:
            jogada = int(input("Jogador 2: "))
            if 0 <= jogada <= 6:
                if turno(jogada, 'O', matriz) is False:
                    print("Coluna inválida")
                else:
                    break
            else:
                print("Número inválido")
        except ValueError:
            print("Input inválido")

def turno(valor, jogador, matrix):
    if matrix[0, valor] != '-': # coluna cheia
        return False
    for i in range(5, -1, -1):
        if matrix[i, valor] == '-':
            matrix[i, valor] = jogador
            break

def is_board_full(matriz):
    matriz_np = np.array(matriz)
    return np.all(matriz_np != '-')

# verificaçao vitoria ----------------------------------------------------------------------------

def vertical(matrix):
    for i in range(7):
        contador = 1
        for j in range(5):
            if matrix[j, i] != '-' and matrix[j, i] == matrix[j+1, i]:
                contador += 1
                if contador == 4:
                    return True
            else:
                contador = 1
    return False

def horizontal(matrix):
    for i in range(6):
        contador = 1
        for j in range(6):
            if matrix[i, j] != '-' and matrix[i, j] == matrix[i, j+1]:
                contador += 1
                if contador == 4:
                    return True
            else:
                contador = 1
    return False

def diagonal1(matrix):
    for i in range(3, 6):
        for j in range(4):
            if matrix[i, j] != '-' and matrix[i, j] == matrix[i-1, j+1] == matrix[i-2, j+2] == matrix[i-3, j+3]:
                return True
    return False

def diagonal2(matrix):
    for i in range(3):
        for j in range(4):
            if matrix[i, j] != '-' and matrix[i, j] == matrix[i+1, j+1] == matrix[i+2, j+2] == matrix[i+3, j+3]:
                return True
    return False

def vitoria(matrix):
    if vertical(matrix) or horizontal(matrix) or diagonal1(matrix) or diagonal2(matrix):
        return True
    return False

# contar pontos --------------------------------------------------------------------------------

def heuristica(seguidos):
    if seguidos == 0:
        totalpontos = 1
    elif seguidos == 1:
        totalpontos = 9
    elif seguidos == 2:
        totalpontos = 40
    else:
        totalpontos = 462
    return totalpontos

def pontosvertical(matrix):
    totalpontos = 0
    for i in range(7):
        pontos = 0
        anterior = '-'
        seguidosx = 0
        seguidoso = 0
        for j in range(5,-1,-1):
            if matrix[j, i] == 'X':
                if anterior == 'O':
                    seguidosx = 0
                    pontos = 0
                pontos += heuristica(seguidosx)
                seguidosx += 1
                anterior = 'X'
            elif matrix[j, i] == 'O':
                if anterior == 'X':
                    seguidosx = 0
                    pontos = 0
                pontos -= heuristica(seguidoso)
                seguidoso += 1
                anterior = 'X'
            else: 
                if ((j+seguidoso) > 2) or ((j+seguidosx) > 2):
                    totalpontos += pontos
                break
    return totalpontos

def pontoshorizontal(matrix):
    totalpontos = 0
    for i in range(6):
        pontos = 0
        seguidosx = 0
        seguidoso = 0
        for j in range(7):
            if matrix[i][j] == 'X':
                seguidoso = 0
                pontos += heuristica(seguidosx)
                seguidosx += 1
            elif matrix[i][j] == 'O':
                seguidosx = 0
                pontos -= heuristica(seguidoso)
                seguidoso += 1
            else: 
                seguidoso = 0
                seguidosx = 0
        totalpontos += pontos
    return totalpontos

def pontosdiagonal1(matrix):
    totalpontos = 0
    it=4
    p=2
    c=0
    for _ in range (3):
        pontos = 0
        seguidosx = 0
        seguidoso = 0
        i=p
        j=c
        for _ in range (0,it):
            if matrix[i][j] == 'X':
                seguidoso = 0
                pontos += heuristica(seguidosx)
                seguidosx += 1
            elif matrix[i][j] == 'O':
                seguidosx = 0
                pontos -= heuristica(seguidoso)
                seguidoso += 1
            else: 
                seguidoso = 0
                seguidosx = 0
            i +=1
            j +=1
        totalpontos += pontos
        it +=1
        p -=1

    it=6
    p=0
    c=1
    for _ in range (3):
        pontos = 0
        seguidosx = 0
        seguidoso = 0
        i=p
        j=c
        for _ in range (0, it):
            if matrix[i][j] == 'X':
                seguidoso = 0
                pontos += heuristica(seguidosx)
                seguidosx += 1
            elif matrix[i][j] == 'O':
                seguidosx = 0
                pontos -= heuristica(seguidoso)
                seguidoso += 1
            else: 
                seguidoso = 0
                seguidosx = 0
            i +=1
            j +=1
        totalpontos += pontos
        it -=1
        c +=1
    return totalpontos

def pontosdiagonal2(matrix):
    totalpontos = 0
    it=4
    p=0
    c=3
    for _ in range (3):
        pontos = 0
        seguidosx = 0
        seguidoso = 0
        i=p
        j=c
        for _ in range (0, it):
            if matrix[i][j] == 'X':
                seguidoso = 0
                pontos += heuristica(seguidosx)
                seguidosx += 1
            elif matrix[i][j] == 'O':
                seguidosx = 0
                pontos -= heuristica(seguidoso)
                seguidoso += 1
            else: 
                seguidoso = 0
                seguidosx = 0
            i +=1
            j -=1
        totalpontos += pontos
        it +=1
        c +=1
    it =6
    p=0
    c=6
    for _ in range (3):
        pontos = 0
        seguidosx = 0
        seguidoso = 0
        i=p
        j=c
        for _ in range (0,it):
            if matrix[i][j] == 'X':
                seguidoso = 0
                pontos += heuristica(seguidosx)
                seguidosx += 1
            elif matrix[i][j] == 'O':
                seguidosx = 0
                pontos -= heuristica(seguidoso)
                seguidoso += 1
            else: 
                seguidoso = 0
                seguidosx = 0
            i +=1
            j -=1
        totalpontos += pontos
        it -=1
        p +=1

    return totalpontos

def pontosgreedy(matrix):
    totalpontos = pontosvertical(matrix) + pontoshorizontal(matrix) + pontosdiagonal1(matrix) + pontosdiagonal2(matrix)
    return totalpontos

# jogar greedy ---------------------------------------------------------------------------------

def greedy():
    best_column = None
    best_score = float('inf')  

    for column in range(7):  
        if matriz[0, column] == '-': 
            temp_matrix = np.copy(matriz)
            turno(column, 'O', temp_matrix)
            score = pontosgreedy(temp_matrix)

            if score < best_score:
                best_score = score
                best_column = column

    return best_column  

# monte carlo --------------------------------------------------------------------------------------

class ConnectFourState:
    def __init__(self, matrix):
        self.matrix = matrix

    def is_terminal(self):
        return vitoria(self.matrix) or self.is_board_full()

    def is_board_full(self):
        return '-' not in self.matrix[0]

    def is_winning_move(self):
        for col in range(7):
            if self.matrix[0, col] == '-':
                temp_state = self.perform_move(col)
                if vitoria(temp_state.matrix):
                    return col
        return None

    def available_moves(self):
        winning_move = self.is_winning_move()
        if winning_move is not None:
            return [winning_move]
        return [col for col in range(7) if self.matrix[0, col] == '-']
    
    def perform_move(self, column):
        new_matrix = np.copy(self.matrix)
        for i in range(5, -1, -1):
            if new_matrix[i, column] == '-':
                if self.player_turn() == 1:
                    new_matrix[i, column] = 'X'
                else: new_matrix[i, column] = 'O'
                break
        return ConnectFourState(new_matrix)

    def clone(self):
        return ConnectFourState(np.copy(self.matrix))

    def player_turn(self):
        count_X = np.count_nonzero(self.matrix == 'X')
        count_O = np.count_nonzero(self.matrix == 'O')
        if ((count_X + count_O)%2) == 0:
            return 1 #turno X
        else: return 2 #turno O


    def get_result(self):
        if vitoria(self.matrix) and self.player_turn() == 1: # se for o turno do 'O' e ele ganhar retorna 1
            return 1
        else: return 0
    
    def print_matrix(self):
        for row in self.matrix:
            print(' '.join(row))
        print()
    
    

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.untried_moves = state.available_moves()


    def select_child(self):
        if len(self.children) == 0:
            raise ValueError("No children to select")
        
        # UCB1 para escolher o melhor filho
        exploration_constant = 1.4  
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = child.wins / child.visits + exploration_constant * np.sqrt(2*(np.log(self.visits)) / child.visits)
            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child

        return best_child
    
    def expand(self):
        if len(self.untried_moves) == 0:
            raise ValueError("No moves left to expand")

        # verifica se já existe um nó com o mesmo estado
        for child in self.children:
            if np.array_equal(child.state.matrix, self.state.matrix):
                return child

        # se n existir, expandir normalmente
        move = random.choice(self.untried_moves)
        new_state = self.state.perform_move(move)
        new_node = MCTSNode(new_state, parent=self, move=move)
        self.children.append(new_node)
        self.untried_moves.remove(move)

        return new_node


    def simulate(self, node):
        current_state = node.state.clone()
        while not current_state.is_terminal():
            random_move = random.choice(current_state.available_moves())  # escolha aleatória de movimento
            current_state = current_state.perform_move(random_move)  
        return current_state.get_result()


    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)

    

def suggest_move(current_state):
    root = MCTSNode(current_state)
    for _ in range(1500):  # nr de iteracoes
        node = root
        while not node.state.is_terminal() and node.untried_moves == []:
            node = node.select_child()
        if node.untried_moves != []:
            node = node.expand()
        result = node.simulate(node)
        node.backpropagate(result)
    best_child = root.select_child()
    return best_child.move


# jogo -----------------------------------------------------------------------------------------


def play_greedy():
    matrizorganizada(matriz)
    while True:
        userinput()
        if vitoria(matriz):
            matrizorganizada(matriz)
            print("Vitoria jogador 'X'!")
            break
        turno(greedy(),'O',matriz)
        matrizorganizada(matriz)
        if vitoria(matriz):
            print("Vitoria jogador 'O'!")
            break
        if is_board_full(matriz):
            print("Empate!")
            break

def x1():
    matrizorganizada(matriz)
    while True:
        userinput()
        matrizorganizada(matriz)
        if vitoria(matriz):
            print("Vitoria jogador 'X'!")
            break
        user2input()
        matrizorganizada(matriz)
        if vitoria(matriz):
            print("Vitoria jogador 'O'!")
            break
        if is_board_full(matriz):
            print("Empate!")
            break

def montecarlo():
    matrizorganizada(matriz)
    while True:
        userinput()
        matrizorganizada(matriz)
        if vitoria(matriz):
            matrizorganizada(matriz)
            print("Vitoria jogador 'X'!")
            break
        current_state = ConnectFourState(matriz)
        suggested_move = suggest_move(current_state)
        turno(suggested_move, 'O', matriz)
        matrizorganizada(matriz)
        if vitoria(matriz):
            print("Vitoria jogador 'O'!")
            break
        if is_board_full(matriz):
            print("Empate!")
            break

print("\n" + "\033[94m" + "Escolhe o modo que desejas jogar" + "\033[0m")

print("\033[91m" + "1" "\033[0m" + " - Jogador vs Jogador")
print("\033[91m" + "2" "\033[0m" + " - Greedy")
print("\033[91m" + "3" "\033[0m" + " - MCTS")
resposta = int(input("modo: "))
if resposta == 1:
    x1()
elif resposta == 2:
    play_greedy()
else:
    montecarlo()