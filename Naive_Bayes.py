import pandas as pd
import random
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv(r'C:\Users\Suyash Katkam\Downloads\plays_football.csv')

# Normalize column names and string values
data.columns = [col.strip().lower() for col in data.columns]
for col in data.columns:
    if data[col].dtype == object:
        data[col] = data[col].map(lambda x: x.strip().lower() if isinstance(x, str) else x)

# Identify class column
class_column = 'class'
# Exclude 'id' column if present
features = [col for col in data.columns if col not in [class_column, 'id']]

# === Function Definitions ===

def calculate_class_probability(data, class_column, class_value):
    return round(len(data[data[class_column] == class_value]) / len(data), 4)

def calculate_conditional_probability(data, feature, class_column, feature_value, class_value):
    subset = data[data[class_column] == class_value]
    numerator = len(subset[subset[feature] == feature_value])
    denominator = len(subset)
    probability = round(numerator / denominator, 3) if denominator != 0 else 0
    print(f"P({feature} = {feature_value} | class = {class_value}) = {probability}")
    return probability

def compute_likelihood(probabilities):
    result = 1.0
    for prob in probabilities:
        result *= prob
    return round(result, 4)

# === Main Flow ===

# Show feature names
print("\n=== Feature Names ===")
for feature in features:
    print(f"- {feature}")

print("\nClass Label: class (yes/no)")

# Manually define input
X = {
    'outlook': 'rain',
    'temperature': 'cool',
    'humidity': 'normal',
    'windy': 'strong'
}

print("\nUser-defined feature input:")
for feature, value in X.items():
    print(f"{feature}: {value}")

# Calculate class probabilities
print("\n=== Class Probabilities ===")
prob_class_yes = calculate_class_probability(data, class_column, "yes")
prob_class_no = calculate_class_probability(data, class_column, "no")
print(f"P(class = yes) = {prob_class_yes}")
print(f"P(class = no) = {prob_class_no}")

# Calculate conditional probabilities
print("\n=== Conditional Probabilities Given class = yes ===")
probs_yes = [calculate_conditional_probability(data, f, class_column, X[f], "yes") for f in features]

print("\n=== Conditional Probabilities Given class = no ===")
probs_no = [calculate_conditional_probability(data, f, class_column, X[f], "no") for f in features]

# Compute likelihoods
likelihood_yes = compute_likelihood(probs_yes)
likelihood_no = compute_likelihood(probs_no)

print("\n=== Likelihoods ===")
print(f"P(X | class = yes) = {likelihood_yes}")
print(f"P(X | class = no) = {likelihood_no}")

# Final probabilities
final_yes = round(likelihood_yes * prob_class_yes, 4)
final_no = round(likelihood_no * prob_class_no, 4)

print("\n=== Final Scores ===")
print(f"Final score for class = yes: {final_yes}")
print(f"Final score for class = no: {final_no}")

print("\n=== Final Prediction ===")
if final_yes > final_no:
    print("Prediction: class = yes (plays_football)")
elif final_no > final_yes:
    print("Prediction: class = no (does not buy computer)")
else:
    print("Prediction: Tie (equal probabilities)")

# === Visualization ===
classes = ["Yes", "No"]
probabilities = [prob_class_yes, prob_class_no]

plt.figure(figsize=(8, 8))
plt.bar(classes, probabilities, color=['skyblue', 'lightcoral'])
plt.xlabel("Class")
plt.ylabel("Probability")
plt.title("Naive Bayes Classification Probabilities")

# Add probability values on top of each bar
for i, prob in enumerate(probabilities):
    plt.text(i, prob + 0.01, str(prob), ha='center', va='bottom')

plt.show()
