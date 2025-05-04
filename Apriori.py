from itertools import combinations

# Function to take user input for transactions
def get_transactions():
    print("Enter transactions. Each transaction should be items separated by spaces (e.g., 'milk bread butter').")
    print("Type 'done' when all transactions are entered.")
    transactions = []
    while True:
        user_input = input("Enter transaction: ").strip()
        if user_input.lower() == 'done':
            break
        transactions.append(user_input.split())
    return transactions

# Function to calculate support for itemsets
def calculate_support(itemsets, transactions):
    support = {}
    for itemset in itemsets:
        count = sum(1 for transaction in transactions if itemset.issubset(set(transaction)))
        support[frozenset(itemset)] = count
    return support

# Improved candidate generation using Apriori principle
def generate_candidates(prev_frequent_itemsets, size):
    candidates = []
    len_prev = len(prev_frequent_itemsets)
    for i in range(len_prev):
        for j in range(i + 1, len_prev):
            l1 = list(prev_frequent_itemsets[i])
            l2 = list(prev_frequent_itemsets[j])
            l1.sort()
            l2.sort()
            if l1[:size - 2] == l2[:size - 2]:  # join step
                candidate = prev_frequent_itemsets[i] | prev_frequent_itemsets[j]
                # prune step: check all subsets
                if all(set(subset) in prev_frequent_itemsets for subset in combinations(candidate, size - 1)):
                    candidates.append(candidate)
    return candidates

# Apriori Algorithm
def apriori(transactions, min_support):
    items = set(item for transaction in transactions for item in transaction)
    itemsets = [frozenset([item]) for item in items]

    support_data = {}
    frequent_itemsets = []

    while itemsets:
        support = calculate_support(itemsets, transactions)
        filtered_itemsets = [itemset for itemset in itemsets if support[itemset] >= min_support]
        support_data.update({itemset: count for itemset, count in support.items() if count >= min_support})
        frequent_itemsets.extend(filtered_itemsets)
        itemsets = generate_candidates(filtered_itemsets, size=len(filtered_itemsets[0]) + 1) if filtered_itemsets else []

    return frequent_itemsets, support_data

# Function to generate strong association rules
def generate_rules(frequent_itemsets, support_data, min_confidence):
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    if consequent:
                        confidence = support_data[itemset] / support_data[antecedent]
                        if confidence >= min_confidence:
                            rules.append((set(antecedent), set(consequent), confidence))
    return rules

# Main program
transactions = [
    ['I1', 'I3', 'I4', 'I6'],
    ['I2', 'I3', 'I5', '7'],
    ['I1', 'I2', 'I3', 'I5', 'I8'],
    ['I2', 'I5', 'I9', 'I10'],
    ['I1', 'I4'],
]

if len(transactions) < 1:
    print("At least one transaction is required.")
else:
    min_support = float(input("Enter the minimum support (e.g., 0.22 for 22%): "))
    min_support = int(round(min_support * len(transactions), 0))
    print(min_support)
    min_confidence = float(input("Enter the minimum confidence (e.g., 0.6 for 60%): "))

    # Run Apriori Algorithm
    frequent_itemsets, support_data = apriori(transactions, min_support)

    # Display Frequent Itemsets
    print("\nFrequent Itemsets:")
    for itemset in sorted(frequent_itemsets, key=lambda x: (len(x), sorted(x))):
        print(f"{set(itemset)} (Support: {support_data[itemset]})")

    # Generate and Display Strong Association Rules
    rules = generate_rules(frequent_itemsets, support_data, min_confidence)
    print("\nStrong Association Rules:")
    for antecedent, consequent, confidence in rules:
        print(f"{antecedent} => {consequent} (Confidence: {confidence:.2f})")
