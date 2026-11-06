import pandas as pd

DATA_PATH = "data/raw/huggingface_data.csv"


def profile_dataset():
    df = pd.read_csv(DATA_PATH)

    print("\n========== 1. GIÁ TRỊ PHÂN LOẠI ==========")

    categorical_columns = [
        "source",
        "property_type",
        "province",
        "district",
        "ward"
    ]

    for col in categorical_columns:
        print(f"\n--- {col.upper()} ---")
        print("Số lượng giá trị khác nhau:", df[col].nunique())
        print(df[col].value_counts(dropna=False).head(20))

    print("\n========== 2. THỐNG KÊ DỮ LIỆU SỐ ==========")

    numeric_columns = [
        "price_vnd",
        "area_m2",
        "bedrooms",
        "bathrooms",
        "floors"
    ]

    print(df[numeric_columns].describe().to_string())

    print("\n========== 3. KIỂM TRA GIÁ TRỊ BẤT THƯỜNG ==========")

    for col in ["price_vnd", "area_m2"]:
        print(f"\n--- {col.upper()} ---")
        print("Giá trị <= 0:", (df[col] <= 0).sum())
        print("Giá trị lớn nhất:", df[col].max())
        print("Giá trị nhỏ nhất:", df[col].min())

    print("\n========== 4. KIỂM TRA NGÀY THÁNG ==========")

    for col in ["published_at", "collected_at"]:
        dates = pd.to_datetime(df[col], errors="coerce")

        print(f"\n--- {col.upper()} ---")
        print("Ngày không hợp lệ:", dates.isna().sum())
        print("Ngày sớm nhất:", dates.min())
        print("Ngày muộn nhất:", dates.max())

    print("\n========== 5. KIỂM TRA TRÙNG LẶP ==========")

    print("Trùng toàn bộ bản ghi:", df.duplicated().sum())
    print(
        "Trùng tên bất động sản:",
        df["name"].str.strip().duplicated().sum()
    )


if __name__ == "__main__":
    profile_dataset()