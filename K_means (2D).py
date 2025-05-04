import numpy as np
import random
import matplotlib.pyplot as plt

# Get user input
def get_user_input():
    try:
        k = int(input("Enter the number of clusters (k): "))
        n = int(input("Enter the number of data points: "))
        print("Enter the data points (x y):")
        data = []
        for _ in range(n):
            x, y = map(float, input().split())
            data.append([x, y])
        return k, np.array(data)
    except Exception as e:
        print("Error:", e)
        return None, None

# Calculate Euclidean distance
def distance(p1, p2):
    return np.linalg.norm(p1 - p2)

# Assign points to closest centroid
def assign_clusters(data, centroids):
    clusters = [[] for _ in centroids]
    for point in data:
        distances = [distance(point, centroid) for centroid in centroids]
        index = np.argmin(distances)
        clusters[index].append(point)
    return clusters

# Compute new centroids
def compute_centroids(clusters, old_centroids, data):
    new_centroids = []
    for i, cluster in enumerate(clusters):
        if cluster:
            new_centroids.append(np.mean(cluster, axis=0))
        else:
            new_centroids.append(random.choice(data))  # Handle empty cluster
    return new_centroids

# Plot clusters
def plot_clusters(clusters, centroids):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']
    for i, cluster in enumerate(clusters):
        cluster = np.array(cluster)
        if len(cluster) > 0:
            plt.scatter(cluster[:, 0], cluster[:, 1], color=colors[i % len(colors)], label=f'Cluster {i}')
    for i, centroid in enumerate(centroids):
        plt.scatter(centroid[0], centroid[1], color='black', marker='X', s=100, label=f'Centroid {i}')
    plt.title("K-Means Clustering")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Run K-Means ---
k, data = get_user_input()

if k is not None and data is not None:
    random.seed(42)
    centroids = random.sample(list(data), k)

    for iteration in range(100):
        clusters = assign_clusters(data, centroids)
        new_centroids = compute_centroids(clusters, centroids, data)

        print(f"\n--- Iteration {iteration + 1} ---")
        print("Centroids:")
        for i, centroid in enumerate(new_centroids):
            print(f"Centroid {i}: {[round(coord.tolist(), 4) for coord in centroid]}")

        print("\nClusters:")
        for i, cluster in enumerate(clusters):
            readable_points = [point.tolist() for point in cluster]
            print(f"Cluster {i}: {readable_points}")

        if np.allclose(centroids, new_centroids):
            print("\nConverged.")
            break

        centroids = new_centroids

    # Final Results
    print("\n=== Final Results ===")
    print("Final Centroids:")
    for i, centroid in enumerate(centroids):
        print(f"Centroid {i}: {[round(coord.tolist(), 4) for coord in centroid]}")

    print("\nData Points in Each Cluster:")
    for i, cluster in enumerate(clusters):
        readable_points = [point.tolist() for point in cluster]
        print(f"Cluster {i}: {readable_points}")

    # Plot final result
    plot_clusters(clusters, centroids)
