import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR / "data" / "processed"
    / "real_estate_cleaned.csv"
)

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["published_at", "collected_at"]
)

print("========== DATA VERIFICATION ==========")

# 1. Kiểm tra kích thước
print("\n1. Dataset shape:")
print(df.shape)

# 2. Kiểm tra dữ liệu trùng lặp
print("\n2. Duplicate rows:")
print(df.duplicated().sum())

# 3. Kiểm tra floors theo loại bất động sản
print("\n3. Floors by property type:")
print(
    df.groupby("property_type")["floors"]
    .agg(["count", "min", "max"])
)

# 4. Kiểm tra căn hộ còn floors hay không
print("\n4. Apartment floors remaining:")
apartment_mask = (
    df["property_type"] == "Căn hộ chung cư"
)

print(df.loc[apartment_mask, "floors"].notna().sum())

# 5. Kiểm tra ngày tháng
print("\n5. Invalid dates:")
for col in ["published_at", "collected_at"]:
    print(
        col,
        pd.to_datetime(df[col], errors="coerce").isna().sum()
    )

# 6. Kiểm tra kiểu dữ liệu
print("\n6. Data types:")
print(df.dtypes)

print("\n========== VERIFICATION COMPLETED ==========")