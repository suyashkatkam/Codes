import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.cluster.hierarchy import dendrogram

# Step 1: Read Excel file
df = pd.read_excel(r'C:\Users\Suyash Katkam\Downloads\Agglomerative.xlsx')
points = df[['X', 'Y']].values
labels = [f'P{i+1}' for i in range(len(df))]  # Generate labels: P1, P2, ...

# Step 1.5: Compute and print Adjacency Matrix (Euclidean distances)
print("\nAdjacency Matrix (Euclidean distances):")
adj_matrix = np.zeros((len(points), len(points)))
for i in range(len(points)):
    for j in range(len(points)):
        adj_matrix[i][j] = math.sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)
print(np.round(adj_matrix, 2))

# Step 2: Euclidean distance function
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Step 3: Linkage methods
def single_link(c1, c2):
    return min(euclidean(points[i], points[j]) for i in c1 for j in c2)

def complete_link(c1, c2):
    return max(euclidean(points[i], points[j]) for i in c1 for j in c2)

def average_link(c1, c2):
    dists = [euclidean(points[i], points[j]) for i in c1 for j in c2]
    return sum(dists) / len(dists)

# Step 4: Agglomerative clustering with stepwise cluster output
def agglomerative_clustering(link_func, method_name):
    clusters = [[i] for i in range(len(points))]
    cluster_labels = [[labels[i]] for i in range(len(points))]
    history = []
    label_map = {i: i for i in range(len(points))}
    current_cluster_id = len(points)

    # Step 0: Initial cluster state
    print(f"\nInitial Clusters ({method_name} Linkage):")
    print([cl for cl in cluster_labels])

    step = 1
    while len(clusters) > 1:
        min_dist = float('inf')
        to_merge = (0, 1)

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = link_func(clusters[i], clusters[j])
                if dist < min_dist:
                    min_dist = dist
                    to_merge = (i, j)

        i, j = to_merge
        c1, c2 = clusters[i], clusters[j]
        label1, label2 = cluster_labels[i], cluster_labels[j]
        new_cluster = c1 + c2
        new_label = label1 + label2

        id1 = label_map[c1[0]]
        id2 = label_map[c2[0]]
        history.append([id1, id2, min_dist, len(new_cluster)])

        for idx in new_cluster:
            label_map[idx] = current_cluster_id
        current_cluster_id += 1

        # Update clusters and print
        clusters = [clusters[k] for k in range(len(clusters)) if k not in to_merge]
        cluster_labels = [cluster_labels[k] for k in range(len(cluster_labels)) if k not in to_merge]
        clusters.append(new_cluster)
        cluster_labels.append(new_label)

        print(f"\nStep {step}:")
        print([sorted(cl) for cl in cluster_labels])
        step += 1

    return np.array(history)

# Step 5: Dendrogram plotting
def plot_dendrogram(history, method_name):
    plt.figure(figsize=(10, 6))
    dendrogram(history, labels=labels)
    plt.title(f"Agglomerative Clustering Dendrogram ({method_name} Linkage)")
    plt.xlabel("Points")
    plt.ylabel("Distance")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Step 6: Method selection
def select_method():
    print("\nSelect linkage method:")
    print("1. Single Linkage")
    print("2. Complete Linkage")
    print("3. Average Linkage")
    choice = input("Enter 1, 2, or 3: ")

    if choice == '1':
        return "Single", single_link
    elif choice == '2':
        return "Complete", complete_link
    elif choice == '3':
        return "Average", average_link
    else:
        print("Invalid choice. Defaulting to Single Linkage.")
        return "Single", single_link

# Step 7: Run the program
method_name, func = select_method()
history = agglomerative_clustering(func, method_name)
plot_dendrogram(history, method_name)
