from re import A


def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        for j in range(i - 1, -1, -1):
            if arr[j] <= arr[j + 1]:
                break
            arr[j], arr[j + 1] = arr[j + 1], arr[j]


if __name__ == "__main__":
    test_cases = [
        [],
        [1],
        [2, 1],
        [3, 1, 2],
        [5, 2, 4, 6, 1, 3],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 3, 3],
        [10, -1, 2, 5, 0],
    ]
    for arr in test_cases:
        arr_copy = arr.copy()
        insertion_sort(arr_copy)
        expected = sorted(arr)
        success = arr_copy == expected
        print(f"Original: {arr}\tSorted: {arr_copy}\tSuccess: {success}")
