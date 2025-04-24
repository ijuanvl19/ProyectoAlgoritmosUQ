def tree_sort(arr):
    if not arr:
        return []
    root = Node(arr[0])
    for i in range(1, len(arr)):
        insert_iterative(root, arr[i])
    return inorder_traversal_iterative(root)

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert_iterative(root, key):
    if root is None:
        return Node(key)
    current = root
    while True:
        if key[1] > current.val[1] or (key[1] == current.val[1] and key[0] < current.val[0]):
            if current.left is None:
                current.left = Node(key)
                break
            current = current.left
        else:
            if current.right is None:
                current.right = Node(key)
                break
            current = current.right
    return root

def inorder_traversal_iterative(root):
    res = []
    stack = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        res.append(current.val)
        current = current.right
    return res