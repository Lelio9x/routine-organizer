from typing import Any, Optional


class TreeNode:
    def __init__(self, time_key: int, data: Any):
        self.time_key = time_key
        self.data = data
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


class BinaryTree:
    def __init__(self):
        self.root: Optional[TreeNode] = None

    def insert(self, time_key: int, data: Any) -> bool:
        if self.root is None:
            self.root = TreeNode(time_key, data)
            return True
        return self._insert_recursive(self.root, time_key, data)

    def _insert_recursive(self, node: TreeNode, time_key: int, data: Any) -> bool:
        if time_key == node.time_key:
            return False

        if time_key < node.time_key:
            if node.left is None:
                node.left = TreeNode(time_key, data)
                return True
            return self._insert_recursive(node.left, time_key, data)

        if node.right is None:
            node.right = TreeNode(time_key, data)
            return True
        return self._insert_recursive(node.right, time_key, data)

    def search(self, time_key: int) -> Optional[Any]:
        return self._search_recursive(self.root, time_key)

    def _search_recursive(self, node: Optional[TreeNode], time_key: int) -> Optional[Any]:
        if node is None:
            return None
        if time_key == node.time_key:
            return node.data
        if time_key < node.time_key:
            return self._search_recursive(node.left, time_key)
        return self._search_recursive(node.right, time_key)

    def remove(self, time_key: int) -> bool:
        self.root, removed = self._remove_recursive(self.root, time_key)
        return removed

    def _remove_recursive(self, node: Optional[TreeNode], time_key: int) -> tuple[Optional[TreeNode], bool]:
        if node is None:
            return None, False

        if time_key < node.time_key:
            node.left, removed = self._remove_recursive(node.left, time_key)
            return node, removed

        if time_key > node.time_key:
            node.right, removed = self._remove_recursive(node.right, time_key)
            return node, removed

        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        successor = self._find_min(node.right)
        node.time_key = successor.time_key
        node.data = successor.data
        node.right, _ = self._remove_recursive(node.right, successor.time_key)
        return node, True

    def _find_min(self, node: TreeNode) -> TreeNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def in_order(self) -> list[Any]:
        result: list[Any] = []
        self._in_order_recursive(self.root, result)
        return result

    def _in_order_recursive(self, node: Optional[TreeNode], result: list[Any]) -> None:
        if node is None:
            return
        self._in_order_recursive(node.left, result)
        result.append(node.data)
        self._in_order_recursive(node.right, result)