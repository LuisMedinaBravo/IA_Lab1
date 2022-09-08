"""Games or Adversarial Search (Chapter 5)"""

#Nos basamos en el código de la siguiente dirección (clase minmax_decision):
#https://github.com/aimacode/aima-python/blob/master/games.py


import operator
import random
from collections import namedtuple

import numpy as np

jug = 0
nodofinal = -1
esInt = False


##Verificamos que la entrada sea un número entero mayor que cero
while esInt == False:


   print("Ingrese el nivel máximo del árbol: ")
   seleccion3 = input()
   
   if(seleccion3.isnumeric()):
        if seleccion3 > str(0):
            esInt=True
   else:
     print("Entrada no válida")
     print("")


GameState = namedtuple('GameState', 'to_move, utility, board, moves')
StochasticGameState = namedtuple('StochasticGameState',
                                 'to_move, utility, board, moves, chance')


def vector_add(a, b):
    """Component-wise addition of two vectors."""
    return tuple(map(operator.add, a, b))


# ______________________________________________________________________________
# MinMax Search

      

def minmax_decision(state, game, nivel):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""
   
    player = game.to_move(state)
  
    def max_value(state, nivel):
        
        if(nivel==seleccion3):
          return 0
        if game.terminal_test(state):
            return game.utility(state, player)
        #infinto
        nivel = nivel +1
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), nivel))
        return v

    def min_value(state, nivel):
        if(nivel==10):
          return 0
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        nivel=nivel+1
        for a in game.actions(state):
            
            v = min(v, max_value(game.result(state, a),nivel))
        return v

    # Body of minmax_decision:
    return max(game.actions(state),
               key=lambda a: min_value(game.result(state, a), nivel))


# ______________________________________________________________________________


def alpha_beta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            print("Se podo en el estado: "+str(state)+", produndidad:"+str(depth))
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta,
                                 depth + 1))
            
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            print("Se podo en el estado: "+str(state)+", produndidad:"+str(depth))
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta,
                                 depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (
        cutoff_test
        or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


# ______________________________________________________________________________
# Players for Games


def query_player(game, state, jug):
    """Make a move by querying standard input."""
    print("Nodo actual:")
    game.display(state)
    print("")
    print("Ciudades disponibles para moverse: {}".format(game.actions(state)))
    if len(game.actions(state)) == 0:
        print("Esta vacia la lista de ciudades disponibles")
    else:
        print("Esta llena la lista de ciudades disponibles")

    print("")
    move = None
    if game.actions(state):
        
        try:
            
            flag=0

            while flag==0:

             move_string = input('¿A qué ciudad te quieres mover? ')
             print(move_string) 
             move = eval(move_string)
             if move_string>=str(0):
                  if move_string<=str(9):
                    flag=1
                                  
             else:
                 print("Ciudad fuera de rango")

              
          
            print("jugador " + str(jug) + " quiere moverse a " + move_string)

            if jug == 1:
                jug = 2
            else:
                jug = 1

        except NameError:
            move = move_string

    else:
        print('no legal moves: passing turn to next player')
    return move


def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None


def alpha_beta_player(game, state):
    return alpha_beta_search(state, game)


def minmax_player(game, state):
    return minmax_decision(state, game)


# ______________________________________________________________________________
# Some Sample Games


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


class CircuitoCiudades(Game):

    def __init__(self, matrizAdyacencia, ciudadSalida, ciudadLlegada):
        self.m = matrizAdyacencia
        self.s = ciudadSalida
        self.l = ciudadLlegada
        self.actual = ciudadLlegada
       
        self.visitadas1 = [ciudadSalida]
        self.visitadas2 = []
        self.suma1 = 0
        self.suma2 = 0
        self.turno = True

    def actions(self, state):
        """"retorna las jugadas posibles de este estado"""
        movimientos = []
        contador = 0
        for x in self.m[state]:
            if (x != 0):
                if (self.turno == True):  #jugador 1
                    if (not contador in self.visitadas1):
                        #print("jugador 1 se movió a "+str(contador))
                        #print("No se puede mover a "+str(self.visitadas1))
                        movimientos.append(contador)
                        self.turno = False
                      
                else:  #jugador 2
                    if (not contador in self.visitadas2):
                        movimientos.append(contador)
                       # print("jugador 2 se movió a "+str(contador))
                        #print("No se puede mover a "+str(self.visitadas2))
                        self.turno = True

            contador = contador + 1
            
        #for y in movimientos:
        #    print(y, end=" ")

        return movimientos

    def utility(self, state, player):
        """Return the value of this final state to player."""
        print("J1 " + str(self.suma1))
        print("J2 " + str(self.suma2))
      
        if (self.suma1 > self.suma2):
            print("Ganó J1")
            print("Fin combinación de jugada")
            print("")
            #exit()
            return self.suma1
            #exit()
        elif (self.suma1 == self.suma2):
            print("Empate")
            print("Fin combinación de jugada")
            print("")
            #exit()
            return self.suma1
            #exit()
            
        else:
            print("Ganó J2")
            print("Fin combinación de jugada")
            print("")
            #exit()
            return self.suma2
            #exit()
          
    def display(self, state):
        """Print or otherwise display the state."""
        print("Mi estado es: " + str(state))

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.s
        while True:
            for player in players:
                ##move = player(self, state)
                move = query_player(self, state, jug)
                
                state = self.result(state, move)
                ## query_player(self, state,jug)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.s))

        ##moves = [(x, y) for x in range(1, h + 1)
        ##       for y in range(1, v + 1)]

    ## self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)
    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        if (self.turno == True):
            self.suma1 = self.suma1 + self.m[0][move]
      ##      print("j1 lleva " + str(self.suma1))
        else:
            self.suma2 = self.suma2 + self.m[0][move]
        ##    print("j2 lleva " + str(self.suma2))
        self.turno = not self.turno
        if (self.turno == True):
            self.visitadas1.append(move)
        else:
            self.visitadas2.append(move)

       # print("jugada con mayor valor "+str(self.m[0][move]))

        return move

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        #return state.to_move
        return self.turno

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        if (state == self.l):
            #print("Fin combinación de jugadas")
            print("")
            return True
        if (len(self.actions(state)) == 0):
            #print("Fin combinación de jugadas")
            print("")
            return True
        return not self.actions(state)

        raise NotImplementedError

    def printMatrizCiudades(self):
        for x in self.m[0]:
            print(x)


          
##matriz
print("")
print("Espacio de Estados")
print("")
a = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]



#llenado de matriz
for i in range(10):
    for j in range(10):
        if i == j:
            break
        if j != i:
            a[i][j] = random.randint(0, 20)
            a[j][i] = a[i][j]

print("****************************************")
print("Matriz de adyacencia aleatoria creada")
print("")
for p in a:
    print(p)

print("****************************************")
##fin llenado matriz

##b.printMatrizCiudades()
print("")
print("Empieza J1")

print("")
print("")
print("Ciudades disponibles ")
print("[A, B, C, D, E, F, G, H, I, J]")

print("Escoge la ciudad de PARTIDA: ")

valido = 1
partida = -1

while valido != 0:

    seleccion = input()

    if seleccion == 'A':
        partida = 0
        valido = 0
    elif seleccion == 'B':
        partida = 1
        valido = 0
    elif seleccion == 'C':
        partida = 2
        valido = 0
    elif seleccion == 'D':
        partida = 3
        valido = 0
    elif seleccion == 'E':
        partida = 4
        valido = 0
    elif seleccion == 'F':
        partida = 5
        valido = 0
    elif seleccion == 'G':
        partida = 6
        valido = 0
    elif seleccion == 'H':
        partida = 7
        valido = 0
    elif seleccion == 'I':
        partida = 8
        valido = 0
    elif seleccion == 'J':
        partida = 9
        valido = 0
    else:
        print("Opción no válida")
        print("")
        print("Ingrese otro estado inicial")
        valido = 1

print("Ciudad de inicio es: ", partida)

print("")
print("")
print("Ciudades disponibles ")
print("[A, B, C, D, E, F, G, H, I, J]")

print("Escoge la ciudad de TERMINO: ")

valido = 1

while valido != 0:

    seleccion2 = input()

    if seleccion2 == 'A' and seleccion != seleccion2:
        nodofinal = 0
        valido = 0
    elif seleccion2 == 'B' and seleccion != seleccion2:
        nodofinal = 1
        valido = 0
    elif seleccion2 == 'C' and seleccion != seleccion2:
        nodofinal = 2
        valido = 0
    elif seleccion2 == 'D' and seleccion != seleccion2:
        nodofinal = 3
        valido = 0
    elif seleccion2 == 'E' and seleccion != seleccion2:
        nodofinal = 4
        valido = 0
    elif seleccion2 == 'F' and seleccion != seleccion2:
        nodofinal = 5
        valido = 0
    elif seleccion2 == 'G' and seleccion != seleccion2:
        nodofinal = 6
        valido = 0
    elif seleccion2 == 'H' and seleccion != seleccion2:
        nodofinal = 7
        valido = 0
    elif seleccion2 == 'I' and seleccion != seleccion2:
        nodofinal = 8
        valido = 0
    elif seleccion2 == 'J' and seleccion != seleccion2:
        nodofinal = 9
        valido = 0
    else:
        print("Opción no válida")
        print("")
        print("Ingrese otro estado final")
        valido = 1

print("Ciudad de término es: ", nodofinal)
print("")
print("Listado de todas las combinaciones posibles para el nivel ingresado:")
print("")

b = CircuitoCiudades(a, 0, nodofinal)

#b.play_game("J1", "J2")

#print("La mejor jugada es ir a el nodo: "+str(minmax_decision(0, b, 0)))


#Actividad 3 
#considerar que por tema de recursividad, entregara la poda desde,
#  el mas profundo hacia el menos profundo
alpha_beta_cutoff_search(0, b, d=4, cutoff_test=None, eval_fn=None)