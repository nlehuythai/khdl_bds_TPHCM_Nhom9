
import pandas as pd
import numpy as np
from pathlib import Path


class FinalDataValidator:

    def __init__(self):
        self.file_path = Path(
            "data/processed/real_estate_text_features.csv"
        )

    def load_data(self):
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file: {self.file_path}"
            )

        return pd.read_csv(self.file_path)

    def validate_structure(self, df):
        print("\n========= 1. STRUCTURE VALIDATION =========")

        print("Số bản ghi:", len(df))
        print("Số cột:", len(df.columns))

        print("\nTên các cột:")
        print(df.columns.tolist())

        if len(df) == 1000:
            print("PASS: Đủ 1.000 bản ghi.")
        else:
            print("WARNING: Số bản ghi khác 1.000.")

        if len(df.columns) == 25:
            print("PASS: Đủ 25 cột.")
        else:
            print("WARNING: Số cột khác 25.")

    def validate_missing_values(self, df):
        print("\n========= 2. MISSING VALUE VALIDATION =========")

        missing = df.isnull().sum()

        print(missing[missing > 0])

        print(
            "\nTổng số ô thiếu:",
            int(missing.sum())
        )

    def validate_duplicates(self, df):
        print("\n========= 3. DUPLICATE VALIDATION =========")

        duplicate_rows = df.duplicated().sum()

        print("Số dòng trùng lặp:", duplicate_rows)

        duplicate_names = (
            df["name"].astype(str).str.strip().duplicated().sum()
        )

        print("Số tên tin đăng trùng:", duplicate_names)

    def validate_numeric_features(self, df):
        print("\n========= 4. NUMERIC FEATURE VALIDATION =========")

        expected_price_billion = df["price_vnd"] / 1e9

        expected_price_per_m2 = (
            df["price_vnd"] / df["area_m2"]
        )

        price_billion_ok = np.isclose(
            df["price_billion"],
            expected_price_billion,
            rtol=1e-9
        ).all()

        price_per_m2_ok = np.isclose(
            df["price_per_m2"],
            expected_price_per_m2,
            rtol=1e-9
        ).all()

        print(
            "price_billion:",
            "PASS" if price_billion_ok else "FAIL"
        )

        print(
            "price_per_m2:",
            "PASS" if price_per_m2_ok else "FAIL"
        )

        invalid_price = (
            (df["price_vnd"] <= 0)
            | (df["area_m2"] <= 0)
        ).sum()

        print("Giá hoặc diện tích không hợp lệ:", invalid_price)

    def validate_outliers(self, df):
        print("\n========= 5. OUTLIER VALIDATION =========")

        print(
            "Số outliers:",
            int(df["is_outlier_price_per_m2"].sum())
        )

        print("\nPhân bố theo loại bất động sản:")

        print(
            df.groupby("property_type")[
                "is_outlier_price_per_m2"
            ].agg(["count", "sum"])
        )

    def validate_text_features(self, df):
        print("\n========= 6. TEXT FEATURE VALIDATION =========")

        description = (
            df["description"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        expected_length = description.str.len()
        expected_word_count = description.str.split().str.len()

        length_ok = (
            df["description_length"] == expected_length
        ).all()

        word_count_ok = (
            df["description_word_count"] == expected_word_count
        ).all()

        print(
            "description_length:",
            "PASS" if length_ok else "FAIL"
        )

        print(
            "description_word_count:",
            "PASS" if word_count_ok else "FAIL"
        )

        print(
            "has_description:",
            "PASS" if (
                df["has_description"] == description.ne("").astype(int)
            ).all() else "FAIL"
        )

        expected_location = (
            df["district"].notna()
            | df["ward"].notna()
        ).astype(int)

        print(
            "has_location_info:",
            "PASS" if (
                df["has_location_info"] == expected_location
            ).all() else "FAIL"
        )

        print(
            "has_bedrooms:",
            "PASS" if (
                df["has_bedrooms"] == df["bedrooms"].notna().astype(int)
            ).all() else "FAIL"
        )

        print(
            "has_bathrooms:",
            "PASS" if (
                df["has_bathrooms"] == df["bathrooms"].notna().astype(int)
            ).all() else "FAIL"
        )

    def validate_dates(self, df):
        print("\n========= 7. DATE VALIDATION =========")

        published_at = pd.to_datetime(
            df["published_at"],
            format="mixed",
            errors="coerce"
        )

        collected_at = pd.to_datetime(
            df["collected_at"],
            format="mixed",
            errors="coerce"
        )

        print(
            "Ngày đăng không hợp lệ:",
            int(published_at.isna().sum())
        )

        print(
            "Ngày thu thập không hợp lệ:",
            int(collected_at.isna().sum())
        )

        year_ok = (
            df["published_year"].to_numpy()
            == published_at.dt.year.to_numpy()
        ).all()

        month_ok = (
            df["published_month"].to_numpy()
            == published_at.dt.month.to_numpy()
        ).all()

        print(
            "published_year:",
            "PASS" if year_ok else "FAIL"
        )

        print(
            "published_month:",
            "PASS" if month_ok else "FAIL"
        )

    def run(self):
        print("========= FINAL DATA QUALITY VALIDATION =========")

        df = self.load_data()

        self.validate_structure(df)
        self.validate_missing_values(df)
        self.validate_duplicates(df)
        self.validate_numeric_features(df)
        self.validate_outliers(df)
        self.validate_text_features(df)
        self.validate_dates(df)

        print("\n========= VALIDATION COMPLETED =========")


if __name__ == "__main__":
    validator = FinalDataValidator()
    validator.run()
