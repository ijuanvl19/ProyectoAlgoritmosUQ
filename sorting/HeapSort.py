def heap_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and (arr[l][1] > arr[largest][1] or (arr[l][1] == arr[largest][1] and arr[l][0] < arr[largest][0])):
        largest = l
    if r < n and (arr[r][1] > arr[largest][1] or (arr[r][1] == arr[largest][1] and arr[r][0] < arr[largest][0])):
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
