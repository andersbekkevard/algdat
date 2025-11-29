def merge(A, p, q, r):
    INF = 1e9
    L = A[p : q + 1]
    L.append(INF)
    R = A[q + 1 : r + 1]
    R.append(INF)
    left_index, right_index = 0, 0
    for i in range(p, r + 1):
        if L[left_index] <= R[right_index]:
            A[i] = L[left_index]
            left_index += 1
        else:
            A[i] = R[right_index]
            right_index += 1


def merge_sort(A, p, r):
    if p >= r:
        return A
    q = (p + r) // 2

    merge_sort(A, p, q)
    merge_sort(A, q + 1, r)
    merge(A, p, q, r)
