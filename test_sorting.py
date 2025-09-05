#!/usr/bin/env python3
"""
Sorting Algorithm Test Suite
============================

This script provides a flexible testing framework for sorting algorithms
defined in the sort/ folder. Configure the algorithm and test cases below.

FUNCTION SIGNATURE REQUIREMENTS:
===============================

Your sorting function must follow this exact signature:
    def your_sort_function(arr):
        '''
        Args:
            arr (list): A list of comparable elements to be sorted in-place

        Returns:
            list: The sorted list (must be the same list object, not a new one)
            Must sort the input list in ascending order
        '''
"""


# ===== CONFIGURATION SECTION =====
# Import the sorting function you want to test
from sort.insertion_sort import insertion_sort

# Select the sorting method to test (must match function name in imported module)
SORTING_METHOD = insertion_sort

# Test case configuration
TEST_CASES = [
    {"name": "Empty List", "input": []},
    {"name": "Single Element", "input": [42]},
    {"name": "Already Sorted", "input": [1, 2, 3, 4, 5]},
    {"name": "Reverse Sorted", "input": [5, 4, 3, 2, 1]},
    {"name": "Random Order", "input": [3, 1, 4, 1, 5, 9, 2, 6]},
    {"name": "Duplicates", "input": [3, 1, 4, 1, 5, 9, 2, 6, 3, 1]},
    {"name": "Negative Numbers", "input": [-5, 3, -1, 7, -2, 0, 4]},
    {"name": "Large Numbers", "input": [1000, 500, 2000, 100, 1500]},
]


# ===== UTILITY FUNCTIONS =====
def print_separator(title="", width=60):
    """Print a visual separator with optional title."""
    if title:
        total_width = width
        title_width = len(title) + 2
        side_width = (total_width - title_width) // 2
        separator = "=" * side_width + " " + title + " " + "=" * side_width
        if len(separator) < total_width:
            separator += "="
        print(separator)
    else:
        print("=" * width)


def print_test_result(test_case, result, original):
    """Print formatted test results."""
    print(f"\n📝 Test Case: {test_case['name']}")
    print(f"   Input:  {original}")
    print(f"   Output: {result}")

    # Verify if sorting is correct
    is_correct = result == sorted(original)
    status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
    print(f"   Status: {status}")


def run_sorting_test(sort_function, test_cases):
    """Run sorting tests and display results."""
    print_separator("SORTING ALGORITHM TEST SUITE", 60)
    print(f"🔧 Testing Algorithm: {sort_function.__name__}")
    print(f"📊 Number of Test Cases: {len(test_cases)}")
    print_separator("", 60)

    passed_tests = 0
    total_tests = len(test_cases)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. ", end="")
        original = test_case["input"].copy()
        try:
            result = sort_function(original)
            print_test_result(test_case, result, test_case["input"])

            if result == sorted(test_case["input"]):
                passed_tests += 1
        except Exception as e:
            print(f"❌ ERROR in {test_case['name']}: {str(e)}")

    # Summary
    print_separator("TEST SUMMARY", 60)
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    if total_tests - passed_tests > 0:
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the algorithm implementation.")

    print_separator("", 60)


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    try:
        run_sorting_test(SORTING_METHOD, TEST_CASES)
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print(
            "💡 Make sure the sorting algorithm is properly implemented in the sort/ folder"
        )
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("💡 Check your sorting algorithm implementation")
