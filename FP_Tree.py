import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

# TreeNode Class
class TreeNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}

    def increment(self, count):
        self.count += count

# Insert items into the FP-tree
def insert_tree(items, node):
    if len(items) == 0:
        return
    first = items[0]
    if first in node.children:
        node.children[first].increment(1)
    else:
        node.children[first] = TreeNode(first, 1, node)
    remaining_items = items[1:]
    insert_tree(remaining_items, node.children[first])

# Draw FP-Tree using networkx
def draw_tree(root):
    G = nx.DiGraph()

    def add_edges(node, parent_name):
        for child in node.children.values():
            current_name = f"{child.item}:{child.count}"
            G.add_edge(parent_name, current_name)
            add_edges(child, current_name)

    root_name = "null"
    G.add_node(root_name)
    add_edges(root, root_name)

    pos = hierarchy_pos(G, root_name)
    plt.figure(figsize=(9.8, 7))
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=1000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.title("FP-Tree Visualization", fontsize=15)
    plt.show()

# Tree Layout function
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = {}
    def _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter, pos, parent=None):
        children = list(G.successors(root))
        if not isinstance(G, nx.DiGraph):
            raise TypeError('G must be a DiGraph.')
        if root not in pos:
            pos[root] = (xcenter, vert_loc)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter, pos)

# Build FP-Tree
def build_fp_tree(transactions, min_support_count):
    item_count = defaultdict(int)

    # First scan to count frequencies
    for transaction in transactions:
        for item in transaction:
            item_count[item] += 1

    # Remove infrequent items
    item_count = {item: count for item, count in item_count.items() if count >= min_support_count}

    # Sort by frequency
    freq_items = sorted(item_count.items(), key=lambda x: (-x[1], x[0]))

    print("\nFP-Table (after support filtering):")
    for item, count in freq_items:
        print(f"Item: {item}, Count: {count}")

    # Map item to position
    item_order = {item: idx for idx, (item, _) in enumerate(freq_items)}

    # Create FP-Tree root
    root = TreeNode('null', 1, None)

    # Insert transactions
    for tidx, transaction in enumerate(transactions):
        ordered_items = [item for item in sorted(transaction, key=lambda x: item_order.get(x, float('inf'))) if item in item_order]
        print(f"\nTransaction {tidx+1}: {ordered_items}")
        insert_tree(ordered_items, root)

        print(f"Drawing FP-Tree after Transaction {tidx+1}:")
        draw_tree(root)

    return root

# Sample Transactions
transactions = [
    ['I1', 'I2', 'I5'],
    ['I2', 'I4'],
    ['I2', 'I3'],
    ['I1', 'I2', 'I4'],
    ['I1', 'I3'],
    ['I2', 'I3'],
    ['I1', 'I3'],
    ['I1', 'I2', 'I3', 'I5'],
    ['I1', 'I2', 'I3']
]

# Take user input for min_support and min_confidence
# min_support = float(input("Enter minimum support (between 0 and 1): "))

# User Input
min_support = 0.22  # 22% minimum support
min_support_count = int(min_support * len(transactions))  # minimum count (on 9 transactions)

# Build and visualize FP-Tree
fp_tree_root = build_fp_tree(transactions, min_support_count)

print("\nFinal FP-Tree Visualization:")
draw_tree(fp_tree_root)
