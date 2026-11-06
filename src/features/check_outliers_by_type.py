import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR / "data" / "processed"
    / "real_estate_features.csv"
)

df = pd.read_csv(DATA_PATH)

# Đổi sang triệu đồng/m2
df["price_per_m2_million"] = (
    df["price_per_m2"] / 1_000_000
)

print("========== OUTLIER ANALYSIS BY TYPE ==========")

for property_type, group in df.groupby("property_type"):

    q1 = group["price_per_m2_million"].quantile(0.25)
    q3 = group["price_per_m2_million"].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = group[
        (group["price_per_m2_million"] < lower)
        | (group["price_per_m2_million"] > upper)
    ]

    print(f"\nPROPERTY TYPE: {property_type}")
    print("Total records:", len(group))
    print("Q1:", q1)
    print("Q3:", q3)
    print("IQR:", iqr)
    print("Lower bound:", lower)
    print("Upper bound:", upper)
    print("Outliers:", len(outliers))

    print("\nTop 5 outliers:")

    print(
        outliers.nlargest(
            5, "price_per_m2_million"
        )[
            [
                "name",
                "district",
                "price_billion",
                "area_m2",
                "price_per_m2_million"
            ]
        ].to_string(index=False)
    )

print("\n========== COMPLETED ==========")