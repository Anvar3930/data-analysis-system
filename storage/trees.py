from typing import Any, Optional, List, Dict

class BinaryNode:
    def __init__(self, key: Any, left: Optional["BinaryNode"]=None, right: Optional["BinaryNode"]=None):
        self.key = key
        self.left = left
        self.right = right

def preorder(root: Optional[BinaryNode]) -> List[Any]:
    if not root: return []
    return [root.key] + preorder(root.left) + preorder(root.right)

def inorder(root: Optional[BinaryNode]) -> List[Any]:
    if not root: return []
    return inorder(root.left) + [root.key] + inorder(root.right)

def postorder(root: Optional[BinaryNode]) -> List[Any]:
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.key]

class BSTNode:
    def __init__(self, key: Any):
        self.key = key
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None

class BST:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: Any) -> None:
        def _ins(node: Optional[BSTNode], k: Any) -> BSTNode:
            if not node:
                return BSTNode(k)
            if k < node.key:
                node.left = _ins(node.left, k)
            elif k > node.key:
                node.right = _ins(node.right, k)
            return node
        self.root = _ins(self.root, key)

    def search(self, key: Any) -> bool:
        cur = self.root
        while cur:
            if key == cur.key: return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def delete(self, key: Any) -> None:
        def _min_node(n: BSTNode) -> BSTNode:
            while n.left:
                n = n.left
            return n

        def _del(node: Optional[BSTNode], k: Any) -> Optional[BSTNode]:
            if not node:
                return None
            if k < node.key:
                node.left = _del(node.left, k)
            elif k > node.key:
                node.right = _del(node.right, k)
            else:
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                succ = _min_node(node.right)
                node.key = succ.key
                node.right = _del(node.right, succ.key)
            return node
        self.root = _del(self.root, key)

    def inorder_list(self) -> List[Any]:
        def _in(n: Optional[BSTNode]) -> List[Any]:
            if not n: return []
            return _in(n.left) + [n.key] + _in(n.right)
        return _in(self.root)

class AVLNode:
    def __init__(self, key: Any):
        self.key = key
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.h = 1

def _h(n: Optional[AVLNode]) -> int:
    return n.h if n else 0

def _upd(n: AVLNode) -> None:
    n.h = 1 + max(_h(n.left), _h(n.right))

def _bf(n: AVLNode) -> int:
    return _h(n.left) - _h(n.right)

def _rot_right(y: AVLNode) -> AVLNode:
    x = y.left
    t2 = x.right
    x.right = y
    y.left = t2
    _upd(y); _upd(x)
    return x

def _rot_left(x: AVLNode) -> AVLNode:
    y = x.right
    t2 = y.left
    y.left = x
    x.right = t2
    _upd(x); _upd(y)
    return y

class AVL:
    def __init__(self):
        self.root: Optional[AVLNode] = None

    def insert(self, key: Any) -> None:
        def _ins(n: Optional[AVLNode], k: Any) -> AVLNode:
            if not n:
                return AVLNode(k)
            if k < n.key:
                n.left = _ins(n.left, k)
            elif k > n.key:
                n.right = _ins(n.right, k)
            else:
                return n
            _upd(n)
            bal = _bf(n)
            if bal > 1 and k < n.left.key:
                return _rot_right(n)
            if bal < -1 and k > n.right.key:
                return _rot_left(n)
            if bal > 1 and k > n.left.key:
                n.left = _rot_left(n.left)
                return _rot_right(n)
            if bal < -1 and k < n.right.key:
                n.right = _rot_right(n.right)
                return _rot_left(n)
            return n
        self.root = _ins(self.root, key)

    def inorder_list(self) -> List[Any]:
        def _in(n: Optional[AVLNode]) -> List[Any]:
            if not n: return []
            return _in(n.left) + [n.key] + _in(n.right)
        return _in(self.root)

RED = 1
BLACK = 0

class RBNode:
    def __init__(self, key: Any, color: int = RED):
        self.key = key
        self.color = color
        self.left: Optional["RBNode"] = None
        self.right: Optional["RBNode"] = None
        self.parent: Optional["RBNode"] = None

class RedBlackTree:
    def __init__(self):
        self.root: Optional[RBNode] = None

    def _rotate_left(self, x: RBNode) -> None:
        y = x.right
        if not y: return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, y: RBNode) -> None:
        x = y.left
        if not x: return
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    def insert(self, key: Any) -> None:
        node = RBNode(key, RED)
        y = None
        x = self.root
        while x:
            y = x
            if node.key < x.key:
                x = x.left
            elif node.key > x.key:
                x = x.right
            else:
                return
        node.parent = y
        if not y:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        self._fix_insert(node)

    def _fix_insert(self, z: RBNode) -> None:
        while z.parent and z.parent.color == RED:
            gp = z.parent.parent
            if not gp:
                break
            if z.parent == gp.left:
                y = gp.right
                if y and y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    gp.color = RED
                    z = gp
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.color = BLACK
                    gp.color = RED
                    self._rotate_right(gp)
            else:
                y = gp.left
                if y and y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    gp.color = RED
                    z = gp
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.color = BLACK
                    gp.color = RED
                    self._rotate_left(gp)
        if self.root:
            self.root.color = BLACK

    def search(self, key: Any) -> bool:
        cur = self.root
        while cur:
            if key == cur.key: return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def inorder_list(self) -> List[Any]:
        def _in(n: Optional[RBNode]) -> List[Any]:
            if not n: return []
            return _in(n.left) + [n.key] + _in(n.right)
        return _in(self.root)

class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        cur = self.root
        for ch in word:
            if ch not in cur.children:
                cur.children[ch] = TrieNode()
            cur = cur.children[ch]
        cur.end = True

    def starts_with(self, prefix: str) -> List[str]:
        cur = self.root
        for ch in prefix:
            if ch not in cur.children:
                return []
            cur = cur.children[ch]
        out: List[str] = []
        def _dfs(node: TrieNode, path: str):
            if node.end:
                out.append(path)
            for c, nxt in node.children.items():
                _dfs(nxt, path + c)
        _dfs(cur, prefix)
        return out

class MinHeap:
    def __init__(self):
        self.a = []

    def push(self, x):
        self.a.append(x)
        i = len(self.a) - 1
        while i > 0:
            p = (i - 1) // 2
            if self.a[p] <= self.a[i]:
                break
            self.a[p], self.a[i] = self.a[i], self.a[p]
            i = p

    def pop(self):
        if not self.a:
            raise IndexError("pop from empty heap")
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            i = 0
            n = len(self.a)
            while True:
                l = 2 * i + 1
                r = 2 * i + 2
                m = i
                if l < n and self.a[l] < self.a[m]:
                    m = l
                if r < n and self.a[r] < self.a[m]:
                    m = r
                if m == i:
                    break
                self.a[i], self.a[m] = self.a[m], self.a[i]
                i = m
        return top

    def peek(self):
        if not self.a:
            raise IndexError("peek from empty heap")
        return self.a[0]

    def __len__(self):
        return len(self.a)


class MaxHeap:
    def __init__(self):
        self.a = []

    def push(self, x):
        self.a.append(x)
        i = len(self.a) - 1
        while i > 0:
            p = (i - 1) // 2
            if self.a[p] >= self.a[i]:
                break
            self.a[p], self.a[i] = self.a[i], self.a[p]
            i = p

    def pop(self):
        if not self.a:
            raise IndexError("pop from empty heap")
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            i = 0
            n = len(self.a)
            while True:
                l = 2 * i + 1
                r = 2 * i + 2
                m = i
                if l < n and self.a[l] > self.a[m]:
                    m = l
                if r < n and self.a[r] > self.a[m]:
                    m = r
                if m == i:
                    break
                self.a[i], self.a[m] = self.a[m], self.a[i]
                i = m
        return top

    def peek(self):
        if not self.a:
            raise IndexError("peek from empty heap")
        return self.a[0]

    def __len__(self):
        return len(self.a)
