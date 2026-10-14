# Slitherlink Solver — Artificial Intelligence

Project developed for the **Inteligência Artificial** (Artificial Intelligence) course at **Instituto Superior Técnico (IST)**.

---

## 🧩 About the Project

An automated solver for the Japanese logic puzzle **Slitherlink** (Surizarinku) developed in **Python**, utilizing classical AI search algorithms and heuristic techniques.

### 🎯 Puzzle Rules:
* Connect adjacent dots on a rectangular grid to form a **single continuous closed loop** with no branches or self-intersections.
* Numerical clues ($0, 1, 2, 3$) specify exactly how many of that cell's four edges are part of the loop.
* Cells marked with `.` have no clue and can be surrounded by any valid number of edges.

---

## ⚙️ Implementation & AI Search

* **Problem Formulation**: Modeled as a state-space search problem based on the AIMA framework (`search.py`):
  * **State (`SlytherlinkState`)**: Grid status tracking active and inactive horizontal/vertical edges.
  * **Actions & Transitions**: Dynamically generating valid edge placements while respecting local grid constraints.
  * **Goal Test**: Verifies that all numeric constraints are satisfied and edges form a single closed cycle.
* **Search Algorithms**:
  * Uninformed Search: Depth-First Search (DFS) and Breadth-First Search (BFS).
  * Informed Search: Greedy Search and **A\* Search** guided by custom heuristics ($h$) to minimize search space.
* **Visualization (GUI)**: Optional interactive interface built with `tkinter` (`slitherlink_gui.py`) for step-by-step debug and display.

---

## 💻 Tech Stack
* **Python 3.11**
* **NumPy**
* **AIMA Search Framework**
