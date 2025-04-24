def comb_sort(arr):
    arr = arr.copy()
    gap = len(arr)
    shrink = 1.3
    sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        i = 0
        while i + gap < len(arr):
            if arr[i][1] < arr[i + gap][1] or (arr[i][1] == arr[i + gap][1] and arr[i][0] > arr[i + gap][0]):
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
            i += 1
    return arr