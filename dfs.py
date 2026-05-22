# ==========================================
# TASK 4 - DFS FOR PATH FINDING
# ==========================================

# Sample maze
maze = [
    "############",
    "#S...#.....#",
    "#.#.#.#.##.#",
    "#.#...#....#",
    "#.#####.####",
    "#.....#....#",
    "###.#.####.#",
    "#...#......#",
    "#.#######G##",
    "############"
]

rows = len(maze)
cols = len(maze[0])

# Convert maze into mutable list
maze_grid = [list(row) for row in maze]

# Directions: UP, DOWN, LEFT, RIGHT
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Find Start and Goal positions
start = None
goal = None

for r in range(rows):
    for c in range(cols):
        if maze_grid[r][c] == 'S':
            start = (r, c)
        elif maze_grid[r][c] == 'G':
            goal = (r, c)


# ==========================================
# DFS FUNCTION
# ==========================================

def dfs(maze, start, goal):
    stack = [start]
    visited = set()
    parent = {}

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        # Goal found
        if current == goal:
            break

        r, c = current

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc

            # Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:

                # Ignore walls
                if maze[nr][nc] != '#':
                    neighbor = (nr, nc)

                    if neighbor not in visited:
                        parent[neighbor] = current
                        stack.append(neighbor)

    # Reconstruct path
    path = []

    if goal in visited:
        current = goal

        while current != start:
            path.append(current)
            current = parent[current]

        path.append(start)
        path.reverse()

    return path

def print_dfs_explanation():
    print("Explanation of DFS:")
    print(
        "DFS (Depth-First Search) explores one path completely before trying "
        "another path. The algorithm uses a stack data structure. First, the "
        "start node is pushed into the stack. A node is then popped from the "
        "stack and marked as visited. All unvisited neighboring nodes are "
        "pushed into the stack. This process repeats until the goal is found "
        "or the stack becomes empty. DFS does not guarantee the shortest path "
        "because it explores deeply along one branch before checking others."
    )


def print_time_complexity_analysis():
    print("Time Complexity Analysis:")
    print(
        "For DFS, V represents the number of vertices (open cells) and E "
        "represents the number of edges (connections between cells). "
        "The time complexity of DFS is O(V + E) because each vertex and edge "
        "is visited at most once during traversal. "
        "The space complexity is O(V) because the stack and visited set may "
        "store up to all vertices in the worst case."
    )


def print_bfs_vs_dfs_comparison():
    print("BFS vs DFS Comparison:")
    print(
        "BFS uses a Queue while DFS uses a Stack. "
        "BFS explores level-by-level and guarantees the shortest path in an "
        "unweighted graph. DFS explores deeply first and does not guarantee "
        "the shortest path. BFS is more suitable for shortest path problems, "
        "while DFS is useful for general path exploration. "
        "Both BFS and DFS have a time complexity of O(V + E)."
    )

# ==========================================
# RUN DFS
# ==========================================

path = dfs(maze_grid, start, goal)


# ==========================================
# DISPLAY RESULT
# ==========================================

if path:
    for r, c in path:
        if maze_grid[r][c] not in ['S', 'G']:
            maze_grid[r][c] = '*'

    print("DFS Path Found:\n")

    for row in maze_grid:
        print("".join(row))

    print(f"\nDFS Path Length: {len(path) - 1} moves")

else:
    print("No path found using DFS.")

print_dfs_explanation()
print()

print_time_complexity_analysis()
print()

print_bfs_vs_dfs_comparison()