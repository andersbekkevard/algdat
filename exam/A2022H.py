def subset_sum(A: list[int], target: int) -> bool:
    memo: dict[int, bool] = {0: True}

    def solve(remaining: int) -> bool:
        if remaining in memo:
            return memo[remaining]

        if remaining < 0:
            memo[remaining] = False
            return False

        for num in A:
            if solve(remaining - num):
                memo[remaining] = True
                return True

        memo[remaining] = False
        return False

    return solve(target)


# ========== BOTTOM-UP DP SOLUTION ==========
def subset_sum_bottom_up(A: list[int], target: int) -> bool:
    if target < 0:
        return False

    dp = {0: True}

    for num in A:
        current_sums = list(dp.keys())
        for current_sum in current_sums:
            if dp.get(current_sum, False):
                new_sum = current_sum + num
                dp[new_sum] = True
                # Early exit if we found the target
                if new_sum == target:
                    return True

    return dp.get(target, False)


# ========== COMPARISON FUNCTION ==========
def compare_solutions():
    """Compare top-down vs bottom-up with timing and tricky test cases."""
    import time

    print("=" * 70)
    print("SUBSET SUM: TOP-DOWN vs BOTTOM-UP COMPARISON")
    print("=" * 70)

    test_cases = [
        # (array, target, expected, description)
        ([3, 34, 4, 12, 5, 2], 9, True, "Basic case - sum exists"),
        ([3, 34, 4, 12, 5, 2], 30, False, "Sum doesn't exist"),
        ([1, 2, 3, 7], 6, True, "Multiple ways to sum (1+2+3 or none)"),
        ([1, 5, 11, 5], 11, True, "Duplicate elements"),
        ([2, 3, 7, 8, 10], 11, True, "Multiple combinations (3+8 or 2+9)"),
        ([2, 3, 7, 8, 10], 19, True, "Sum: 2+7+10=19"),
        ([2, 3, 7, 8, 10], 29, False, "Sum not possible (too close to total)"),
        ([1], 1, True, "Single element match"),
        ([5], 3, False, "Single element no match"),
        ([], 0, True, "Empty array, target 0"),
        ([1, 2, 3], 0, True, "Target is 0 (empty subset)"),
        ([10, 20, 30, 40, 50], 100, True, "Exact sum of all"),
        ([10, 20, 30, 40, 50], 101, False, "Just over total sum"),
        ([1, 1, 1, 1, 1], 3, True, "Many duplicates"),
        ([5, 10, 15, 20], 25, True, "Large numbers"),
        ([1, 2, 4, 8, 16, 32], 63, True, "Powers of 2 (all elements)"),
        ([1, 2, 4, 8, 16, 32], 45, True, "Powers of 2 (subset)"),
    ]

    all_passed = True
    total_time_top_down = 0
    total_time_bottom_up = 0

    for i, (arr, target, expected, description) in enumerate(test_cases, 1):
        print(f"\n{'─' * 70}")
        print(f"Test {i}: {description}")
        print(f"Array: {arr}")
        print(f"Target: {target}")
        print(f"Expected: {expected}")

        # Time top-down
        start = time.perf_counter()
        result_top_down = subset_sum(arr.copy(), target)
        time_top_down = time.perf_counter() - start
        total_time_top_down += time_top_down

        # Time bottom-up
        start = time.perf_counter()
        result_bottom_up = subset_sum_bottom_up(arr.copy(), target)
        time_bottom_up = time.perf_counter() - start
        total_time_bottom_up += time_bottom_up

        # Check results
        top_down_correct = result_top_down == expected
        bottom_up_correct = result_bottom_up == expected
        both_match = result_top_down == result_bottom_up

        print(
            f"\n  Top-down:    {result_top_down}  ({time_top_down*1000:.4f}ms)  {'✅' if top_down_correct else '❌'}"
        )
        print(
            f"  Bottom-up:   {result_bottom_up}  ({time_bottom_up*1000:.4f}ms)  {'✅' if bottom_up_correct else '❌'}"
        )
        print(f"  Match:       {'✅' if both_match else '❌'}")

        if not both_match or not bottom_up_correct:
            all_passed = False
            print(f"  ⚠️  MISMATCH DETECTED!")

    print(f"\n{'=' * 70}")
    print("PERFORMANCE SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total time (Top-down):  {total_time_top_down*1000:.4f}ms")
    print(f"Total time (Bottom-up): {total_time_bottom_up*1000:.4f}ms")

    if total_time_bottom_up < total_time_top_down:
        speedup = total_time_top_down / total_time_bottom_up
        print(f"✅ Bottom-up is {speedup:.2f}x FASTER")
    else:
        speedup = total_time_bottom_up / total_time_top_down
        print(f"✅ Top-down is {speedup:.2f}x FASTER")

    print(f"\n{'=' * 70}")
    if all_passed:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED - Check results above")
    print(f"{'=' * 70}\n")


# ========== DEMO / TEST BOILERPLATE ==========
if __name__ == "__main__":
    compare_solutions()
