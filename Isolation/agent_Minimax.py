from typing import List, Tuple
from board import Board
from agent import Agent
import random

animation = [
    "[=     ]",
    "[ =    ]",
    "[  =   ]",
    "[   =  ]",
    "[    = ]",
    "[     =]",
    "[    = ]",
    "[   =  ]",
    "[  =   ]",
    "[ =    ]",
]

class AgentMinimax(Agent):
    def __init__(self, player=1):
        self.player = player
        self.other_player = 2
    def next_action(self, board: Board) -> tuple[int, int]:
        self.idx = 0
        _, pos = self.minimax(board, self.player,4)
        return pos


    def minimax(self, board: Board, player: int, d: int) -> tuple[int, tuple[int, tuple[int, int]]]:
        actions = board.get_possible_actions(player)

        random.shuffle(actions)

        # Caso base
        ended, winner = board.is_end(player)
        if ended or d == 0:
            if winner == self.player:
                return 100, [None, None]
            elif winner == self.other_player:
                return -100, [None, None]
            else:
                return self.heuristic_utility(board), (None, None)

        # Casos no base
        action_nodes = []

        for action in actions:
            child_board = board.clone()
            child_board.play(action, player)  # Acción es un array en el que la posición 0 es la dirección
            action_nodes.append((action, child_board))

        value = float('-inf') if player == 1 else float('inf')
        chosen_action = (None, None)

        if player != 1:  # Minimizer
            for action_node in action_nodes:
                aux_value, _ = self.minimax(action_node[1], 1, d - 1)
                if aux_value <= value:
                    value = aux_value
                    chosen_action = action_node[0]
        else:  # Maximizer (player == self.player)
            for action_node in action_nodes:
                aux_value, _ = self.minimax(action_node[1], 2, d - 1)
                if aux_value >= value:
                    value = aux_value
                    chosen_action = action_node[0]

        return value, chosen_action
    
    def heuristic_utility(self, board: Board):
        # Obtener las posiciones de los jugadores
        player_position = board.find_player_position(self.player)
        opponent_position = board.find_player_position(self.other_player)

        # Contar la cantidad de celdas ocupadas por cada jugador
        player_cells = 1 if player_position else 0
        opponent_cells = 1 if opponent_position else 0

        # Calcular la distancia Manhattan entre los jugadores si ambos están presentes
        distance = 0
        if player_position and opponent_position:
            distance = abs(player_position[0] - opponent_position[0]) + abs(player_position[1] - opponent_position[1])

        # Valorar la cantidad de movimientos disponibles
        player_moves = len(board.get_possible_actions(self.player))
        opponent_moves = len(board.get_possible_actions(self.other_player))

        # Calcular la heurística general
        utility = player_cells - opponent_cells - 0.5 * distance + 0.5 * (opponent_moves - player_moves)

        return utility






