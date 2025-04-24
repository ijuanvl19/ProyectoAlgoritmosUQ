def radix_sort(arr):
    arr = arr.copy()
    max_val = max(arr, key=lambda x: x[1])[1]
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort(arr, exp)
        exp *= 10
    return arr

def counting_sort(arr, exp):
    n = len(arr)
    output = [None] * n
    count = [0] * 10
    for i in range(n):
        index = (arr[i][1] // exp) % 10
        count[index] += 1
    for i in range(8, -1, -1):
        count[i] += count[i + 1]
    for i in range(n-1, -1, -1):
        index = (arr[i][1] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    return output
