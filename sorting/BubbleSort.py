def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][1] < arr[j + 1][1] or (arr[j][1] == arr[j + 1][1] and arr[j][0] > arr[j + 1][0]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr