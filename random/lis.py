#!/usr/bin/python3
import random
from bisect import bisect_left

# =====================================================================
# Test configuration
# =====================================================================
generate_random_tests = True
random_tests = 15
max_length = 18
max_value = 40
# If seed is 0, new random instances are generated every run.
seed = 1


# =====================================================================
# Student-facing function (to be implemented by you)
# =====================================================================
def solve(seq):
    """
    Return the length of the longest strictly increasing subsequence of seq.

    You may optionally also return the subsequence itself, e.g. as either:
      - length
      - (length, subsequence)
      - [subsequence] (in which case length = len(subsequence))

    Args:
        seq: Iterable of comparable values (typically a list of ints).

    Returns:
        One of the accepted formats above.
    """
    INF = 1e9
    n = len(seq)
    memo = {i: [] for i in range(n)}
    memo[-1] = [(-INF, 0)]
    for i in range(n):
        m = -INF
        prev = memo[i - 1]

        # Kan ta alle løsninger fra i-1, fordi vår limit er INF
        for limit, result in prev:
            if result > m:
                m = result
                memo[i].append((limit, result))

        # Går nå gjennom valgene hvor vi inkluderer i
        next_element = seq[i]
        for limit, result in prev:
            if limit < next_element:
                m = max(m, result + 1)
        memo[i].append((next_element, m))
    answer = -INF
    for limit, result in memo[n - 1]:
        answer = max(answer, result)
    return answer


def solve_bisect(seq):
    """
    Optimized O(n log n) LIS length using patience sorting and bisect_left.

    Returns:
        Length of the longest strictly increasing subsequence.
    """
    tails = []
    for x in seq:
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# =====================================================================
# Reference implementation (used only for generating/validating tests)
# =====================================================================
def _reference_lis(seq):
    """Patience-sorting style LIS with reconstruction (O(n log n))."""
    n = len(seq)
    if n == 0:
        return 0, []

    tails = []
    tails_idx = []
    prev = [-1] * n

    for i, x in enumerate(seq):
        pos = bisect_left(tails, x)  # bisect_left -> strictly increasing
        if pos == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[pos] = x
            tails_idx[pos] = i
        if pos > 0:
            prev[i] = tails_idx[pos - 1]

    length = len(tails)
    # Reconstruct one optimal subsequence
    k = tails_idx[-1]
    lis = []
    while k != -1:
        lis.append(seq[k])
        k = prev[k]
    lis.reverse()
    return length, lis


# =====================================================================
# Test helpers
# =====================================================================
def _is_subsequence(candidate, seq):
    """Return True if candidate is a subsequence of seq."""
    try:
        cand = list(candidate)
    except Exception:
        return False

    it = iter(seq)
    return all(any(x == c for x in it) for c in cand)


def _is_strictly_increasing(seq):
    try:
        return all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
    except Exception:
        return False


def _extract_answer(student_answer):
    """
    Acceptable return formats:
      - int (only the length)
      - list/tuple interpreted as:
          * (length, subsequence) if first element is int
          * subsequence itself otherwise (length = len(subsequence))
    """
    if isinstance(student_answer, int):
        return student_answer, None, None

    if isinstance(student_answer, (list, tuple)):
        if len(student_answer) == 0:
            return None, None, "Empty list/tuple is not a valid return value."
        first = student_answer[0]
        if isinstance(first, int):
            length = first
            subseq = student_answer[1] if len(student_answer) > 1 else None
            return length, subseq, None
        # Treat the entire object as the subsequence
        try:
            subseq_len = len(student_answer)
        except Exception:
            return None, None, "Could not interpret your subsequence."
        return subseq_len, student_answer, None

    return None, None, f"Unsupported return type: {type(student_answer).__name__}"


def get_feedback(student_answer, expected_len, seq, reference_subseq):
    length, subseq, parse_error = _extract_answer(student_answer)
    if parse_error:
        return parse_error

    if not isinstance(length, int):
        return f"First element must be an int, got {type(length).__name__}"

    if length != expected_len:
        return f"Returned length {length}, but optimal length is {expected_len}"

    if subseq is not None:
        if not isinstance(subseq, (list, tuple)):
            try:
                subseq = list(subseq)
            except Exception:
                return "Could not convert your subsequence to a list for checking."

        if len(subseq) != expected_len:
            return f"Subsequence length is {len(subseq)}, expected {expected_len}"

        if not _is_strictly_increasing(subseq):
            return "Your subsequence is not strictly increasing."

        if not _is_subsequence(subseq, seq):
            return (
                "Your subsequence is not a subsequence of the input sequence. "
                f"Example LIS: {reference_subseq}"
            )

    return None


def _format_instance(seq):
    return f"seq: {seq}"


# =====================================================================
# Hand-crafted tests
# =====================================================================
tests = [
    ([], 0, "Empty sequence"),
    ([5], 1, "Single element"),
    ([3, 2, 1], 1, "Strictly decreasing"),
    ([1, 2, 3, 4], 4, "Already increasing"),
    ([2, 2, 2, 2], 1, "All equal"),
    ([10, 9, 2, 5, 3, 7, 101, 18], 4, "Classic example"),
    ([0, 8, 4, 12, 2], 3, "Mixed ups and downs"),
    ([3, 1, 2, 1, 8, 5, 6], 4, "Multiple optimal choices"),
]


# =====================================================================
# Random tests
# =====================================================================
def _generate_random_test():
    if seed != 0:
        random.seed(seed)

    n = random.randint(0, max_length)
    seq = [random.randint(-max_value, max_value) for _ in range(n)]
    expected_len, reference_subseq = _reference_lis(seq)
    return seq, expected_len, reference_subseq, f"Random test (n={n})"


# =====================================================================
# Test runner
# =====================================================================
def _run_tests():
    failed = False
    all_tests = []

    # Validate hand-made tests with reference solver
    for seq, expected_len, description in tests:
        ref_len, ref_subseq = _reference_lis(seq)
        assert (
            ref_len == expected_len
        ), f"Hand-made test '{description}' has wrong answer."
        all_tests.append((seq, expected_len, ref_subseq, description))

    if generate_random_tests:
        for _ in range(random_tests):
            all_tests.append(_generate_random_test())

    for i, (seq, expected_len, ref_subseq, description) in enumerate(all_tests, 1):
        try:
            student_answer = solve(list(seq))
        except NotImplementedError:
            print("You need to implement solve() before running the tests.")
            return
        except Exception as e:
            failed = True
            print(f"Test {i} crashed: {description}")
            print(_format_instance(seq))
            print(f"Raised exception: {e}")
            print("-" * 60)
            continue

        response = get_feedback(student_answer, expected_len, seq, ref_subseq)
        if response is not None:
            failed = True
            print(f"Test {i} failed: {description}")
            print(_format_instance(seq))
            print(f"Your answer: {student_answer}")
            print(f"Feedback: {response}")
            print(f"Example LIS: {ref_subseq}")
            print("-" * 60)

    if not failed:
        print(f"All {len(all_tests)} tests passed! ✓")


if __name__ == "__main__":
    _run_tests()
