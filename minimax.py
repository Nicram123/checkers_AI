import pygame
from copy import deepcopy
from constatnts import RED, WHITE
import math


class MinimaxAlgorithm:

    def __init__(self):
        # licznik dla statystyk
        self.nodes_visited = 0
        self.prunes = 0

    def reset_counters(self):
        self.nodes_visited = 0
        self.prunes = 0

    #
    def mini_max(self, dep, board, if_max, alpha=None, beta=None):
        if alpha is None:
            alpha = -math.inf
        if beta is None:
            beta = math.inf

        # zliczamy odwiedzony węzeł
        self.nodes_visited += 1

        # warunek zakończenia
        if dep == 0 or board.if_win_the_game() is not None:
            return board.score(), board, None

        if not if_max:
            return self._minimize(dep, board, alpha, beta)

        return self._maximize(dep, board, alpha, beta)

    def _maximize(self, dep, board, alpha, beta):
        best_piece = None
        optimal_action = None
        highest_evaluation = -math.inf

        actions = self.all_action(board, WHITE)

        if not actions:
            return board.score(), board, None

        for action, piece in actions:
            evaluation, _, _ = self.mini_max(dep - 1, action, False, alpha, beta)

            if evaluation > highest_evaluation:
                highest_evaluation = evaluation
                best_piece = piece
                optimal_action = action

            alpha = max(alpha, highest_evaluation)

            # pruning
            #if alpha >= beta:
            #    self.prunes += 1
            #    break

        return highest_evaluation, optimal_action, best_piece

    def _minimize(self, dep, board, alpha, beta):
        best_piece = None
        optimal_action = None
        lowest_evaluation = math.inf

        actions = self.all_action(board, RED)

        if not actions:
            return board.score(), board, None

        for action, piece in actions:
            evaluation, _, _ = self.mini_max(dep - 1, action, True, alpha, beta)

            if evaluation < lowest_evaluation:
                lowest_evaluation = evaluation
                best_piece = piece
                optimal_action = action

            beta = min(beta, lowest_evaluation)

            #if alpha >= beta:
            #    self.prunes += 1
            #    break

        return lowest_evaluation, optimal_action, best_piece

    # zwraca listę akcji
    def all_action(self, board, color):
        actions = []
        for obj in board.list_pieces(color):
            actual_actions = obj.possible_moves(board)
            for action, objects in actual_actions.items():
                temp_board = deepcopy(board)
                temp_obj = temp_board.board[obj.row][obj.col]

                if temp_obj != 0:
                    if color == WHITE:
                        for x in objects:
                            cloned_piece = temp_board.board[x.row][x.col]
                            if cloned_piece.king and cloned_piece in temp_board.king_piece:
                                temp_board.king_piece.remove(cloned_piece)
                                temp_board.number_of_kings_red -= 1

                new_board = self.imitate_action(action, temp_obj, objects, temp_board)
                actions.append((new_board, temp_obj))

        return actions

    # imitacja akcji
    def imitate_action(self, action, piece, objects, board):
        board.move(piece, action[0], action[1])
        if objects:
            board.remove(objects)
        return board
