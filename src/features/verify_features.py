import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR / "data" / "processed"
    / "real_estate_features.csv"
)

df = pd.read_csv(DATA_PATH)

print("========== FEATURE VERIFICATION ==========")

print("\n1. Dataset shape:")
print(df.shape)

print("\n2. New feature statistics:")
print(
    df[
        [
            "price_billion",
            "price_per_m2",
            "published_year",
            "published_month"
        ]
    ].describe()
)

print("\n3. Sample data:")
print(
    df[
        [
            "name",
            "price_billion",
            "price_per_m2",
            "published_year",
            "published_month"
        ]
    ].head(10).to_string(index=False)
)

print("\n4. Missing values:")
print(
    df[
        [
            "price_billion",
            "price_per_m2",
            "published_year",
            "published_month"
        ]
    ].isnull().sum()
)

print("\n========== VERIFICATION COMPLETED ==========")