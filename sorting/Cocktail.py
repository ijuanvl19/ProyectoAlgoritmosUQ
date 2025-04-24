def cocktail_sort(arr):
    arr = arr.copy()
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i][1] < arr[i+1][1] or (arr[i][1] == arr[i+1][1] and arr[i][0] > arr[i+1][0]):
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end-1, start-1, -1):
            if arr[i][1] < arr[i+1][1] or (arr[i][1] == arr[i+1][1] and arr[i][0] > arr[i+1][0]):
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
        start += 1
    return arr