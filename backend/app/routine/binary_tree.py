from typing import Any, Optional


class TreeNode:
    def __init__(self, time_key: int, data: Any):
        self.time_key = time_key
        self.data = data
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None
        self.height = 1


def _height(node: Optional[TreeNode]) -> int:
    return node.height if node is not None else 0


def _update_height(node: TreeNode) -> None:
    node.height = 1 + max(_height(node.left), _height(node.right))


def _balance_factor(node: TreeNode) -> int:
    return _height(node.left) - _height(node.right)


def _rotate_right(y: TreeNode) -> TreeNode:
    x = y.left
    y.left = x.right
    x.right = y
    _update_height(y)
    _update_height(x)
    return x


def _rotate_left(x: TreeNode) -> TreeNode:
    y = x.right
    x.right = y.left
    y.left = x
    _update_height(x)
    _update_height(y)
    return y


def _rebalance(node: TreeNode) -> TreeNode:
    _update_height(node)
    balance = _balance_factor(node)

    if balance > 1:
        if _balance_factor(node.left) < 0:
            node.left = _rotate_left(node.left)
        return _rotate_right(node)

    if balance < -1:
        if _balance_factor(node.right) > 0:
            node.right = _rotate_right(node.right)
        return _rotate_left(node)

    return node


class BinaryTree:
    """Árvore Binária de Busca auto-balanceada (AVL) indexada por `time_key`.

    A ABB simples degenera em lista quando as chaves chegam em ordem crescente
    (o caso mais comum numa agenda). O balanceamento AVL mantém a altura em
    O(log n), garantindo busca, inserção e remoção em O(log n).
    """

    def __init__(self):
        self.root: Optional[TreeNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def height(self) -> int:
        return _height(self.root)

    def insert(self, time_key: int, data: Any) -> bool:
        self.root, inserted = self._insert_recursive(self.root, time_key, data)
        if inserted:
            self._size += 1
        return inserted

    def _insert_recursive(
        self, node: Optional[TreeNode], time_key: int, data: Any
    ) -> tuple[TreeNode, bool]:
        if node is None:
            return TreeNode(time_key, data), True

        if time_key == node.time_key:
            return node, False

        if time_key < node.time_key:
            node.left, inserted = self._insert_recursive(node.left, time_key, data)
        else:
            node.right, inserted = self._insert_recursive(node.right, time_key, data)

        if not inserted:
            return node, False
        return _rebalance(node), True

    def search(self, time_key: int) -> Optional[Any]:
        node = self.root
        while node is not None:
            if time_key == node.time_key:
                return node.data
            node = node.left if time_key < node.time_key else node.right
        return None

    def predecessor(self, time_key: int) -> Optional[Any]:
        """Dado do nó com a maior chave estritamente menor que `time_key`."""
        node, best = self.root, None
        while node is not None:
            if node.time_key < time_key:
                best = node
                node = node.right
            else:
                node = node.left
        return best.data if best is not None else None

    def successor(self, time_key: int) -> Optional[Any]:
        """Dado do nó com a menor chave estritamente maior que `time_key`."""
        node, best = self.root, None
        while node is not None:
            if node.time_key > time_key:
                best = node
                node = node.left
            else:
                node = node.right
        return best.data if best is not None else None

    def remove(self, time_key: int) -> bool:
        self.root, removed = self._remove_recursive(self.root, time_key)
        if removed:
            self._size -= 1
        return removed

    def _remove_recursive(
        self, node: Optional[TreeNode], time_key: int
    ) -> tuple[Optional[TreeNode], bool]:
        if node is None:
            return None, False

        if time_key < node.time_key:
            node.left, removed = self._remove_recursive(node.left, time_key)
        elif time_key > node.time_key:
            node.right, removed = self._remove_recursive(node.right, time_key)
        else:
            # Caso 1 (folha) e caso 2 (um filho): o filho existente sobe.
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            # Caso 3 (dois filhos): o sucessor in-order assume o lugar do nó.
            successor = self._find_min(node.right)
            node.time_key = successor.time_key
            node.data = successor.data
            node.right, _ = self._remove_recursive(node.right, successor.time_key)
            removed = True

        if not removed:
            return node, False
        return _rebalance(node), True

    def _find_min(self, node: TreeNode) -> TreeNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def in_order(self) -> list[Any]:
        result: list[Any] = []
        stack: list[TreeNode] = []
        node = self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.data)
            node = node.right
        return result
