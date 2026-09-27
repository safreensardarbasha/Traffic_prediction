import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


# ============================================
# LOAD DATASET
# ============================================

data = pd.read_csv("data.csv")

print("================================")
print("TRAFFIC DATASET")
print("================================")

print(data.head())

print("\nCongestion Distribution:")
print(data["congestion"].value_counts())


# ============================================
# FEATURES
# ============================================

X = data[
    [
        "vehicle_count",
        "average_speed",
        "road_capacity",
        "hour"
    ]
]

y = data["congestion"]


# ============================================
# TRAIN / TEST SPLIT
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================
# RANDOM FOREST MODEL
# ============================================

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ============================================
# MODEL EVALUATION
# ============================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n================================")
print("TRAFFIC AI MODEL TRAINED")
print("================================")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# ============================================
# MODEL CLASSES
# ============================================

print("Model Classes:")
print(model.classes_)


# ============================================
# SAVE MODEL
# ============================================

joblib.dump(
    model,
    "traffic_model.pkl"
)

print("\n================================")
print("MODEL SAVED SUCCESSFULLY")
print("================================")

print("File: traffic_model.pkl")


# ============================================
# TEST PREDICTIONS
# ============================================

print("\n================================")
print("TEST PREDICTIONS")
print("================================")


test_cases = [
    [250, 55, 1800, 10],
    [600, 43, 1700, 8],
    [800, 38, 1700, 18],
    [1000, 30, 1800, 8]
]


for case in test_cases:

    result = model.predict([case])[0]

    print(
        f"Vehicles: {case[0]} | "
        f"Speed: {case[1]} | "
        f"Hour: {case[3]} | "
        f"Prediction: {result}"
    )