from queue import Queue


def edmonds_karp(residual_graph, source, sink):
    def create_path(parent, start, target):
        path = []
        current = target
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()
        return path

    def find_bottleneck(residual_graph, path):
        return min(residual_graph[path[i]][path[i + 1]] for i in range(len(path) - 1))

    def reduce_path(residual_graph, path, bottleneck):
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual_graph[u][v] -= bottleneck
            residual_graph[v][u] += bottleneck

    def bfs_to_target(graph, start, target):
        n = len(graph)
        visited: list[bool] = [False] * n
        parent = [None] * n
        queue = Queue()
        queue.put(start)
        visited[start] = True
        while not queue.empty():
            u = queue.get()
            for v in range(n):
                if graph[u][v] > 0 and not visited[v]:
                    parent[v] = u
                    if v == target:
                        return create_path(parent, start, target)
                    visited[v] = True
                    queue.put(v)
        return None

    max_flow = 0
    while (path := bfs_to_target(residual_graph, source, sink)) is not None:
        bottleneck = find_bottleneck(residual_graph, path)
        max_flow += bottleneck
        reduce_path(residual_graph, path, bottleneck)

    return max_flow


def copy_graph(graph):
    """Create a deep copy of the graph."""
    return [row[:] for row in graph]


def run_test(test_name, graph, source, sink, expected):
    """Run a single test case and print the result."""
    result = edmonds_karp(copy_graph(graph), source, sink)
    status = "✅" if result == expected else "❌"
    print(f"{test_name}: {result} (expected: {expected}) {status}")
    return result == expected


# Example of finding the maximum flow in a graph
if __name__ == "__main__":
    # Test 1: Simple path
    run_test(
        "Test 1 - Simple path",
        [
            [0, 5, 0],
            [0, 0, 4],
            [0, 0, 0],
        ],
        0,
        2,
        4,
    )

    # Test 2: Single edge
    run_test(
        "Test 2 - Single edge",
        [
            [0, 10],
            [0, 0],
        ],
        0,
        1,
        10,
    )

    # Test 3: No path
    run_test(
        "Test 3 - No path",
        [
            [0, 5, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        0,
        2,
        0,
    )

    # Test 4: Multiple paths
    run_test(
        "Test 4 - Multiple paths",
        [
            [0, 3, 2, 0],
            [0, 0, 0, 3],
            [0, 0, 0, 2],
            [0, 0, 0, 0],
        ],
        0,
        3,
        5,
    )

    # Test 5: Classic example
    run_test(
        "Test 5 - Classic example",
        [
            [0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0],
        ],
        0,
        5,
        23,
    )

    # Test 6: Bottleneck in middle
    run_test(
        "Test 6 - Bottleneck in middle",
        [
            [0, 10, 0, 0],
            [0, 0, 5, 0],
            [0, 0, 0, 10],
            [0, 0, 0, 0],
        ],
        0,
        3,
        5,
    )

    # Test 7: Parallel paths
    run_test(
        "Test 7 - Parallel paths",
        [
            [0, 5, 5, 0],
            [0, 0, 0, 5],
            [0, 0, 0, 5],
            [0, 0, 0, 0],
        ],
        0,
        3,
        10,
    )
