def bucket_sort(arr):
    arr = arr.copy()
    if len(arr) == 0:
        return []
    max_val = max(arr, key=lambda x: x[1])[1]
    size = len(arr)
    buckets = [[] for _ in range(size)]
    for item in arr:
        index = int(item[1] * size / (max_val + 1))
        buckets[index].append(item)
    for i in range(size):
        buckets[i] = sorted(buckets[i], key=lambda x: (-x[1], x[0]))
    result = []
    for bucket in buckets:
        result.extend(bucket)
    return result