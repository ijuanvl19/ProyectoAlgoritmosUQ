def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x[1] > pivot[1] or (x[1] == pivot[1] and x[0] < pivot[0])]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x[1] < pivot[1] or (x[1] == pivot[1] and x[0] > pivot[0])]
    return quicksort(left) + middle + quicksort(right)