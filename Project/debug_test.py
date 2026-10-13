#!/usr/bin/python3
import copy
from collections import defaultdict
from Slitherlink import Board, Slitherlink, SlitherlinkState
from search import depth_first_tree_search

# Criar um tabuleiro simples manualmente
grid = [
    [0, -1, 2, -1],
    [-1, -1, 0, -1],
    [-1, 0, -1, -1],
    [-1, 3, -1, 0]
]

board = Board(grid)
print("Grid loaded:", board.grid)
print("Rows:", board.rows, "Cols:", board.columns)
print("Edges count:", len(board.edges))

problem = Slitherlink(board)
initial_state = problem.initial

# Test goal_test on empty board
print("\nTesting goal_test on initial state (should be False):")
print("Result:", problem.goal_test(initial_state))

# Test actions
print("\nTesting actions on initial state:")
actions = problem.actions(initial_state)
print(f"Number of possible actions: {len(actions)}")
if actions:
    print(f"First few actions: {actions[:5]}")

# Test result
if actions:
    print("\nTesting result after first action:")
    state1 = problem.result(initial_state, actions[0])
    print(f"New state created. Board edges changed: {state1.board.edges != initial_state.board.edges}")
    
    # Check if propagation worked
    print(f"Active edges in initial: {sum(1 for e in initial_state.board.edges.values() if e == 1)}")
    print(f"Active edges after action: {sum(1 for e in state1.board.edges.values() if e == 1)}")

print("\n" + "="*50)
print("Starting search (with timeout awareness)...")
print("="*50)

solution_node = depth_first_tree_search(problem)

if solution_node:
    print("\nSOLUTION FOUND!")
    print(solution_node.state.board.print_board())
else:
    print("\nNO SOLUTION FOUND")
