import pandas as pd
from sklearn.preprocessing import LabelEncoder


def load_dataset(csv_path: str):
    df = pd.read_csv(csv_path)

    needed = [
        "tenth_pct", "twelfth_pct", "graduation_pct",
        "skill_count", "career", "salary"
    ]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing columns: {missing}")

    df = df.dropna(subset=needed)

    for col in ["tenth_pct", "twelfth_pct", "graduation_pct", "skill_count", "salary"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["tenth_pct", "twelfth_pct", "graduation_pct", "skill_count", "salary"])
    df["skill_count"] = df["skill_count"].astype(int)

    return df


def encode_labels(df):
    encoder = LabelEncoder()
    df["career_encoded"] = encoder.fit_transform(df["career"].astype(str))
    return df, encoder