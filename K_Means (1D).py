import numpy as np
import matplotlib.pyplot as plt

# Take input for 1D data array
data_input = input("Enter 1D data points (comma or space separated): ")

# Process input into NumPy array
if ',' in data_input:
    data = np.array([int(x.strip()) for x in data_input.split(',')])
else:
    data = np.array([int(x.strip()) for x in data_input.split()])

# Input k (number of clusters)
k = int(input("Enter the value of k: "))

# Initialize centroids using first k data points
k_means = [int(data[i]) for i in range(k)]

print("\nInitial Centroids:", k_means)

# Distance function
def distance(a, b):
    return abs(a - b)

# Initialize clusters
clusters = [[] for _ in range(k)]
clusters_new = [[] for _ in range(k)]

max_iterations = 10

# K-Means Algorithm
for iteration in range(max_iterations):
    print(f"\n--- Iteration {iteration+1} ---")

    clusters_new = [[] for _ in range(k)]

    for point in data:
        distances = [distance(point, mean) for mean in k_means]
        closest_mean = np.argmin(distances)
        clusters_new[closest_mean].append(int(point))
        print(f"Point {point} assigned to Cluster {closest_mean+1} (Centroid {round(k_means[closest_mean], 2)})")

    print("\nClusters formed:")
    for i in range(k):
        print(f"Cluster {i+1}: {clusters_new[i]}")

    if clusters == clusters_new:
        print("\nClusters stabilized. Stopping early!")
        break

    clusters = clusters_new

    for j in range(k):
        if clusters[j]:
            old_mean = k_means[j]
            k_means[j] = float(np.mean(clusters[j]))
            print(f"Centroid {j+1} updated from {round(old_mean, 2)} to {round(k_means[j], 2)}")

print("\n=== Final Result ===")
for i in range(k):
    print(f"Cluster {i+1}: {clusters[i]}")
print("Final Centroids:", [round(x, 2) for x in k_means])

# Visualization
plt.figure(figsize=(8, 6))

for i, cluster in enumerate(clusters):
    plt.scatter(cluster, [0]*len(cluster), label=f"Cluster {i+1}")
plt.scatter(k_means, [0]*len(k_means), marker='x', s=100, c='red', label='Centroids')
plt.xlabel("Data Points")
plt.ylabel("Cluster")
plt.title("1D K-Means Clustering (User Input)")
plt.legend()
plt.grid(True)
plt.show()
