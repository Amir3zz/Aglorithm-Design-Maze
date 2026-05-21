from collections import deque
from typing import Dict, List

from main import (
    MazeGraph,
    read_maze_from_stdin,
    build_graph,
    print_maze,
)


def bfs_shortest_path(graph: MazeGraph) -> tuple[List[int], Dict[int, int], Dict[int, int | None]]:

    if graph.start is None or graph.goal is None:
        return [], {}, {}

    start_vertex = graph.cell_to_vertex[graph.start]
    goal_vertex = graph.cell_to_vertex[graph.goal]

    # Queue implementation using deque
    queue = deque()

    # Visited vertices
    visited = set()

    # Distance tracking
    distance: Dict[int, int] = {}

    # Parent tracking
    parent: Dict[int, int | None] = {}

    # Initialize BFS
    visited.add(start_vertex)

    distance[start_vertex] = 0

    parent[start_vertex] = None

    queue.append(start_vertex)

    # BFS traversal
    while queue:

        current = queue.popleft()

        if current == goal_vertex:
            break

        for neighbor in graph.adjacency_list[current]:

            if neighbor not in visited:

                visited.add(neighbor)

                distance[neighbor] = distance[current] + 1

                parent[neighbor] = current

                queue.append(neighbor)

    # Shortest path reconstruction
    path: List[int] = []

    if goal_vertex not in parent:
        return [], distance, parent

    current = goal_vertex

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path, distance, parent


def mark_path_on_maze(
    graph: MazeGraph,
    path: List[int]
) -> List[List[str]]:

    maze_copy = [row[:] for row in graph.maze]

    for vertex in path:

        r, c = graph.vertex_to_cell[vertex]

        if maze_copy[r][c] not in {"S", "G"}:
            maze_copy[r][c] = "*"

    return maze_copy


def main() -> None:

    maze, rows, cols = read_maze_from_stdin()

    graph = build_graph(maze, rows, cols)

    print("Original Maze:")
    print_maze(graph.maze)

    print()

    path, distance, parent = bfs_shortest_path(graph)

    print("Output Produced by Student 2")
    print("-----------------------------------")

    # BFS function
    print("1. BFS Function")
    print("BFS implemented using queue-based traversal.")
    print()

    # Queue implementation
    print("2. Queue Implementation or Library Usage")
    print("Queue used: collections.deque")
    print()

    # Distance tracking
    print("3. Distance Tracking")

    for vertex in sorted(distance):
        print(f"Vertex {vertex}: Distance = {distance[vertex]}")

    print()

    # Parent tracking
    print("4. Parent Tracking")

    for vertex in sorted(parent):

        print(f"Vertex {vertex}: Parent = {parent[vertex]}")

    print()

    # Shortest path reconstruction
    print("5. Shortest Path Reconstruction")

    if path:

        print("Shortest Path (Vertex IDs):")
        print(" -> ".join(map(str, path)))

        print()

        path_maze = mark_path_on_maze(graph, path)

        print("Maze with Shortest Path:")
        print_maze(path_maze)

    else:
        print("No path found from S to G.")

    print()

    # BFS correctness explanation
    print("6. BFS Correctness Explanation")
    print(
        "BFS explores the maze level by level using a queue. "
        "Because each edge has equal weight, the first time the goal "
        "vertex is reached guarantees the shortest path. "
        "The parent dictionary reconstructs the path from goal back to start."
    )


if __name__ == "__main__":
    main()