import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load Excel data
df = pd.read_excel(r'C:\Users\Suyash Katkam\Downloads\Linear_Regression.xlsx')

# Step 2: Extract X and Y values (assuming 1st and 2nd columns)
X = df.iloc[:, 0].tolist()
Y = df.iloc[:, 1].tolist()

# Step 3: Calculate Avg(X) and Avg(Y)
x_bar = sum(X) / len(X)
y_bar = sum(Y) / len(Y)

print(f"x_bar (Average of X) = {x_bar:.2f}")
print(f"y_bar (Average of Y) = {y_bar:.2f}")

# Step 4: Calculate β (slope)
numerator = sum((x - x_bar) * (y - y_bar) for x, y in zip(X, Y))
denominator = sum((x - x_bar) ** 2 for x in X)
beta = numerator / denominator

# Step 5: Calculate α (intercept)
alpha = y_bar - beta * x_bar

# Step 6: Display equation
print(f"\nβ (Slope) = {beta:.2f}")
print(f"α (Intercept) = {alpha:.2f}")
print(f"Linear Regression Equation: y = {alpha:.2f} + {beta:.2f}x")

# Step 7: Plot the data and regression line
plt.figure(figsize=(8, 5))
plt.scatter(X, Y, color='blue', label='Data Points')

# Step 8: Predict Y for a given X
input_x = float(input("Enter an X value to predict Y: "))
predicted_y = alpha + beta * input_x
print(f"Predicted Y for X = {input_x:.2f} is: {predicted_y:.2f}")

# Regression line points
x_line = list(range(min(X), max(X) + 1))
y_line = [alpha + beta * x for x in x_line]

plt.plot(x_line, y_line, color='red', label='Regression Line')

# Styling the plot
plt.title("Linear Regression")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)
plt.show()
