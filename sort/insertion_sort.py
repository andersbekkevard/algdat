def insertion_sort(arr):
    # Itererer over alle elementene
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            # Skyver alle en indeks opp, så vi får plass til å inserte
            arr[j + 1] = arr[j]
            j -= 1
        # Nå er elementet på j det første som er mindre enn key
        arr[j + 1] = key

    return arr
