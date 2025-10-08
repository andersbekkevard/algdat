def find_path(weights):
    # assembling pieces
    n = len(weights)
    if n == 0:
        return []
    m = len(weights[0])
    if m == 0:
        return []
    elif n == 1:
        return [(weights[0].index(min(weights[0])), 0)]
    elif m == 1:
        path = []
        for i in range(n):
            path.append((0, i))
        return path

    memo = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(m):
        memo[0][i] = weights[0][i]

    # finding cumulative path length for each position
    for i in range(1, n):
        for j in range(m):
            path = memo[i - 1][j]
            if j != 0:
                path = min(path, memo[i - 1][j - 1])
            if j != m - 1:
                path = min(path, memo[i - 1][j + 1])
            memo[i][j] = weights[i][j] + path

    # building the path (O(n))
    path = []
    j = memo[n - 1].index(min(memo[n - 1]))
    path.append((j, n - 1))
    for i in range(n - 2, -1, -1):
        candidates = [(j, memo[i][j])]
        if j > 0:
            candidates.append((j - 1, memo[i][j - 1]))
        if j < m - 1:
            candidates.append((j + 1, memo[i][j + 1]))
        j = min(candidates, key=lambda x: x[1])[0]
        path.append((j, i))
    path.reverse()
    return path


def find_min_iterative(weights):
    n = len(weights)
    m = len(weights[0])
    memo = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(m):
        memo[0][i] = weights[0][i]

    for i in range(1, n):
        for j in range(m):
            path = memo[i - 1][j]
            if j != 0:
                path = min(path, memo[i - 1][j - 1])
            if j != m - 1:
                path = min(path, memo[i - 1][j + 1])
            memo[i][j] = weights[i][j] + path

    return min(memo[n - 1])


def test_find_min(find_min):
    errors = []

    def check(weights, expected, name):
        result = find_min(weights)
        if result != expected:
            errors.append(f"{name} failed: expected {expected}, got {result}")

    # Base and simple cases
    check([[5]], 5, "Test 1 - single element")
    check([[3, 1, 4]], 1, "Test 2 - single row")
    check([[1], [2], [3]], 6, "Test 3 - single column")

    # Basic structure tests
    check([[2, 1, 3], [6, 5, 4], [7, 8, 9]], 13, "Test 4 - small 3x3")
    check([[1, 2, 3], [4, 1, 6], [7, 8, 1]], 3, "Test 5 - diagonal path")
    check(
        [[10, 2, 8, 5], [6, 1, 3, 7], [4, 9, 2, 1], [5, 6, 7, 2]],
        7,
        "Test 6 - larger grid",
    )

    # Edge and corner cases
    check([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, "Test 7 - all zeros")
    check([[5, 5, 5], [5, 5, 5], [5, 5, 5]], 15, "Test 8 - all equal")
    check([[1, 2], [3, 4]], 4, "Test 9 - small 2x2")
    check([[9, 1], [1, 9], [9, 1]], 3, "Test 10 - zigzag minimum")

    # Wider grid
    check(
        [
            [1, 9, 9, 9, 9],
            [9, 1, 9, 9, 9],
            [9, 9, 1, 9, 9],
            [9, 9, 9, 1, 9],
            [9, 9, 9, 9, 1],
        ],
        5,
        "Test 13 - diagonal through wide grid",
    )

    # Random uneven landscape
    check(
        [[5, 3, 1, 9], [4, 8, 2, 3], [7, 1, 5, 6], [9, 2, 8, 1]],
        6,
        "Test 14 - mixed terrain",
    )

    # Large flat plateau with one valley
    check(
        [[10, 10, 10, 10], [10, 1, 10, 10], [10, 10, 10, 10], [10, 10, 10, 10]],
        31,
        "Test 15 - single valley",
    )

    if errors:
        for e in errors:
            print(e)
    else:
        print("all tests passed")


def run_tests():
    errors = []

    # 1. empty input
    if find_path([]) != []:
        errors.append("empty list failed")
    if find_path([[]]) != []:
        errors.append("empty row failed")

    # 2. single row
    w = [[5, 2, 8, 1]]
    if find_path(w) != [(3, 0)]:
        errors.append("single row failed")

    # 3. single column
    w = [[3], [1], [4], [2]]
    expected = [(0, 0), (0, 1), (0, 2), (0, 3)]
    if find_path(w) != expected:
        errors.append("single column failed")

    # 4. small square
    w = [[1, 2, 3], [4, 8, 2], [1, 5, 3]]
    expected = [(0, 0), (1, 1), (2, 2)]
    if find_path(w) != expected:
        errors.append("small square failed")

    # 5. all equal
    w = [[1, 1], [1, 1], [1, 1]]
    p = find_path(w)
    if len(p) != 3 or not all(0 <= x <= 1 for x, _ in p):
        errors.append("all equal failed")

    # 6. non-square
    w = [[4, 3, 1], [2, 1, 3], [3, 2, 1], [5, 4, 2]]
    expected = [(2, 0), (1, 1), (2, 2), (2, 3)]
    if find_path(w) != expected:
        errors.append("non-square failed")

    # 7. diagonal bias
    w = [[1, 9, 9], [9, 1, 9], [9, 9, 1]]
    expected = [(0, 0), (1, 1), (2, 2)]
    if find_path(w) != expected:
        errors.append("diagonal bias failed")

    # 8. random sanity check
    import random

    random.seed(0)
    w = [[random.randint(1, 9) for _ in range(10)] for _ in range(10)]
    p = find_path(w)
    if len(p) != 10:
        errors.append("random length failed")
    for i in range(1, len(p)):
        if abs(p[i][0] - p[i - 1][0]) > 1:
            errors.append("random invalid step")
            break

    if errors:
        for e in errors:
            print("Error:", e)
    else:
        print("all successful")


# Run the suite
# test_find_min(find_min_iterative)
run_tests()
