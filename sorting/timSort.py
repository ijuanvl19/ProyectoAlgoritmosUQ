def timsort(arr):
    return sorted(arr, key=lambda x: (-x[1], x[0]))