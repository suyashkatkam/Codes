import numpy as np
import random
import matplotlib.pyplot as plt

def kmeans_1d():
    # Take user input for 1D data points
    data_input = input("Enter 1D data points (comma or space separated): ")

    # Process input into NumPy array
    if ',' in data_input:
        data = np.array([int(x.strip()) for x in data_input.split(',')])
    else:
        data = np.array([int(x.strip()) for x in data_input.split()])

    # Input k (number of clusters)
    k = int(input("Enter the value of k: "))
    k_means = [int(data[i]) for i in range(k)]
    print("\nInitial Centroids:", k_means)

    def distance(a, b): return abs(a - b)

    clusters = [[] for _ in range(k)]
    clusters_new = [[] for _ in range(k)]
    max_iterations = 10

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

    plt.figure(figsize=(8, 6))
    for i, cluster in enumerate(clusters):
        plt.scatter(cluster, [0]*len(cluster), label=f"Cluster {i+1}")
    plt.scatter(k_means, [0]*len(k_means), marker='x', s=100, c='red', label='Centroids')
    plt.xlabel("Data Points")
    plt.ylabel("Cluster")
    plt.title("1D K-Means Clustering")
    plt.legend()
    plt.grid(True)
    plt.show()

def kmeans_2d():
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

    def distance(p1, p2):
        return np.linalg.norm(p1 - p2)

    def assign_clusters(data, centroids):
        clusters = [[] for _ in centroids]
        for point in data:
            distances = [distance(point, centroid) for centroid in centroids]
            index = np.argmin(distances)
            clusters[index].append(point)
        return clusters

    def compute_centroids(clusters, old_centroids, data):
        new_centroids = []
        for i, cluster in enumerate(clusters):
            if cluster:
                new_centroids.append(np.mean(cluster, axis=0))
            else:
                new_centroids.append(random.choice(data))
        return new_centroids

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

        print("\n=== Final Results ===")
        print("Final Centroids:")
        for i, centroid in enumerate(centroids):
            print(f"Centroid {i}: {[round(coord.tolist(), 4) for coord in centroid]}")

        print("\nData Points in Each Cluster:")
        for i, cluster in enumerate(clusters):
            readable_points = [point.tolist() for point in cluster]
            print(f"Cluster {i}: {readable_points}")

        plot_clusters(clusters, centroids)

# --- Looping Menu ---
while True:
    print("\nK-Means Clustering Menu")
    print("1. 1D Clustering")
    print("2. 2D Clustering")
    print("0. Exit")
    choice = input("Enter your choice (0/1/2): ")

    if choice == '1':
        kmeans_1d()
    elif choice == '2':
        kmeans_2d()
    elif choice == '0':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter 0, 1, or 2.")
