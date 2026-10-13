#!/usr/bin/python3
# slitherlink.py: Template para implementação do projeto de Inteligência Artificial 2025/2026.

import random, copy
from sys import stdin
from collections import defaultdict

import utils
from utils import *

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class SlitherlinkState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = SlitherlinkState.state_id
        SlitherlinkState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id
    
    def __eq__(self, other):
        if not isinstance(other, SlitherlinkState):
            return False
        return self.board.edges == other.board.edges
    
    def __hash__(self):
        return hash(frozenset(self.board.edges.items()))


class Board:
    """Representação interna de um tabuleiro de Slitherlink."""

    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0]) if self.rows > 0 else 0

        self.edges = {}
        self.initialized_edges()

    def initialized_edges(self):
        for row in range(self.rows + 1):
            for column in range(self.columns):
                self.edges[('h', row, column)] = 0
        for row in range(self.rows):
            for column in range(self.columns + 1):
                self.edges[('v', row, column)] = 0
      
    def adjacent_cell(self, cell: tuple) -> list:
        row, col = cell
        adjacents = []
        if row > 0:
            adjacents.append((row-1, col))
        if row < self.rows - 1:
            adjacents.append((row+1, col))
        if col > 0:
            adjacents.append((row, col-1))
        if col < self.columns - 1:
            adjacents.append((row, col+1))
        return adjacents

    def get_cell_edges(self, row: int, column: int) -> list:
        edges = []
        edges.append(('h', row, column))
        edges.append(('h', row + 1, column))
        edges.append(('v', row, column))
        edges.append(('v', row, column + 1))
        return edges
    
    def get_cell_value(self, row: int, column: int) -> int:
        value = self.grid[row][column]
        return int(value)

    def get_active_edges(self, row: int, column: int) -> list:
        edges = self.get_cell_edges(row, column)
        active_edges = 0
        for edge in edges:
            if self.edges[edge] == 1:
                active_edges += 1
        return active_edges

    def is_move_valid(self, edge_type: str, row: int, column: int) -> bool:
        if edge_type == 'h':
            affected_cells = [(row-1, column), (row, column)]
        else:  # 'v'
            affected_cells = [(row, column-1), (row, column)]
        
        for r, c in affected_cells:
            if 0 <= r < self.rows and 0 <= c < self.columns:
                active_edges = self.get_active_edges(r, c)
                value = self.get_cell_value(r, c)
                if value != -1 and active_edges >= value:
                    return False
        return True 

    def is_board_valid(self) -> bool:
        for row in range(self.rows):
            for col in range(self.columns):
                value = self.get_cell_value(row, col)
                if value == -1:
                    continue
                active_edges = self.get_active_edges(row, col)
                if active_edges > value:
                    return False
        return True

    @staticmethod
    def parse_instance():
        grid = []
        for line in stdin:
            parts = line.strip().split()
            if parts:
                row = [int(x) if x != '.' else -1 for x in parts]
                grid.append(row)
        return Board(grid)

    def get_edge_state(self, edge_type: str, row: int, column: int) -> int:
        return self.edges[(edge_type, row, column)]
    
    def set_edge_state(self, edge_type: str, row: int, column: int, state: int):
        self.edges[(edge_type, row, column)] = state
    
    def set_edges(self, edge_list):
        """Batch set multiple edges at once. edge_list: [(type, row, col, state), ...]"""
        for edge_type, row, col, state in edge_list:
            self.set_edge_state(edge_type, row, col, state)
    
    def get_forbidden_edges(self, row: int, column: int) -> int:
        count = 0
        edges = self.get_cell_edges(row, column)
        for edge_type, edge_row, edge_col in edges:
            if self.edges[(edge_type, edge_row, edge_col)] == 2:
                count += 1
        return count

    def get_constraint_violation(self, row: int, column: int) -> int:
        value = self.get_cell_value(row, column)
        if value == -1:
            return 0
        active_edges = self.get_active_edges(row, column)
        forbidden_edges = self.get_forbidden_edges(row, column)
        if active_edges + forbidden_edges > value:
            return active_edges + forbidden_edges - value
        return 0
    

class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        self.board = board
        initial_state = SlitherlinkState(board)
        super().__init__(initial_state)

    def process_zeros(self, board: Board):
        for row in range(board.rows):
            for col in range(board.columns):
                value = board.get_cell_value(row, col)
                if value != 0:
                    continue

                edges = board.get_cell_edges(row, col)
                for edge in edges:
                    edge_type, edge_row, edge_col = edge
                    if edge_type == 'h' and 0 <= edge_row <= board.rows and 0 <= edge_col < board.columns:
                        if board.get_edge_state(edge_type, edge_row, edge_col) == 0:
                            board.set_edge_state(edge_type, edge_row, edge_col, 2)
                    elif edge_type == 'v' and 0 <= edge_row < board.rows and 0 <= edge_col <= board.columns:
                        if board.get_edge_state(edge_type, edge_row, edge_col) == 0:
                            board.set_edge_state(edge_type, edge_row, edge_col, 2)

                is_top = (row == 0)
                is_bottom = (row == board.rows - 1)
                is_left = (col == 0)
                is_right = (col == board.columns - 1)
                is_corner = (is_top or is_bottom) and (is_left or is_right)

                if not is_corner:
                    if is_top:
                        if col > 0: board.set_edge_state('h', 0, col - 1, 2)
                        if col < board.columns - 1: board.set_edge_state('h', 0, col + 1, 2)
                    elif is_bottom:
                        if col > 0: board.set_edge_state('h', row + 1, col - 1, 2)
                        if col < board.columns - 1: board.set_edge_state('h', row + 1, col + 1, 2)
                    elif is_left:
                        if row > 0: board.set_edge_state('v', row - 1, 0, 2)
                        if row < board.rows - 1: board.set_edge_state('v', row + 1, 0, 2)
                    elif is_right:
                        if row > 0: board.set_edge_state('v', row - 1, col + 1, 2)
                        if row < board.rows - 1: board.set_edge_state('v', row + 1, col + 1, 2)
    
    def process_corners(self, board: Board):
        corners = [
            (0, 0), (0, board.columns - 1),
            (board.rows - 1, 0), (board.rows - 1, board.columns - 1)
        ]
        
        for row, col in corners:
            value = board.get_cell_value(row, col)
            if value == -1:
                continue
            
            if value == 0:
                if row == 0:
                    if col == 0:
                        board.set_edge_state('h', 0, 1, 2)
                        board.set_edge_state('v', 1, 0, 2)
                    else:
                        board.set_edge_state('h', 0, col - 1, 2)
                        board.set_edge_state('v', 1, col + 1, 2)
                else:
                    if col == 0:
                        board.set_edge_state('h', row + 1, 1, 2)
                        board.set_edge_state('v', row - 1, 0, 2)
                    else:
                        board.set_edge_state('h', row + 1, col - 1, 2)
                        board.set_edge_state('v', row - 1, col + 1, 2)

            elif value == 1:
                if row == 0:
                    if col == 0:
                        board.set_edge_state('h', 0, 0, 2)
                        board.set_edge_state('v', 0, 0, 2)
                    else:
                        board.set_edge_state('h', 0, col, 2)
                        board.set_edge_state('v', 0, col + 1, 2)
                else:
                    if col == 0:
                        board.set_edge_state('h', row + 1, 0, 2)
                        board.set_edge_state('v', row, 0, 2)
                    else:
                        board.set_edge_state('h', row + 1, col, 2)
                        board.set_edge_state('v', row, col + 1, 2)
            
            elif value == 2:
                if row == 0:
                    if col == 0:
                        board.set_edge_state('h', 0, 1, 1)
                        board.set_edge_state('v', 1, 0, 1)
                    else:
                        board.set_edge_state('h', 0, col - 1, 1)
                        board.set_edge_state('v', 1, col + 1, 1)
                else:
                    if col == 0:
                        board.set_edge_state('h', row + 1, 1, 1)
                        board.set_edge_state('v', row - 1, 0, 1)
                    else:
                        board.set_edge_state('h', row + 1, col - 1, 1)
                        board.set_edge_state('v', row - 1, col + 1, 1)
            
            elif value == 3:
                if row == 0:
                    if col == 0:
                        board.set_edge_state('h', 0, 0, 1)  
                        board.set_edge_state('v', 0, 0, 1)  
                    else:
                        board.set_edge_state('h', 0, col, 1)  
                        board.set_edge_state('v', 0, col + 1, 1)  
                else:
                    if col == 0:
                        board.set_edge_state('h', row + 1, 0, 1)  
                        board.set_edge_state('v', row, 0, 1)  
                    else:
                        board.set_edge_state('h', row + 1, col, 1)  
                        board.set_edge_state('v', row, col + 1, 1)

    def process_threes(self, board: Board):
        for row in range(board.rows):
            for col in range(board.columns):
                value = board.get_cell_value(row, col)
                if value != 3:
                    continue

                adj_values = [
                    (row - 1, col, 'top'),
                    (row + 1, col, 'bottom'),
                    (row, col - 1, 'left'),
                    (row, col + 1, 'right')
                ]

                for row_adj, col_adj, pos in adj_values:
                    if not board.valid_position(row_adj, col_adj):
                        continue
                    
                    value_adj = board.get_cell_value(row_adj, col_adj)

                    if value_adj == 0:
  
                        if pos == 'bottom':
                            board.set_edge_state('v', row, col, 1)
                            board.set_edge_state('h', row, col, 1)
                            board.set_edge_state('v', row, col + 1, 1)
                            board.set_edge_state('h', row + 1, col - 1, 1)
                            board.set_edge_state('h', row + 1, col + 1, 1)
                            board.set_edge_state('v', row - 1, col, 2)
                            board.set_edge_state('v', row - 1, col + 1, 2)
                            board.set_edge_state('h', row - 1, col - 1, 2)
                            board.set_edge_state('h', row - 1, col + 1, 2)

                        elif pos == 'right':
                            board.set_edge_state('h', row, col, 1)
                            board.set_edge_state('v', row, col, 1)
                            board.set_edge_state('h', row + 1, col, 1)
                            board.set_edge_state('v', row - 1, col + 1, 1)
                            board.set_edge_state('v', row + 1, col + 1, 1)
                            board.set_edge_state('h', row, col - 1, 2)
                            board.set_edge_state('h', row + 1, col - 1, 2)
                            board.set_edge_state('v', row - 1, col, 2)
                            board.set_edge_state('v', row + 1, col, 2)

                    elif value_adj == 3:
                        if pos == 'top':
                            board.set_edge_state('h', row, col, 1)
                            board.set_edge_state('h', row + 1, col, 1)
                            board.set_edge_state('h', row - 1, col, 1)
                            board.set_edge_state('v', row, col, 2)
                            board.set_edge_state('v', row, col + 1, 2)
                        elif pos == 'bottom':
                            board.set_edge_state('h', row + 1, col, 1)
                            board.set_edge_state('h', row, col, 1)
                            board.set_edge_state('h', row + 2, col, 1)
                            board.set_edge_state('v', row + 1, col, 2)
                            board.set_edge_state('v', row + 1, col + 1, 2)
                        elif pos == 'left':
                            board.set_edge_state('v', row, col, 1)
                            board.set_edge_state('v', row, col + 1, 1)
                            board.set_edge_state('v', row, col - 1, 1)
                            board.set_edge_state('h', row, col, 2)
                            board.set_edge_state('h', row + 1, col, 2)
                        elif pos == 'right':
                            board.set_edge_state('v', row, col + 1, 1)
                            board.set_edge_state('v', row, col, 1)
                            board.set_edge_state('v', row, col + 2, 1)
                            board.set_edge_state('h', row, col + 1, 2)
                            board.set_edge_state('h', row + 1, col + 1, 2)

                diag_neighbors = [
                    (row - 1, col - 1, 'top_left'), (row - 1, col + 1, 'top_right'),
                    (row + 1, col - 1, 'bottom_left'), (row + 1, col + 1, 'bottom_right')
                ]

                for r_diag, c_diag, diag_pos in diag_neighbors:
                    if not board.valid_position(r_diag, c_diag):
                        continue
                    
                    value_diag = board.get_cell_value(r_diag, c_diag)

                    if value_diag == 0:
                        if diag_pos == 'top_left':
                            board.set_edge_state('v', row, col + 1, 1)
                            board.set_edge_state('h', row + 1, col, 1)
                        elif diag_pos == 'top_right':
                            board.set_edge_state('v', row, col, 1)
                            board.set_edge_state('h', row + 1, col, 1)
                        elif diag_pos == 'bottom_left':
                            board.set_edge_state('v', row, col + 1, 1)
                            board.set_edge_state('h', row, col, 1)
                        elif diag_pos == 'bottom_right':
                            board.set_edge_state('v', row, col, 1)
                            board.set_edge_state('h', row, col, 1)

                    elif value_diag == 3:
                        if diag_pos == 'top_left':
                            board.set_edge_state('v', row, col + 1, 1)
                            board.set_edge_state('h', row + 1, col, 1)
                            board.set_edge_state('h', row, col + 1, 2)
                            board.set_edge_state('v', row + 1, col + 1, 2)
                        elif diag_pos == 'top_right':
                            board.set_edge_state('v', row, col, 1)
                            board.set_edge_state('h', row + 1, col, 1)
                            board.set_edge_state('h', row, col - 1, 2)
                            board.set_edge_state('v', row + 1, col, 2)
                        elif diag_pos == 'bottom_left':
                            board.set_edge_state('v', row, col + 1, 1)
                            board.set_edge_state('h', row, col, 1)
                            board.set_edge_state('h', row + 1, col + 1, 2)
                            board.set_edge_state('v', row - 1, col + 1, 2)
                        elif diag_pos == 'bottom_right':
                            board.set_edge_state('v', row, col, 1)
                            board.set_edge_state('h', row, col, 1)
                            board.set_edge_state('h', row + 1, col - 1, 2)
                            board.set_edge_state('v', row - 1, col, 2)

    def actions(self, state: SlitherlinkState):
        board = state.board
        possible_edges = []
        
        for edge, edge_state in board.edges.items():
            if edge_state == 0:
                possible_edges.append(edge)
        
        # Ordenar: arestas adjacentes a células com constraints vêm primeiro
        def edge_priority(edge):
            edge_type, row, col = edge
            priority = 0
            
            # Células afetadas por esta aresta
            cells = []
            if edge_type == 'h':
                cells = [(row-1, col), (row, col)]
            else:
                cells = [(row, col-1), (row, col)]
            
            # Priorizar arestas de células com números altos (3, 2)
            for r, c in cells:
                if board.valid_position(r, c):
                    val = board.get_cell_value(r, c)
                    if val == 3: priority += 10
                    elif val == 2: priority += 5
                    elif val == 1: priority += 2
            
            return -priority  # Negativo para ordenação decrescente
        
        possible_edges.sort(key=edge_priority)
        return possible_edges

    def result(self, state: SlitherlinkState, action):
        board_copy = copy.deepcopy(state.board)
        edge_type, row, col = action
        board_copy.set_edge_state(edge_type, row, col, 1)
        
        # Verificar se viola constraints - prune o ramo imediatamente
        affected_cells = []
        if edge_type == 'h':
            affected_cells = [(row-1, col), (row, col)]
        else:  # 'v'
            affected_cells = [(row, col-1), (row, col)]
        
        for r, c in affected_cells:
            if board_copy.valid_position(r, c):
                active = board_copy.get_active_edges(r, c)
                value = board_copy.get_cell_value(r, c)
                if value != -1 and active > value:
                    return None  # Viola constraint - prune
        
        return SlitherlinkState(board_copy)
    
    def goal_test(self, state: SlitherlinkState):
        board = state.board 
        # Nenhuma aresta pode estar indefinida
        for edge_state in board.edges.values():
            if edge_state == 0:
                return False
               
        for row in range(board.rows):
            for col in range(board.columns):
                value = board.get_cell_value(row, col)
                if value == -1:
                    continue
                if board.get_active_edges(row, col) != value: 
                    return False
        return True

    def h(self, node: Node):
        # Heurística: contar arestas indefinidas (quanto menos, melhor)
        if node.state is None:
            return float('inf')  # Prune branches inválidas
        
        board = node.state.board
        undefined_edges = sum(1 for state in board.edges.values() if state == 0)
        return undefined_edges


if __name__ == "__main__":
    board = Board.parse_instance()
    problem = Slitherlink(board)
    
    problem.process_zeros(board)
    problem.process_corners(board)
    problem.process_threes(board)
    
    solution_node = astar_search(problem)
    
    if solution_node:
        solution_node.state.board.print_solution()