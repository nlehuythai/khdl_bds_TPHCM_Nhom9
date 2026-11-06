
import pandas as pd
import numpy as np
import os

# ==============================
# 1. CONFIGURATION
# ==============================

INPUT_FILE = "data/raw/raw_data.csv"
OUTPUT_DIR = "data/quality"

ALLOWED_TYPES = ["Nhà", "Căn hộ chung cư"]

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================
# 2. LOAD DATA
# ==============================

def load_data():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Khong tim thay file: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print("=" * 55)
    print("DATA QUALITY ASSESSMENT")
    print("=" * 55)

    print(f"Tong so ban ghi: {len(df)}")
    print(f"Tong so cot: {len(df.columns)}")

    return df


# ==============================
# 3. CHECK STRUCTURE
# ==============================

def check_structure(df):
    print("\n[1] KIEM TRA CAU TRUC DU LIEU")

    print("\nDanh sach cot:")
    for col in df.columns:
        print(f"- {col}: {df[col].dtype}")

    print("\nSo luong ban ghi:", len(df))
    print("So luong cot:", len(df.columns))

    expected_columns = [
        "source", "name", "property_type",
        "province", "district", "ward",
        "price_vnd", "area_m2",
        "bedrooms", "bathrooms", "floors",
        "description", "published_at"
    ]

    missing_columns = [
        col for col in expected_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("Thieu cot:", missing_columns)
    else:
        print("Day du cac cot mong doi.")


# ==============================
# 4. CHECK MISSING VALUES
# ==============================

def check_missing(df):
    print("\n[2] KIEM TRA DU LIEU THIEU")

    missing_count = df.isnull().sum()
    missing_percent = (
        df.isnull().mean() * 100
    ).round(2)

    report = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percent": missing_percent
    })

    report = report.sort_values(
        by="missing_count",
        ascending=False
    )

    print(report)

    print(
        "\nTong so o du lieu thieu:",
        int(missing_count.sum())
    )

    report.to_csv(
        f"{OUTPUT_DIR}/missing_report.csv",
        encoding="utf-8-sig"
    )

    return report


# ==============================
# 5. CHECK DUPLICATES
# ==============================

def check_duplicates(df):
    print("\n[3] KIEM TRA BAN GHI TRUNG LAP")

    duplicate_count = df.duplicated().sum()

    print(
        "So ban ghi trung lap hoan toan:",
        duplicate_count
    )

    duplicate_rows = df[df.duplicated(keep=False)]

    duplicate_rows.to_csv(
        f"{OUTPUT_DIR}/duplicate_records.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return duplicate_count


# ==============================
# 6. CHECK PROPERTY TYPE
# ==============================

def check_property_type(df):
    print("\n[4] KIEM TRA LOAI BAT DONG SAN")

    counts = df["property_type"].value_counts(
        dropna=False
    )

    print(counts)

    invalid = df[
        ~df["property_type"].isin(ALLOWED_TYPES)
    ]

    print(
        "\nSo ban ghi sai hoac khong thuoc loai cho phep:",
        len(invalid)
    )

    invalid.to_csv(
        f"{OUTPUT_DIR}/invalid_property_type.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return counts, len(invalid)


# ==============================
# 7. CHECK PRICE AND AREA
# ==============================

def check_price_area(df):
    print("\n[5] KIEM TRA GIA VA DIEN TICH")

    price = pd.to_numeric(
        df["price_vnd"],
        errors="coerce"
    )

    area = pd.to_numeric(
        df["area_m2"],
        errors="coerce"
    )

    invalid_price = df[
        price.isna() | (price <= 0)
    ]

    invalid_area = df[
        area.isna() | (area <= 0)
    ]

    print("Gia khong hop le:", len(invalid_price))
    print("Dien tich khong hop le:", len(invalid_area))

    invalid_price.to_csv(
        f"{OUTPUT_DIR}/invalid_price.csv",
        index=False,
        encoding="utf-8-sig"
    )

    invalid_area.to_csv(
        f"{OUTPUT_DIR}/invalid_area.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return price, area, len(invalid_price), len(invalid_area)


# ==============================
# 8. CHECK NUMERIC ATTRIBUTES
# ==============================

def check_numeric_attributes(df):
    print("\n[6] KIEM TRA THUOC TINH SO")

    columns = [
        "bedrooms",
        "bathrooms",
        "floors"
    ]

    invalid_reports = []

    for col in columns:
        values = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        invalid = (
            values.notna()
            & (
                (values < 0)
                | (values % 1 != 0)
            )
        )

        invalid_count = int(invalid.sum())

        print(f"{col}: {invalid_count} gia tri bat thuong")

        for index in df.index[invalid]:
            invalid_reports.append({
                "row_index": index,
                "column": col,
                "value": df.loc[index, col]
            })

    pd.DataFrame(invalid_reports).to_csv(
        f"{OUTPUT_DIR}/invalid_numeric_attributes.csv",
        index=False,
        encoding="utf-8-sig"
    )


# ==============================
# 9. CHECK DATE
# ==============================

def check_date(df):
    print("\n[7] KIEM TRA NGAY DANG TIN")

    dates = pd.to_datetime(
        df["published_at"],
        errors="coerce"
    )

    invalid_count = int(dates.isna().sum())

    print("Ngay khong hop le:", invalid_count)

    return invalid_count


# ==============================
# 10. CHECK OUTLIERS USING IQR
# ==============================

def detect_outliers(df, column):
    values = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if len(values) < 4:
        return pd.Series(False, index=df.index)

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    result = (
        pd.to_numeric(df[column], errors="coerce")
        .lt(lower_bound)
        | pd.to_numeric(df[column], errors="coerce")
        .gt(upper_bound)
    )

    return result.fillna(False)


def check_outliers(df):
    print("\n[8] PHAT HIEN GIA TRI BAT THUONG")

    columns = ["price_vnd", "area_m2"]

    reports = []

    for col in columns:
        outliers = detect_outliers(df, col)

        count = int(outliers.sum())

        print(f"{col}: {count} gia tri nghi ngo bat thuong")

        for index in df.index[outliers]:
            reports.append({
                "row_index": index,
                "column": col,
                "value": df.loc[index, col]
            })

    pd.DataFrame(reports).to_csv(
        f"{OUTPUT_DIR}/outlier_report.csv",
        index=False,
        encoding="utf-8-sig"
    )


# ==============================
# 11. STATISTICAL SUMMARY
# ==============================

def statistical_summary(df):
    print("\n[9] THONG KE MO TA")

    columns = [
        "price_vnd",
        "area_m2",
        "bedrooms",
        "bathrooms",
        "floors"
    ]

    summary = df[columns].describe().round(2)

    print(summary)

    summary.to_csv(
        f"{OUTPUT_DIR}/statistical_summary.csv",
        encoding="utf-8-sig"
    )


# ==============================
# 12. FINAL QUALITY REPORT
# ==============================

def final_report(
    df,
    missing_report,
    duplicate_count,
    invalid_type_count,
    invalid_price_count,
    invalid_area_count,
    invalid_date_count
):
    report = pd.DataFrame({
        "Metric": [
            "Total Records",
            "Total Columns",
            "Missing Values",
            "Duplicate Records",
            "Invalid Property Type",
            "Invalid Price",
            "Invalid Area",
            "Invalid Published Date"
        ],
        "Value": [
            len(df),
            len(df.columns),
            int(missing_report["missing_count"].sum()),
            duplicate_count,
            invalid_type_count,
            invalid_price_count,
            invalid_area_count,
            invalid_date_count
        ]
    })

    print("\n" + "=" * 55)
    print("FINAL DATA QUALITY REPORT")
    print("=" * 55)

    print(report.to_string(index=False))

    report.to_csv(
        f"{OUTPUT_DIR}/data_quality_report.csv",
        index=False,
        encoding="utf-8-sig"
    )


# ==============================
# 13. MAIN
# ==============================

def main():
    df = load_data()

    check_structure(df)

    missing_report = check_missing(df)

    duplicate_count = check_duplicates(df)

    _, invalid_type_count = check_property_type(df)

    _, _, invalid_price_count, invalid_area_count = (
        check_price_area(df)
    )

    check_numeric_attributes(df)

    invalid_date_count = check_date(df)

    check_outliers(df)

    statistical_summary(df)

    final_report(
        df,
        missing_report,
        duplicate_count,
        invalid_type_count,
        invalid_price_count,
        invalid_area_count,
        invalid_date_count
    )

    print("\nDa hoan thanh danh gia chat luong du lieu.")
    print("Ket qua duoc luu tai:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
