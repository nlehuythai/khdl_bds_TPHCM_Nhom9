import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR / "data" / "processed"
    / "real_estate_features.csv"
)

df = pd.read_csv(DATA_PATH)

# Đổi đơn vị từ VND/m² sang triệu đồng/m²
df["price_per_m2_million"] = (
    df["price_per_m2"] / 1_000_000
)

print("========== PRICE PER M2 ANALYSIS ==========")

# 1. Thống kê tổng quan
print("\n1. Overall statistics (million VND/m2):")

print(
    df["price_per_m2_million"].describe(
        percentiles=[0.25, 0.5, 0.75, 0.90, 0.95, 0.99]
    )
)

# 2. So sánh theo loại bất động sản
print("\n2. Statistics by property type:")

print(
    df.groupby("property_type")["price_per_m2_million"]
    .describe()
)

# 3. Xác định ngoại lệ bằng IQR
q1 = df["price_per_m2_million"].quantile(0.25)
q3 = df["price_per_m2_million"].quantile(0.75)

iqr = q3 - q1

upper_bound = q3 + 1.5 * iqr
lower_bound = q1 - 1.5 * iqr

outliers = df[
    (df["price_per_m2_million"] < lower_bound)
    | (df["price_per_m2_million"] > upper_bound)
]

print("\n3. IQR outlier analysis:")
print("Q1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)
print("Number of outliers:", len(outliers))

# 4. Top 10 giá/m2 cao nhất
print("\n4. Top 10 highest price per m2:")

print(
    df.nlargest(10, "price_per_m2_million")[
        [
            "name",
            "property_type",
            "district",
            "price_billion",
            "area_m2",
            "price_per_m2_million"
        ]
    ].to_string(index=False)
)

# 5. Bottom 10 giá/m2 thấp nhất
print("\n5. Bottom 10 lowest price per m2:")

print(
    df.nsmallest(10, "price_per_m2_million")[
        [
            "name",
            "property_type",
            "district",
            "price_billion",
            "area_m2",
            "price_per_m2_million"
        ]
    ].to_string(index=False)
)