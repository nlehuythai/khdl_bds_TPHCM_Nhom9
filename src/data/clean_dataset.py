
import pandas as pd
from pathlib import Path


# ==============================
# CONFIGURATION
# ==============================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "huggingface_data.csv"

PROCESSED_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DATA_PATH = PROCESSED_DIR / "real_estate_cleaned.csv"


# ==============================
# DATA CLEANER
# ==============================

class RealEstateCleaner:

    DISTRICT_MAPPING = {
        "1": "Quận 1",
        "3": "Quận 3",
        "4": "Quận 4",
        "5": "Quận 5",
        "6": "Quận 6",
        "7": "Quận 7",
        "8": "Quận 8",
        "10": "Quận 10",
        "11": "Quận 11",
        "12": "Quận 12"
    }

    def __init__(self, data):
        self.df = data.copy()
        self.cleaning_log = []

    def remove_empty_columns(self):
        empty_columns = [
            col for col in self.df.columns
            if self.df[col].isna().all()
        ]

        self.df.drop(columns=empty_columns, inplace=True)

        self.cleaning_log.append(
            f"Loại bỏ các cột rỗng hoàn toàn: {empty_columns}"
        )

    def normalize_text(self):
        text_columns = [
            "source",
            "name",
            "property_type",
            "province",
            "district",
            "ward",
            "description"
        ]

        for col in text_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(
                    lambda value: (
                        value.strip()
                        if isinstance(value, str)
                        else value
                    )
                )

        self.cleaning_log.append(
            "Chuẩn hóa khoảng trắng ở các cột văn bản"
        )

    def normalize_district(self):
        self.df["district"] = (
            self.df["district"]
            .astype("string")
            .str.strip()
            .replace(self.DISTRICT_MAPPING)
        )

        self.cleaning_log.append(
            "Chuẩn hóa cách ghi tên quận"
        )

    def convert_datetime(self):
        datetime_columns = [
            "published_at",
            "collected_at"
        ]

        for col in datetime_columns:
            self.df[col] = pd.to_datetime(
                self.df[col],
                format="mixed",
                errors="coerce"
            )

        self.cleaning_log.append(
            "Chuyển đổi published_at và collected_at sang datetime"
        )

    def validate_numeric_values(self):
        numeric_columns = [
            "price_vnd",
            "area_m2",
            "bedrooms",
            "bathrooms",
            "floors"
        ]

        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(
                    self.df[col],
                    errors="coerce"
                )

        self.cleaning_log.append(
            "Đảm bảo các thuộc tính số có kiểu dữ liệu phù hợp"
        )

    def clean(self):
        self.remove_empty_columns()
        self.normalize_text()
        self.normalize_district()
        self.convert_datetime()
        self.validate_numeric_values()
        self.handle_apartment_floors()
        return self.df

    def show_cleaning_log(self):
        print("\n========== CLEANING LOG ==========")

        for index, message in enumerate(
            self.cleaning_log,
            start=1
        ):
            print(f"{index}. {message}")
    def handle_apartment_floors(self):
        apartment_mask = (
            self.df["property_type"] == "Căn hộ chung cư"
        ) & (self.df["floors"] >= 10)

        affected_rows = apartment_mask.sum()

        self.df.loc[apartment_mask, "floors"] = pd.NA

        self.cleaning_log.append(
          f"Loại bỏ giá trị floors của {affected_rows} căn hộ chung cư"
        )

# ==============================
# PIPELINE
# ==============================

def run_cleaning():
    print("Loading raw dataset...")

    df = pd.read_csv(RAW_DATA_PATH)

    print("Original shape:", df.shape)

    cleaner = RealEstateCleaner(df)

    cleaned_df = cleaner.clean()

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    cleaned_df.to_csv(
        OUTPUT_DATA_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    cleaner.show_cleaning_log()

    print("\n========== CLEANING SUMMARY ==========")

    print("Original rows:", len(df))
    print("Cleaned rows:", len(cleaned_df))
    print("Original columns:", len(df.columns))
    print("Cleaned columns:", len(cleaned_df.columns))

    print("\nMissing values after cleaning:")
    print(cleaned_df.isnull().sum())

    print("\nOutput:", OUTPUT_DATA_PATH)


if __name__ == "__main__":
    run_cleaning()
