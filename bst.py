class BstNode:
    def __init__(self, data):
        self.data = data[0]
        self.priority = data[1]
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def Insert(self, root, data):
        if root == None:
            return BstNode(data)
        if data[0] <= root.data[0]:
            root.left = self.Insert(root.left, data)
        else:
            root.right = self.Insert(root.right, data)
        return root

    def Remove(self, root, data):
        if (root == None):
            return root
        if (data < root.data):
            root.left = self.Remove(root.left, data)
        elif (data > root.data):
            root.right = self.Remove(root.right, data)
        else:
            if (root.left == None and root.right == None):
                root = None
                return None
            elif (root.left == None):
                temp = root.right
                root = None
                return temp
            elif (root.right == None):
                temp = root.left
                root = None
                return temp
            else:
                temp = self.FindMinNode(root.right)
                root.data = temp.data
                root.right = self.Remove(root.right, temp.data)

        return root

    def FindMinNode(self, root):
        if root is None:
            return None
        while root.left is not None:
            root = root.left
        return root

    def Print(self, root):
        if root is None:
            return
        self.Print(root.left)
        print(root.data, end=' ')
        self.Print(root.right)