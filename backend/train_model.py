import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(current_dir, ".."))
    data_path = os.path.join(project_dir, "data", "nutrition_data.csv")

    print("📄 Loading data from:", data_path)
    df = pd.read_csv(data_path)
    print("✅ Data loaded. Shape:", df.shape)

    # Show how many samples per class
    print("\n🔢 Class distribution in dataset (deficiency_label):")
    print(df["deficiency_label"].value_counts().sort_index())

    feature_cols = [
        "age",
        "gender",
        "height",
        "weight",
        "diet_type",
        "sunlight",
        "fatigue",
        "hair_fall",
        "pale_skin",
        "bone_pain",
        "cracked_lips"
    ]
    target_col = "deficiency_label"

    # Safety: ensure columns exist
    for col in feature_cols + [target_col]:
        if col not in df.columns:
            raise ValueError(f"Missing column in CSV: {col}")

    X = df[feature_cols]
    y = df[target_col]

    # Stratified split (we now have enough rows)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("\n📚 Train size:", X_train.shape, " Test size:", X_test.shape)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # You can tweak k if you want
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)

    y_pred = knn.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n🎯 Accuracy on test set: {acc:.4f}")
    print("\n📊 Classification report:\n", classification_report(y_test, y_pred))

    # Show which classes the model actually predicted
    print("🧪 Unique predicted classes in test set:", sorted(set(y_pred)))

    artifact = {
        "model": knn,
        "scaler": scaler,
        "columns": feature_cols
    }

    model_path = os.path.join(current_dir, "model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(artifact, f)

    print("\n✅ New model saved to:", model_path)

if __name__ == "__main__":
    main()
