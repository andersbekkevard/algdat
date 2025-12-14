from __future__ import annotations
from typing import Optional
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, value):
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None

    def __str__(self):
        return f"Node({self.value})"

    def __repr__(self):
        return self.__str__()


def inorder_tree_walk(node):
    if node is not None:
        inorder_tree_walk(node.left)
        print(node.value)
        inorder_tree_walk(node.right)


def tree_search(x, key):
    if x is None or x.value == key:
        return x
    if x.value > key:
        return tree_search(x.left, key)
    else:
        return tree_search(x.right, key)


def iterative_tree_search(x, key):
    while x is not None and x.value != key:
        if x.value > key:
            x = x.left
        else:
            x = x.right
    return x


def tree_insert(root, z):
    # Implemented with a trailing pointer
    p = None
    x = root
    while x is not None:
        p = x
        if z.value < x.value:
            x = x.left
        else:
            x = x.right

    z.parent = p
    if p is None:
        return  # make z new root
    else:
        if z.value < p.value:
            p.left = z
        else:
            p.right = z


def draw_tree(root):
    if root is None:
        return

    G = nx.DiGraph()
    labels = {}

    def build_graph(node):
        if node:
            G.add_node(node)
            labels[node] = node.value
            if node.left:
                G.add_edge(node, node.left)
                build_graph(node.left)
            if node.right:
                G.add_edge(node, node.right)
                build_graph(node.right)

    build_graph(root)

    def get_pos(node, x=0.0, y=0.0, width=4.0):
        pos = {node: (x, y)}
        if node.left:
            pos.update(get_pos(node.left, x - width / 2, y - 1, width / 2))
        if node.right:
            pos.update(get_pos(node.right, x + width / 2, y - 1, width / 2))
        return pos

    pos = get_pos(root)

    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        labels=labels,
        with_labels=True,
        node_size=2000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        arrows=True,
    )
    plt.title("BST Visualization")
    plt.show()


n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n5 = Node(5)
n6 = Node(1)
n7 = Node(1)
n8 = Node(1)
n9 = Node(1)
n10 = Node(1)

root = n1
tree_insert(root, n2)
tree_insert(root, n3)
tree_insert(root, n4)
tree_insert(root, n5)
tree_insert(root, n6)
tree_insert(root, n7)
tree_insert(root, n8)
tree_insert(root, n9)
tree_insert(root, n10)
draw_tree(root)
