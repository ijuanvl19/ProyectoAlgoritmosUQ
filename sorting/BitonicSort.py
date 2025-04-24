def bitonic_sort(arr):
    arr = arr.copy()
    n = len(arr)
    next_pow2 = 1 << (n - 1).bit_length()
    arr.extend([(chr(255), -1)] * (next_pow2 - n))
    bitonic_sort_recursive(arr, 0, len(arr), 1)
    return [x for x in arr if x[1] != -1]

def bitonic_sort_recursive(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort_recursive(arr, low, k, 1)
        bitonic_sort_recursive(arr, low + k, k, 0)
        bitonic_merge(arr, low, cnt, direction)

def bitonic_merge(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            if (direction == 1 and arr[i][1] < arr[i + k][1]) or (direction == 0 and arr[i][1] > arr[i + k][1]):
                arr[i], arr[i + k] = arr[i + k], arr[i]
        bitonic_merge(arr, low, k, direction)
        bitonic_merge(arr, low + k, k, direction)