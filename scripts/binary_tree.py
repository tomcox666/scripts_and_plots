class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.prev = None
        self.next = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert(key, self.root)

    def _insert(self, key, node, parent=None):
        if node is None:
            new_node = Node(key)
            if parent is not None and key < parent.val:
                new_node.prev = parent.prev
                new_node.next = parent
                if parent.prev is not None:
                    parent.prev.next = new_node
                parent.prev = new_node
            elif parent is not None and key > parent.val:
                new_node.next = parent.next
                new_node.prev = parent
                if parent.next is not None:
                    parent.next.prev = new_node
                parent.next = new_node
            return new_node
        if key < node.val:
            node.left = self._insert(key, node.left, node)
        else:
            node.right = self._insert(key, node.right, node)
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node
        if key < node.val:
            node.left = self._delete(node.left, key)
        elif key > node.val:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._minValueNode(node.right)
            node.val = temp.val
            node.right = self._delete(node.right, temp.val)
        return node

    def _minValueNode(self, node):
        current = node
        while(current.left is not None):
            current = current.left
        return current

    def inorder(self):
        self._inorder(self.root)
        print()

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            print(node.val, end=" ")
            self._inorder(node.right)

    def preorder(self):
        self._preorder(self.root)
        print()

    def _preorder(self, node):
        if node:
            print(node.val, end=" ")
            self._preorder(node.left)
            self._preorder(node.right)

    def postorder(self):
        self._postorder(self.root)
        print()

    def _postorder(self, node):
        if node:
            self._postorder(node.left)
            self._postorder(node.right)
            print(node.val, end=" ")

    def threaded_inorder(self):
        node = self.root
        while node.left is not None:
            node = node.left
        while node is not None:
            print(node.val, end=" ")
            node = node.next
        print()

# Example usage
bt = BinaryTree()
bt.insert(50)
bt.insert(30)
bt.insert(20)
bt.insert(40)
bt.insert(70)
bt.insert(60)
bt.insert(80)

print("Inorder traversal:")
bt.inorder()

print("Threaded inorder traversal:")
bt.threaded_inorder()

#Tests
