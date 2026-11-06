
import pandas as pd

df = pd.read_csv("data/raw/raw_data.csv")

print("=" * 50)
print("SOURCE DATA AUDIT")
print("=" * 50)

print("\n1. So luong ban ghi theo nguon:")
print(df["source"].value_counts(dropna=False))

print("\n2. Cac cot hien co:")
print(df.columns.tolist())

print("\n3. Kiem tra kha nang truy xuat nguon:")

if "source_url" in df.columns:
    print("Da co cot source_url")
    print("So URL hop le:", df["source_url"].notna().sum())
else:
    print("Chua co cot source_url")

print("\n4. Kiem tra cac truong quan trong:")
columns = [
    "name",
    "property_type",
    "province",
    "district",
    "price_vnd",
    "area_m2",
    "published_at"
]

for col in columns:
    if col in df.columns:
        print(f"{col}: {df[col].notna().sum()}/{len(df)}")

print("\n5. Phan bo loai bat dong san:")
print(df["property_type"].value_counts(dropna=False))

