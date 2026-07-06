import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==========================================================
# CREATE FOLDERS
# ==========================================================

os.makedirs("graphs", exist_ok=True)
os.makedirs("models", exist_ok=True)

# ==========================================================
# COLUMN NAMES
# ==========================================================

columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted",
    "num_root","num_file_creations","num_shells","num_access_files",
    "num_outbound_cmds","is_host_login","is_guest_login","count",
    "srv_count","serror_rate","srv_serror_rate","rerror_rate",
    "srv_rerror_rate","same_srv_rate","diff_srv_rate",
    "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label","difficulty"
]

# ==========================================================
# LOAD DATA
# ==========================================================

print("="*60)
print("Loading Dataset...")
print("="*60)

df = pd.read_csv("data/KDDTrain+.txt", names=columns)

print("Dataset Loaded Successfully")
print("Shape :", df.shape)

# ==========================================================
# BINARY CLASSIFICATION
# ==========================================================

df["label"] = df["label"].apply(
    lambda x: "normal" if x == "normal" else "attack"
)

# ==========================================================
# ENCODE CATEGORICAL DATA
# ==========================================================

encoder = LabelEncoder()

categorical = [
    "protocol_type",
    "service",
    "flag"
]

for col in categorical:
    df[col] = encoder.fit_transform(df[col])

df["label"] = encoder.fit_transform(df["label"])

print("\nData Encoding Completed.")

# ==========================================================
# EDA
# ==========================================================

print("\nGenerating Graphs...")

# Attack Distribution
plt.figure(figsize=(8,5))
sns.countplot(x=df["label"])
plt.title("Attack Distribution")
plt.savefig("graphs/attack_distribution.png")
plt.close()

# Protocol Distribution
plt.figure(figsize=(8,5))
sns.countplot(x=df["protocol_type"])
plt.title("Protocol Distribution")
plt.savefig("graphs/protocol_distribution.png")
plt.close()

# Correlation Heatmap
plt.figure(figsize=(14,10))
corr = df.corr(numeric_only=True)
sns.heatmap(corr)
plt.title("Correlation Heatmap")
plt.savefig("graphs/correlation_heatmap.png")
plt.close()

print("Graphs Saved Successfully!")

# ==========================================================
# FEATURES
# ==========================================================

X = df.drop("label", axis=1)

y = df["label"]

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining Samples :", X_train.shape)
print("Testing Samples :", X_test.shape)

# ==========================================================
# MODELS
# ==========================================================

models = {
    "Logistic Regression": LogisticRegression(max_iter=500),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),
    "KNN": KNeighborsClassifier()
}

results = {}

best_accuracy = 0
best_model = None
best_name = ""

print("\nTraining Models...\n")

for name, model in models.items():

    print("="*50)
    print(name)
    print("="*50)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    results[name] = accuracy

    print("Accuracy :", round(accuracy*100,2), "%")

    print("\nConfusion Matrix")

    print(confusion_matrix(y_test, predictions))

    print("\nClassification Report")

    print(classification_report(y_test, predictions))

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_name = name

# ==========================================================
# SAVE BEST MODEL
# ==========================================================

joblib.dump(
    best_model,
    "models/network_intrusion_model.pkl"
)

print("\n" + "="*60)
print("BEST MODEL :", best_name)
print("BEST ACCURACY :", round(best_accuracy*100,2), "%")
print("="*60)

print("\nModel Saved Successfully!")

# ==========================================================
# ACCURACY GRAPH
# ==========================================================

plt.figure(figsize=(8,5))

plt.bar(results.keys(), results.values())

plt.xticks(rotation=20)

plt.ylabel("Accuracy")

plt.title("Model Comparison")

plt.savefig("graphs/model_comparison.png")

plt.show()

print("\nProject Completed Successfully!")