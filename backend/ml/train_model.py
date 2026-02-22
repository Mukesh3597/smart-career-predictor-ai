import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from preprocess import load_dataset, encode_labels

ARTIFACT_DIR = "artifacts"
DATA_PATH = "data/student_career.csv"

def train():
    print("Loading dataset...")
    df = load_dataset(DATA_PATH)
    df, encoder = encode_labels(df)

    features = ["tenth_pct", "twelfth_pct", "graduation_pct", "skill_count"]
    X = df[features]
    y_class = df["career_encoded"]
    y_salary = df["salary"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_class, test_size=0.2, random_state=42
    )

    print("Training Career Classifier...")
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    print("Training Salary Regressor...")
    reg = RandomForestRegressor()
    reg.fit(X, y_salary)

    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    joblib.dump(clf, os.path.join(ARTIFACT_DIR, "career_model.pkl"))
    joblib.dump(reg, os.path.join(ARTIFACT_DIR, "salary_model.pkl"))
    joblib.dump(encoder, os.path.join(ARTIFACT_DIR, "encoder.pkl"))

    print("✅ Real-data models saved in artifacts/")

if __name__ == "__main__":
    train()