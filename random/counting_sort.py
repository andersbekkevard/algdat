def counting_sort(A, n, exp, k=9):  # k is the number of possible digits (0-9)
    B = [0] * n
    C = [0] * (k + 1)

    for i in range(n):
        digit = (A[i] // exp) % 10
        C[digit] = C[digit] + 1

    for i in range(1, k + 1):
        C[i] = C[i] + C[i - 1]

    # Iterate backwards to maintain stability (crucial when sorting by digits)
    for i in range(n - 1, -1, -1):
        digit = (A[i] // exp) % 10
        B[C[digit] - 1] = A[i]
        C[digit] = C[digit] - 1

    return B


A = [170, 45, 75, 90, 802, 24, 2, 66]
n = len(A)
print(f"Original: {A}")

# Sort by 1s digit (exp=1)
A = counting_sort(A, n, 1)
print(f"Sorted by 1s: {A}")

# Sort by 10s digit (exp=10)
A = counting_sort(A, n, 10)
print(f"Sorted by 10s: {A}")

# Sort by 100s digit (exp=100)
A = counting_sort(A, n, 100)
print(f"Sorted by 100s: {A}")
