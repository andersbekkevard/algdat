INF = 1e9


def merge(A, p, q, r):
    L = A[p : q + 1]
    R = A[q + 1 : r + 1]
    L.append(INF)
    R.append(INF)

    i, j = 0, 0
    for pos in range(p, r + 1):
        if L[i] <= R[j]:
            A[pos] = L[i]
            i += 1
        else:
            A[pos] = R[j]
            j += 1


def merge_sort(A, p, r):
    if p < r:
        q = p + (r - p) // 2
        merge_sort(A, p, q)
        merge_sort(A, q + 1, r)
        merge(A, p, q, r)


A = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
merge_sort(A, 0, len(A) - 1)
print(A)
