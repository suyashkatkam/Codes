import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from Excel
df = pd.read_excel(r'C:\Users\Suyash Katkam\Downloads\Data_Discretization.xlsx')
data = df.iloc[:, 0].values  
data = sorted(data)  # Returns a new sorted list

# User input for number of bins
num_bins = int(input("Enter the number of bins: "))
bin_size = len(data) // num_bins

# Create equi-depth bins
bins = [data[i * bin_size : (i + 1) * bin_size] for i in range(num_bins - 1)]
bins.append(data[(num_bins - 1) * bin_size:])

# Bin transformation - means
mean_bins = [np.full(len(b), np.mean(b)) for b in bins]

# Bin transformation - boundaries
boundary_bins = [
    [min(b) if val < (min(b) + max(b)) / 2 else max(b) for val in b] for b in bins
]

# === Cleanly Print the bin details ===
print("\nOriginal Bins (Equi-depth):")
for i, b in enumerate(bins, start=1):
    print(f"Bin {i}: {[int(val) for val in b]}")

print("\nBin Means:")
for i, b in enumerate(mean_bins, start=1):
    print(f"Bin {i}: {[round(float(val), 1) for val in b]}")

print("\nBin Boundaries:")
for i, b in enumerate(boundary_bins, start=1):
    print(f"Bin {i}: {[int(val) for val in b]}")

# Flatten all bins for plotting
original = data
means = np.concatenate(mean_bins)
boundaries = np.concatenate(boundary_bins)

# Plot histograms
titles = ["Original Data", "Bin Means", "Bin Boundaries"]
datasets = [original, means, boundaries]
colors = ["skyblue", "orange", "green"]

plt.figure(figsize=(10, 12))
for i in range(3):
    plt.subplot(3, 1, i+1)
    plt.hist(datasets[i], bins=num_bins, color=colors[i], edgecolor='black')
    plt.title(titles[i])
    if i == 2: plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.grid(True)

plt.tight_layout()
plt.show()
