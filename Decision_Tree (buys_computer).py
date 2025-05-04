import math
from collections import Counter

def calculate_entropy(data, target_column):
    class_counts = Counter([row[target_column] for row in data])
    total_rows = len(data)
    entropy = 0.0
    for count in class_counts.values():
        probability = count / total_rows
        entropy -= probability * math.log2(probability)
    return entropy

def calculate_information_gain(data, attribute, target_column):
    total_entropy = calculate_entropy(data, target_column)
    attribute_values = set([row[attribute] for row in data])
    weighted_entropy = 0.0
    total_rows = len(data)
    for value in attribute_values:
        subset = [row for row in data if row[attribute] == value]
        subset_size = len(subset)
        subset_entropy = calculate_entropy(subset, target_column)
        weighted_entropy += (subset_size / total_rows) * subset_entropy
    return total_entropy - weighted_entropy

def find_best_attribute(data, attributes, target_column):
    best_attribute = None
    max_gain = -1
    for attribute in attributes:
        gain = calculate_information_gain(data, attribute, target_column)
        print(f"Information Gain for {attribute}: {gain:.4f}")
        if gain > max_gain:
            max_gain = gain
            best_attribute = attribute
    return best_attribute

def build_decision_tree(data, attributes, target_column, tree=None):
    if tree is None:
        tree = {}
    classes = [row[target_column] for row in data]
    if len(set(classes)) == 1:
        return classes[0]
    if not attributes:
        return Counter(classes).most_common(1)[0][0]
    best_attribute = find_best_attribute(data, attributes, target_column)
    print(f"\nBest attribute to split on: {best_attribute}\n")
    tree = {best_attribute: {}}
    remaining_attributes = [attr for attr in attributes if attr != best_attribute]
    attribute_values = set([row[best_attribute] for row in data])
    for value in attribute_values:
        subset = [row for row in data if row[best_attribute] == value]
        if not subset:
            tree[best_attribute][value] = Counter(classes).most_common(1)[0][0]
        else:
            tree[best_attribute][value] = build_decision_tree(subset, remaining_attributes, target_column)
    return tree

def classify(tree, instance):
    if isinstance(tree, str):
        return tree
    attribute = next(iter(tree))
    attribute_value = instance.get(attribute)
    if attribute_value not in tree[attribute]:
        return None
    return classify(tree[attribute][attribute_value], instance)

def print_rules(tree, rule=""):
    if isinstance(tree, str):
        print(f"IF {rule} THEN Class = {tree}")
        return
    attribute = next(iter(tree))
    for value, subtree in tree[attribute].items():
        new_rule = f"{rule} AND {attribute} = {value}" if rule else f"{attribute} = {value}"
        print_rules(subtree, new_rule)

def print_tree(tree, indent=""):
    if isinstance(tree, str):
        print(indent + "└── Class:", tree)
        return
    attribute = next(iter(tree))
    print(indent + attribute)
    for value, subtree in tree[attribute].items():
        print(indent + "├──", value)
        print_tree(subtree, indent + "│   ")

def decision_tree_main():
    data = [
        {'Age': 'Youth', 'Income': 'High', 'Student': 'No', 'Credit_rating': 'Fair', 'Class': 'No'},
        {'Age': 'Youth', 'Income': 'High', 'Student': 'No', 'Credit_rating': 'Excellent', 'Class': 'No'},
        {'Age': 'Middle_aged', 'Income': 'High', 'Student': 'No', 'Credit_rating': 'Fair', 'Class': 'Yes'},
        {'Age': 'Senior', 'Income': 'Medium', 'Student': 'No', 'Credit_rating': 'Fair', 'Class': 'Yes'},
        {'Age': 'Senior', 'Income': 'Low', 'Student': 'Yes', 'Credit_rating': 'Fair', 'Class': 'Yes'},
        {'Age': 'Senior', 'Income': 'Low', 'Student': 'Yes', 'Credit_rating': 'Excellent', 'Class': 'No'},
        {'Age': 'Middle_aged', 'Income': 'Low', 'Student': 'Yes', 'Credit_rating': 'Excellent', 'Class': 'Yes'},
        {'Age': 'Youth', 'Income': 'Medium', 'Student': 'No', 'Credit_rating': 'Fair', 'Class': 'No'},
        {'Age': 'Youth', 'Income': 'Low', 'Student': 'Yes', 'Credit_rating': 'Fair', 'Class': 'Yes'},
        {'Age': 'Senior', 'Income': 'Medium', 'Student': 'Yes', 'Credit_rating': 'Fair', 'Class': 'Yes'},
        {'Age': 'Youth', 'Income': 'Medium', 'Student': 'Yes', 'Credit_rating': 'Excellent', 'Class': 'Yes'},
        {'Age': 'Middle_aged', 'Income': 'Medium', 'Student': 'No', 'Credit_rating': 'Excellent', 'Class': 'Yes'},
        {'Age': 'Middle_aged', 'Income': 'High', 'Student': 'Yes', 'Credit_rating': 'Fair', 'Class': 'Yes'},
        {'Age': 'Senior', 'Income': 'Medium', 'Student': 'No', 'Credit_rating': 'Excellent', 'Class': 'No'}
    ]
    attributes = ['Age', 'Income', 'Student', 'Credit_rating']
    target_column = 'Class'

    print("Step 1: Calculating Initial Entropy (Info(D))")
    print(f"Initial Entropy (Info(D)): {calculate_entropy(data, target_column):.4f}\n")

    print("Step 2: Calculating Information Gain for Each Attribute")
    for attr in attributes:
        print(f"Information Gain for {attr}: {calculate_information_gain(data, attr, target_column):.4f}")

    print("\nStep 3: Building the Decision Tree")
    decision_tree = build_decision_tree(data, attributes, target_column)

    print("\nStep 4: Decision Tree Rules")
    print_rules(decision_tree)

    print("\nStep 5: Text-Based Tree Visualization")
    print_tree(decision_tree)

decision_tree_main()
