def binary_insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        val = arr[i]
        low = 0
        high = i - 1
        while low <= high:
            mid = (low + high) // 2
            if (arr[mid][1] < val[1]) or (arr[mid][1] == val[1] and arr[mid][0] > val[0]):
                high = mid - 1
            else:
                low = mid + 1
        arr = arr[:low] + [val] + arr[low:i] + arr[i+1:]
    return arr