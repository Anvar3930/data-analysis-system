from storage.trees import BinaryNode, preorder, inorder, postorder, BST, AVL, RedBlackTree, Trie

def main():
    root = BinaryNode(2, BinaryNode(1), BinaryNode(3))
    print("Preorder:", preorder(root))
    print("Inorder:", inorder(root))
    print("Postorder:", postorder(root))

    bst = BST()
    for x in [10, 5, 15, 3, 7, 12]:
        bst.insert(x)
    print("BST inorder:", bst.inorder_list())
    bst.delete(5)
    print("BST after delete 5:", bst.inorder_list())

    avl = AVL()
    for x in [10, 5, 15, 3, 7, 12, 11]:
        avl.insert(x)
    print("AVL inorder:", avl.inorder_list())

    rbt = RedBlackTree()
    for x in [10, 5, 15, 3, 7, 12, 11]:
        rbt.insert(x)
    print("RBT inorder:", rbt.inorder_list(), "search(7):", rbt.search(7))

    tr = Trie()
    for w in ["cpu", "case", "car", "cat", "iphone"]:
        tr.insert(w)
    print("Trie 'ca':", tr.starts_with("ca"))

if __name__ == "__main__":
    main()
