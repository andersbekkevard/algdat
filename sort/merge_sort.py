def merge(A, p, q, r):
    if p >= r:
        return
    L = A[p : q + 1]
    L.append(float("inf"))
    R = A[q + 1 : r + 1]
    R.append(float("inf"))
    left_index, right_index = 0, 0

    for i in range(p, r + 1):
        if L[left_index] <= R[right_index]:
            A[i] = L[left_index]
            left_index += 1
        else:
            A[i] = R[right_index]
            right_index += 1


def merge_sort(A, p, r):
    if p == r:
        return
    q = (p + r) // 2
    merge_sort(A, p, q)
    merge_sort(A, q + 1, r)
    merge(A, p, q, r)


def merge_sort_wrapper(A):
    if A:
        merge_sort(A, 0, len(A) - 1)
    return A
