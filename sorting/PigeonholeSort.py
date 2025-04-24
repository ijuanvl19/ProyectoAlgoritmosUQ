def pigeonhole_sort(arr):
    arr = arr.copy()
    max_val = max(arr, key=lambda x: x[1])[1]
    min_val = min(arr, key=lambda x: x[1])[1]
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]
    for item in arr:
        holes[item[1] - min_val].append(item)
    result = []
    for i in range(size - 1, -1, -1):
        result.extend(sorted(holes[i], key=lambda x: x[0]))
    return result