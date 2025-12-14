#!/usr/bin/python3
import random

# =====================================================================
# Test configuration
# =====================================================================
generate_random_tests = True
random_tests = 12
max_boxes = 8
max_dim = 12
# If seed is 0, a new random set is produced every run.
seed = 1


# =====================================================================
# Student-facing solution (implement this)
# =====================================================================
def solve(boxes):
    """
    Compute the maximum possible stack height.

    Args:
        boxes: Iterable of (L, W, H) triples with positive numbers.

    Returns:
        Either:
          - int height
          - (height, stack) where stack is a list of boxes from bottom to top
    """
    # Ingen bokser → høyde 0
    if not boxes:
        return 0

    # Ingen rotasjoner er tillatt; bruk boksene som de er
    n = len(boxes)

    # Bygg graf hvor (i, j) er kant hvis L_i > L_j og W_i > W_j (Theta(n^2))
    adj = [[] for _ in range(n)]
    for i in range(n):
        Li, Wi, _ = boxes[i]
        for j in range(n):
            if i == j:
                continue
            Lj, Wj, _ = boxes[j]
            if Li > Lj and Wi > Wj:
                adj[i].append(j)

    # Topologisk sort med DFS (Theta(n^2) for tett graf)
    order = []
    state = [0] * n  # 0 = uoppdaget, 1 = på stakken, 2 = ferdig

    def dfs(u: int):
        state[u] = 1
        for v in adj[u]:
            if state[v] == 0:
                dfs(v)
        state[u] = 2
        order.append(u)

    for i in range(n):
        if state[i] == 0:
            dfs(i)

    topo = reversed(order)  # ferdig-listen gir reversert topologisk rekkefølge

    # Lag en array h der h[i] er optimal høyde med boks i på toppen (Theta(n))
    h = [b[2] for b in boxes]
    best = max(h)

    # For hver ut-kant (i, j), sett h[j] = max(h[j], h[i] + H_j) (Theta(V+E))
    for u in topo:
        for v in adj[u]:
            cand = h[u] + boxes[v][2]
            if cand > h[v]:
                h[v] = cand
                # Hold alltid styr på max h
                if h[v] > best:
                    best = h[v]

    # Returner
    return best


# =====================================================================
# Reference solver (used only to generate/validate tests)
# =====================================================================
def _reference_height(boxes):
    """Referanse uten rotasjoner (samme graf-DP som studentløsningen)."""
    B = [tuple(b) for b in boxes]
    n = len(B)
    if n == 0:
        return 0

    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and B[i][0] > B[j][0] and B[i][1] > B[j][1]:
                adj[i].append(j)

    order = []
    state = [0] * n

    def dfs(u):
        state[u] = 1
        for v in adj[u]:
            if state[v] == 0:
                dfs(v)
        state[u] = 2
        order.append(u)

    for i in range(n):
        if state[i] == 0:
            dfs(i)

    topo = reversed(order)
    h = [b[2] for b in B]
    best = max(h)

    for u in topo:
        for v in adj[u]:
            cand = h[u] + B[v][2]
            if cand > h[v]:
                h[v] = cand
                if h[v] > best:
                    best = h[v]

    return best


# =====================================================================
# Helpers for feedback
# =====================================================================
def _extract_answer(student_answer):
    if isinstance(student_answer, int):
        return student_answer, None, None
    if isinstance(student_answer, (list, tuple)):
        if not student_answer:
            return None, None, "Empty list/tuple is not a valid return value."
        first = student_answer[0]
        height = first if isinstance(first, int) else None
        stack = student_answer[1] if len(student_answer) > 1 else None
        if height is None:
            try:
                height = int(first)
            except Exception:
                return None, None, "Could not interpret first element as height."
        return height, stack, None
    return None, None, f"Unsupported return type {type(student_answer).__name__}"


def _is_valid_stack(stack):
    """Check strictly decreasing L and W bottom-to-top."""
    try:
        boxes = [tuple(b) for b in stack]
    except Exception:
        return False
    for b in boxes:
        if len(b) != 3:
            return False
        if b[0] <= 0 or b[1] <= 0 or b[2] <= 0:
            return False
    for i in range(1, len(boxes)):
        if not (boxes[i][0] < boxes[i - 1][0] and boxes[i][1] < boxes[i - 1][1]):
            return False
    return True


def _stack_height(stack):
    try:
        return sum(tuple(b)[2] for b in stack)
    except Exception:
        return None


def get_feedback(student_answer, expected_height, boxes, example_height):
    height, stack, parse_error = _extract_answer(student_answer)
    if parse_error:
        return parse_error

    if not isinstance(height, int):
        return f"Height must be an int, got {type(height).__name__}"

    if stack is not None:
        if not _is_valid_stack(stack):
            return "Provided stack is not strictly decreasing in (L, W) or contains invalid boxes."
        sh = _stack_height(stack)
        if sh is None:
            return "Could not compute the height of your stack."
        if sh != height:
            return f"Stack height {sh} does not match returned height {height}."

    if height != expected_height:
        return f"Returned height {height}, but optimal height is {expected_height} (example {example_height})."

    return None


def _format_instance(boxes):
    return "boxes: " + ", ".join(f"({l},{w},{h})" for l, w, h in boxes)


# =====================================================================
# Hand-made tests
# =====================================================================
tests = [
    ([], 0, "No boxes"),
    ([(3, 2, 5)], 5, "Single box"),
    ([(3, 2, 5), (4, 3, 1)], 6, "Two boxes stackable"),
    ([(3, 3, 3), (2, 2, 10)], 13, "Only width/length decreasing matters"),
    ([(1, 2, 3), (2, 3, 4)], 7, "Stacking uten rotasjon"),
    ([(4, 6, 7), (1, 2, 3), (4, 5, 6), (10, 12, 32)], 42, "Kjede uten rotasjoner"),
    ([(5, 5, 1), (4, 4, 10)], 11, "Direkte stacking uten rotasjon"),
]


# =====================================================================
# Random tests
# =====================================================================
def _generate_random_test():
    if seed != 0:
        random.seed(seed)
    n = random.randint(1, max_boxes)
    boxes = []
    for _ in range(n):
        l = random.randint(1, max_dim)
        w = random.randint(1, max_dim)
        h = random.randint(1, max_dim)
        boxes.append((l, w, h))
    expected = _reference_height(boxes)
    return boxes, expected, f"Random test (n={n})"


# =====================================================================
# Test runner
# =====================================================================
def _run_tests():
    failed = False
    all_tests = []

    # Validate hand-made tests against reference
    for boxes, expected, description in tests:
        ref = _reference_height(boxes)
        assert (
            ref == expected
        ), f"Hand-made test '{description}' has wrong answer ({ref} vs {expected})."
        all_tests.append((boxes, expected, description))

    if generate_random_tests:
        for _ in range(random_tests):
            all_tests.append(_generate_random_test())

    for i, (boxes, expected, description) in enumerate(all_tests, 1):
        try:
            student_answer = solve(list(boxes))
        except NotImplementedError:
            print("You need to implement solve() before running the tests.")
            return
        except Exception as e:
            failed = True
            print(f"Test {i} crashed: {description}")
            print(_format_instance(boxes))
            print(f"Raised exception: {e}")
            print("-" * 60)
            continue

        response = get_feedback(student_answer, expected, boxes, expected)
        if response is not None:
            failed = True
            print(f"Test {i} failed: {description}")
            print(_format_instance(boxes))
            print(f"Your answer: {student_answer}")
            print(f"Feedback: {response}")
            print("-" * 60)

    if not failed:
        print(f"All {len(all_tests)} tests passed! ✓")


if __name__ == "__main__":
    _run_tests()
