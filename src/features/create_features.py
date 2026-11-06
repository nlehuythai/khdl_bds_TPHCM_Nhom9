import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR / "data" / "processed"
    / "real_estate_cleaned.csv"
)

OUTPUT_PATH = (
    BASE_DIR / "data" / "processed"
    / "real_estate_features.csv"
)


class RealEstateFeatureEngineer:

    def __init__(self, data):
        self.df = data.copy()
        self.feature_log = []

    # 1. Tạo thuộc tính giá theo tỷ đồng
    def create_price_billion(self):
        self.df["price_billion"] = (
            self.df["price_vnd"] / 1_000_000_000
        )

        self.feature_log.append(
            "Tạo thuộc tính price_billion"
        )

    # 2. Tạo thuộc tính giá trên mỗi mét vuông
    def create_price_per_m2(self):
        self.df["price_per_m2"] = (
            self.df["price_vnd"] / self.df["area_m2"]
        )

        self.feature_log.append(
            "Tạo thuộc tính price_per_m2"
        )

    # 3. Trích xuất năm đăng tin
    def create_published_year(self):
        self.df["published_at"] = pd.to_datetime(
            self.df["published_at"],
            format="mixed",
            errors="coerce"
        )

        self.df["published_year"] = (
            self.df["published_at"].dt.year
        )

        self.feature_log.append(
            "Tạo thuộc tính published_year"
        )

    # 4. Trích xuất tháng đăng tin
    def create_published_month(self):
        self.df["published_month"] = (
            self.df["published_at"].dt.month
        )

        self.feature_log.append(
            "Tạo thuộc tính published_month"
        )

    # Thực hiện toàn bộ Feature Engineering
    def transform(self):
        self.create_price_billion()
        self.create_price_per_m2()
        self.create_published_year()
        self.create_published_month()

        return self.df

    # Hiển thị nhật ký
    def show_feature_log(self):
        print("\n========== FEATURE ENGINEERING LOG ==========")

        for index, message in enumerate(
            self.feature_log, start=1
        ):
            print(f"{index}. {message}")


def run_feature_engineering():

    print("Loading cleaned dataset...")

    df = pd.read_csv(INPUT_PATH)

    print("Original shape:", df.shape)

    engineer = RealEstateFeatureEngineer(df)

    featured_df = engineer.transform()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    featured_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    engineer.show_feature_log()

    print("\n========== FEATURE ENGINEERING SUMMARY ==========")

    print("Original rows:", len(df))
    print("Featured rows:", len(featured_df))

    print("Original columns:", len(df.columns))
    print("Featured columns:", len(featured_df.columns))

    print("\nNew features:")

    new_features = [
        "price_billion",
        "price_per_m2",
        "published_year",
        "published_month"
    ]

    print(featured_df[new_features].head(10))

    print("\nMissing values in new features:")

    print(featured_df[new_features].isnull().sum())

    print("\nOutput:", OUTPUT_PATH)


if __name__ == "__main__":
    run_feature_engineering()