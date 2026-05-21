from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple
import sys


@dataclass(frozen=True)
class MazeGraph:
    maze: List[List[str]]
    rows: int
    cols: int
    start: Tuple[int, int] | None
    goal: Tuple[int, int] | None
    cell_to_vertex: Dict[Tuple[int, int], int]
    vertex_to_cell: Dict[int, Tuple[int, int]]
    adjacency_list: Dict[int, List[int]]
    adjacency_matrix: List[List[int]]


def read_maze_from_stdin() -> Tuple[List[List[str]], int, int]:
    """
    Reads a maze from standard input.
    Returns:
        maze grid, rows, cols
    """
    first_line = sys.stdin.readline().strip()
    while first_line == "":
        first_line = sys.stdin.readline().strip()

    try:
        rows, cols = map(int, first_line.split())
    except ValueError as exc:
        raise ValueError("First line must contain two integers: rows cols") from exc

    maze: List[List[str]] = []
    for _ in range(rows):
        line = sys.stdin.readline().rstrip("\n")
        if len(line) != cols:
            raise ValueError(
                f"Each maze row must have exactly {cols} characters. "
                f"Got '{line}' with length {len(line)}."
            )
        maze.append(list(line))

    return maze, rows, cols


def is_open_cell(ch: str) -> bool:
    return ch in {".", "S", "G"}


def build_graph(maze: List[List[str]], rows: int, cols: int) -> MazeGraph:
    """
    Converts the maze into a graph where each non-wall cell becomes a vertex.
    """
    cell_to_vertex: Dict[Tuple[int, int], int] = {}
    vertex_to_cell: Dict[int, Tuple[int, int]] = {}
    start = None
    goal = None

    # Assign vertex IDs to all open cells.
    vertex_id = 0
    for r in range(rows):
        for c in range(cols):
            if is_open_cell(maze[r][c]):
                cell_to_vertex[(r, c)] = vertex_id
                vertex_to_cell[vertex_id] = (r, c)
                if maze[r][c] == "S":
                    start = (r, c)
                elif maze[r][c] == "G":
                    goal = (r, c)
                vertex_id += 1

    v_count = len(cell_to_vertex)
    adjacency_list: Dict[int, List[int]] = {v: [] for v in range(v_count)}
    adjacency_matrix: List[List[int]] = [[0] * v_count for _ in range(v_count)]

    # 4-direction movement: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for (r, c), v in cell_to_vertex.items():
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (nr, nc) in cell_to_vertex:
                u = cell_to_vertex[(nr, nc)]

                # Undirected graph: connect both ways.
                if u not in adjacency_list[v]:
                    adjacency_list[v].append(u)
                if v not in adjacency_list[u]:
                    adjacency_list[u].append(v)

                adjacency_matrix[v][u] = 1
                adjacency_matrix[u][v] = 1

    # Keep adjacency list output stable and easy to read.
    for v in adjacency_list:
        adjacency_list[v].sort()

    return MazeGraph(
        maze=maze,
        rows=rows,
        cols=cols,
        start=start,
        goal=goal,
        cell_to_vertex=cell_to_vertex,
        vertex_to_cell=vertex_to_cell,
        adjacency_list=adjacency_list,
        adjacency_matrix=adjacency_matrix,
    )


def print_maze(maze: List[List[str]]) -> None:
    for row in maze:
        print("".join(row))


def print_adjacency_list(adjacency_list: Dict[int, List[int]]) -> None:
    print("Adjacency List:")
    for v in sorted(adjacency_list):
        neighbors = ", ".join(map(str, adjacency_list[v]))
        print(f"{v}: {neighbors}" if neighbors else f"{v}:")
    print()


def print_adjacency_matrix(adjacency_matrix: List[List[int]]) -> None:
    print("Adjacency Matrix:")
    for row in adjacency_matrix:
        print(" ".join(map(str, row)))
    print()


def print_cell_vertex_mapping(graph: MazeGraph) -> None:
    print("Cell to Vertex Mapping:")
    for (r, c), v in sorted(graph.cell_to_vertex.items(), key=lambda x: x[1]):
        print(f"cell({r}, {c}) -> vertex {v}")
    print()

    print("Vertex to Cell Mapping:")
    for v, (r, c) in sorted(graph.vertex_to_cell.items()):
        print(f"vertex {v} -> cell({r}, {c})")
    print()


def main() -> None:
    maze, rows, cols = read_maze_from_stdin()
    graph = build_graph(maze, rows, cols)

    print("Original Maze:")
    print_maze(graph.maze)
    print()

    if graph.start is None or graph.goal is None:
        print("Warning: maze should contain exactly one S and one G.")
        print()

    print_cell_vertex_mapping(graph)
    print_adjacency_list(graph.adjacency_list)
    print_adjacency_matrix(graph.adjacency_matrix)


if __name__ == "__main__":
    main()
