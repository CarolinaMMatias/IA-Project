#!/usr/bin/env python3
# slitherlink.py: Template para implementação do projeto de Inteligência Artificial 2025/2026.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Slitherlink."""

    def __init__(self, grid: list):
        """Inicializa o tabuleiro com a grelha de restrições.
        
        Args:
            grid: Lista de listas com as restrições (0, 1, 2, 3, ou '.')
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        
        # Estado das arestas: None=desconhecida, True=ativa, False=inativa
        # Arestas horizontais: (rows+1) x cols
        self.h_edges = [[None] * self.cols for _ in range(self.rows + 1)]
        # Arestas verticais: rows x (cols+1)
        self.v_edges = [[None] * (self.cols + 1) for _ in range(self.rows)]

    def adjacent_cell(self, cell: tuple) -> list:
        """Devolve uma lista das células que fazem
        fronteira com a célula enviada no argumento"""
        row, col = cell
        adjacent = []
        
        # Cima
        if row > 0:
            adjacent.append((row - 1, col))
        # Baixo
        if row < self.rows - 1:
            adjacent.append((row + 1, col))
        # Esquerda
        if col > 0:
            adjacent.append((row, col - 1))
        # Direita
        if col < self.cols - 1:
            adjacent.append((row, col + 1))
        
        return adjacent

    def get_cell_edges(self, row: int, column: int) -> list:
        """Devolve as arestas da célula enviada no argumento.
        
        Cada aresta é representada como uma tupla (tipo, row, col) onde:
        - tipo: 'h' (horizontal) ou 'v' (vertical)
        - row, col: coordenadas da aresta
        """
        edges = []
        
        # Aresta superior (horizontal)
        edges.append(('h', row, column))
        
        # Aresta inferior (horizontal)
        edges.append(('h', row + 1, column))
        
        # Aresta esquerda (vertical)
        edges.append(('v', row, column))
        
        # Aresta direita (vertical)
        edges.append(('v', row, column + 1))
        
        return edges

    def get_active_edges(self, row: int, column: int) -> int:
        """Devolve o número de arestas ativas da célula"""
        count = 0
        edges = self.get_cell_edges(row, column)
        
        for edge_type, edge_row, edge_col in edges:
            if edge_type == 'h':
                if self.h_edges[edge_row][edge_col] is True:
                    count += 1
            else:  # 'v'
                if self.v_edges[edge_row][edge_col] is True:
                    count += 1
        
        return count

    def get_inactive_edges(self, row: int, column: int) -> int:
        """Devolve o número de arestas inativas (marcadas como False) da célula"""
        count = 0
        edges = self.get_cell_edges(row, column)
        
        for edge_type, edge_row, edge_col in edges:
            if edge_type == 'h':
                if self.h_edges[edge_row][edge_col] is False:
                    count += 1
            else:  # 'v'
                if self.v_edges[edge_row][edge_col] is False:
                    count += 1
        
        return count

    def get_cell_constraint(self, row: int, column: int):
        """Devolve o valor da restrição da célula (0, 1, 2, 3, ou '.')"""
        return self.grid[row][column]

    def print_instance(self) -> str:
        """Imprime a grelha no formato de output especificado na secção 4.2"""
        result = []
        
        for row in range(self.rows):
            row_str = []
            for col in range(self.cols):
                # Cada célula é representada por 4 dígitos: top, right, bottom, left
                top = '1' if self.h_edges[row][col] is True else '0'
                right = '1' if self.v_edges[row][col + 1] is True else '0'
                bottom = '1' if self.h_edges[row + 1][col] is True else '0'
                left = '1' if self.v_edges[row][col] is True else '0'
                
                cell_str = top + right + bottom + left
                row_str.append(cell_str)
            
            result.append(' '.join(row_str))
        
        return '\n'.join(result)

    @staticmethod
    def parse_instance():
        """Lê a instância do standard input (stdin) e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 slitherlink.py < test-01.txt
        """
        grid = []
        
        # Lê todas as linhas do stdin
        for line in stdin:
            line = line.strip()
            if line:  # Ignora linhas vazias
                # Divide por tabs ou espaços
                row = line.split()
                # Converte valores numéricos para int, mantém '.'
                converted_row = []
                for val in row:
                    if val == '.':
                        converted_row.append('.')
                    else:
                        converted_row.append(int(val))
                grid.append(converted_row)
        
        return Board(grid)

    # TODO: outros metodos da classe

class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        """O construtor especifica o estado inicial."""
        # TODO
        pass


    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass


    def result(self, state: SlitherlinkState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: SlitherlinkState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass







