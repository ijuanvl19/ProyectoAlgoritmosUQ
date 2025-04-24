def gnome_sort(arr):
    arr = arr.copy()
    index = 0
    while index < len(arr):
        if index == 0 or arr[index][1] > arr[index - 1][1] or (arr[index][1] == arr[index - 1][1] and arr[index][0] <= arr[index - 1][0]):
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr