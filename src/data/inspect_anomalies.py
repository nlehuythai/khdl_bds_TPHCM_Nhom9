import pandas as pd

DATA_PATH = "data/raw/huggingface_data.csv"


def inspect_anomalies():
    df = pd.read_csv(DATA_PATH)

    columns = [
        "name",
        "property_type",
        "district",
        "ward",
        "price_vnd",
        "area_m2",
        "bedrooms",
        "bathrooms",
        "floors"
    ]

    # 1. Kiểm tra bất động sản có giá cao nhất
    print("\n========== TOP 10 GIÁ CAO NHẤT ==========")

    print(
        df.nlargest(10, "price_vnd")[columns]
        .to_string(index=False)
    )

    # 2. Kiểm tra bất động sản có diện tích lớn nhất
    print("\n========== TOP 10 DIỆN TÍCH LỚN NHẤT ==========")

    print(
        df.nlargest(10, "area_m2")[columns]
        .to_string(index=False)
    )

    # 3. Kiểm tra số phòng ngủ bất thường
    print("\n========== BEDROOMS >= 10 ==========")

    print(
        df[df["bedrooms"] >= 10][columns]
        .to_string(index=False)
    )

    # 4. Kiểm tra số phòng tắm bất thường
    print("\n========== BATHROOMS >= 10 ==========")

    print(
        df[df["bathrooms"] >= 10][columns]
        .to_string(index=False)
    )

    # 5. Kiểm tra số tầng bất thường
    print("\n========== FLOORS >= 10 ==========")

    print(
        df[df["floors"] >= 10][columns]
        .to_string(index=False)
    )

    # 6. Kiểm tra ngày đăng không hợp lệ
    print("\n========== INVALID PUBLISHED_AT ==========")

    dates = pd.to_datetime(
        df["published_at"],
        errors="coerce"
    )

    print(
        df.loc[dates.isna(), ["name", "published_at"]]
        .to_string(index=False)
    )

    # 7. Kiểm tra toàn bộ giá trị district
    print("\n========== ALL DISTRICTS ==========")

    print(
        sorted(df["district"].dropna().unique(), key=str)
    )


if __name__ == "__main__":
    inspect_anomalies()