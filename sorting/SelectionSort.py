def selection_sort(arr):
    arr = arr.copy()
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if (arr[j][1] > arr[min_idx][1]) or (arr[j][1] == arr[min_idx][1] and arr[j][0] < arr[min_idx][0]):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr