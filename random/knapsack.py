#!/usr/bin/python3
import random

# Control how many random tests are generated in addition to the hand-made ones.
generate_random_tests = True
random_tests = 12
max_items = 12
max_weight = 12
max_value = 25
# If seed is 0, a new set of random instances is generated every run.
seed = 1


# =====================================================================
# Student-facing solution function
# =====================================================================
def solve(weights: list[int], values: list[int], capacity: int):
    """
    Args:
        weights: Sequence of item weights.
        values: Sequence of item values (same length as weights).
        capacity: Maximum total weight allowed.

    Returns:
        Maximum achievable value. You may also return (value, chosen_items),
        where chosen_items can be a list of indices or a list of booleans.
    """
    return solve_memo(weights, values, capacity)
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n)]
    dp[0] = [0 if weights[0] > c else values[0] for c in range(capacity + 1)]

    for i in range(1, n):
        for c in range(capacity + 1):
            m = dp[i - 1][c]
            if weights[i] <= c:
                m = max(m, dp[i - 1][c - weights[i]] + values[i])
            dp[i][c] = m

    return dp[n - 1][capacity]


def solve_memo(weights, values, capacity):
    """Top-down 0/1 knapsack with memoization (i, remaining_capacity)."""
    n = len(weights)
    cap = max(0, capacity)
    memo: dict[tuple[int, int], int] = {}

    def dfs(i: int, c: int) -> int:
        if i == n or c == 0:
            return 0
        key = (i, c)
        if key in memo:
            return memo[key]

        best = dfs(i + 1, c)  # skip item i
        if weights[i] <= c:
            best = max(best, values[i] + dfs(i + 1, c - weights[i]))

        memo[key] = best
        return best

    return dfs(0, cap)


# =====================================================================
# Reference / utility implementations
# =====================================================================
def solve_bottom_up(
    weights: list[int], values: list[int], capacity: int
) -> tuple[int, list[int]]:
    """Bottom-up DP that also reconstructs one optimal item set."""
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")
    n = len(weights)
    cap = max(0, capacity)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(cap + 1):
            if w > c:
                dp[i][c] = dp[i - 1][c]
            else:
                dp[i][c] = max(dp[i - 1][c], v + dp[i - 1][c - w])

    # Reconstruct one optimal choice of item indices.
    chosen: list[int] = []
    c = cap
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(i - 1)
            c -= weights[i - 1]
    chosen.reverse()
    return dp[n][cap], chosen


def _reference_knapsack(
    weights: list[int], values: list[int], capacity: int
) -> tuple[int, list[int]]:
    """Alias to the tabulation solver, used as ground truth in tests."""
    return solve_bottom_up(weights, values, capacity)


# =====================================================================
# Test helpers
# =====================================================================
def _extract_answer(student_answer):
    """
    Accept either:
    - int (only the best value)
    - (value, chosen) where chosen is a list of indices or booleans
    """
    if isinstance(student_answer, int):
        return student_answer, None, None

    if isinstance(student_answer, (list, tuple)):
        if not student_answer:
            return None, None, "Empty list/tuple is not a valid return value."
        value = student_answer[0]
        chosen = student_answer[1] if len(student_answer) > 1 else None
        return value, chosen, None

    return None, None, f"Unsupported return type: {type(student_answer).__name__}"


def _validate_choice(
    chosen, weights: list[int], values: list[int], capacity: int
) -> tuple[int | None, int | None, str | None]:
    """
    Validate a chosen-item description.

    Supports:
        - List/tuple of booleans (length == n)
        - List/tuple of indices (0-based)
    """
    if chosen is None:
        return None, None, None

    n = len(weights)

    # Boolean mask
    if isinstance(chosen, (list, tuple)) and all(isinstance(x, bool) for x in chosen):
        if len(chosen) != n:
            return None, None, "Boolean mask must match number of items."
        indices = [i for i, take in enumerate(chosen) if take]
    # Indices
    elif isinstance(chosen, (list, tuple)) and all(isinstance(x, int) for x in chosen):
        indices = list(chosen)
    else:
        return None, None, "Chosen items must be booleans or indices."

    if len(indices) != len(set(indices)):
        return None, None, "Duplicate indices detected; 0/1 knapsack allows each once."
    if any(i < 0 or i >= n for i in indices):
        return None, None, "Index out of bounds in chosen items."

    total_weight = sum(weights[i] for i in indices)
    total_value = sum(values[i] for i in indices)

    if total_weight > capacity:
        return total_weight, total_value, "Chosen items exceed capacity."

    return total_weight, total_value, None


def _format_instance(weights, values, capacity):
    return f"weights : {weights}\nvalues  : {values}\ncapacity: {capacity}"


# =====================================================================
# Hand-made and random tests
# =====================================================================
tests = [
    ([2, 3, 4, 5], [3, 4, 5, 6], 5, 7, "Simple mix"),
    ([1, 2, 3], [6, 10, 12], 5, 22, "Take 2+3"),
    ([10, 20, 30], [60, 100, 120], 50, 220, "Greedy would fail"),
    ([5, 4, 6, 3], [10, 40, 30, 50], 10, 90, "Pick 4+3"),
    ([2, 2, 2, 2], [5, 5, 5, 5], 4, 10, "Duplicates"),
    ([1], [10], 1, 10, "Single item fits"),
    ([1, 2], [1, 2], 1, 1, "Single capacity"),
    ([3, 4, 5], [30, 50, 60], 8, 90, "Classic example"),
    ([1, 3, 4, 5], [1, 4, 5, 7], 7, 9, "Multiple ways"),
    ([2, 3, 4, 5], [3, 4, 5, 6], 0, 0, "Zero capacity"),
]


def _generate_random_test():
    if seed != 0:
        random.seed(seed)

    n = random.randint(1, max_items)
    weights = [random.randint(1, max_weight) for _ in range(n)]
    values = [random.randint(1, max_value) for _ in range(n)]
    capacity = random.randint(0, sum(weights) // 2 + 1)
    best_value, best_choice = _reference_knapsack(weights, values, capacity)
    return weights, values, capacity, best_value, best_choice, f"Random test (n={n})"


# =====================================================================
# Test runner
# =====================================================================
def _run_tests():
    failed = False
    all_tests = []

    # Validate hand-made tests against the reference solver.
    for w, v, c, expected, description in tests:
        ref_value, ref_choice = _reference_knapsack(w, v, c)
        assert (
            ref_value == expected
        ), f"Hand-made test '{description}' has wrong expected value."
        all_tests.append((w, v, c, expected, ref_choice, description))

    # Add random instances
    if generate_random_tests:
        for _ in range(random_tests):
            all_tests.append(_generate_random_test())

    for i, (w, v, c, expected, ref_choice, description) in enumerate(all_tests, 1):
        try:
            student_answer = solve(w, v, c)
        except NotImplementedError:
            print("You need to implement solve() before running the tests.")
            return
        except Exception as e:
            failed = True
            print(f"Test {i} crashed: {description}")
            print(_format_instance(w, v, c))
            print(f"Raised exception: {e}")
            print("-" * 60)
            continue

        value, chosen, parse_error = _extract_answer(student_answer)
        if parse_error:
            failed = True
            print(f"Test {i} failed ({description})")
            print(_format_instance(w, v, c))
            print(f"Your answer: {student_answer}")
            print(f"Reason: {parse_error}")
            print("-" * 60)
            continue

        if not isinstance(value, int):
            failed = True
            print(f"Test {i} failed ({description})")
            print("The first element you return must be an int (the best value).")
            print("-" * 60)
            continue

        total_w, total_v, choice_error = _validate_choice(chosen, w, v, c)
        if choice_error:
            failed = True
            print(f"Test {i} failed ({description})")
            print(_format_instance(w, v, c))
            print(f"Your answer: {student_answer}")
            print(f"Reason: {choice_error}")
            print("-" * 60)
            continue

        if value != expected:
            failed = True
            print(f"Test {i} failed ({description})")
            print(_format_instance(w, v, c))
            print(f"Your answer value: {value}")
            if total_w is not None:
                print(f"Your chosen weight/value: {total_w}/{total_v}")
            print(f"Expected best value: {expected}")
            print(f"One optimal choice (indices): {ref_choice}")
            print("-" * 60)

    if not failed:
        print(f"All {len(all_tests)} tests passed! ✓")


if __name__ == "__main__":
    _run_tests()
