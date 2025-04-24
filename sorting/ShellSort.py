def shell_sort(arr):
    arr = arr.copy()
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and (arr[j - gap][1] < temp[1] or (arr[j - gap][1] == temp[1] and arr[j - gap][0] > temp[0])):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr