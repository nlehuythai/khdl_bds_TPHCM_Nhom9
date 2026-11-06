
import pandas as pd
from pathlib import Path


class TextFeatureEngineer:

    def __init__(self):
        self.input_path = Path(
            "data/processed/real_estate_features_flagged.csv"
        )

        self.output_path = Path(
            "data/processed/real_estate_text_features.csv"
        )

    def load_data(self):
        if not self.input_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file: {self.input_path}"
            )

        df = pd.read_csv(self.input_path)

        print("Đã tải dữ liệu thành công.")
        print(f"Số bản ghi: {len(df)}")

        return df

    def extract_text_features(self, df):

        description = (
            df["description"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # Độ dài mô tả
        df["description_length"] = description.str.len()

        # Số lượng từ trong mô tả
        df["description_word_count"] = (
            description.str.split().str.len()
        )

        # Có mô tả hay không
        df["has_description"] = (
            description.ne("").astype(int)
        )

        # Có thông tin vị trí hay không
        has_district = (
            df["district"].notna()
            & df["district"].astype(str).str.strip().ne("")
        )

        has_ward = (
            df["ward"].notna()
            & df["ward"].astype(str).str.strip().ne("")
        )

        df["has_location_info"] = (
            has_district | has_ward
        ).astype(int)

        # Có thông tin phòng ngủ hay không
        df["has_bedrooms"] = (
            df["bedrooms"].notna()
        ).astype(int)

        # Có thông tin phòng tắm hay không
        df["has_bathrooms"] = (
            df["bathrooms"].notna()
        ).astype(int)

        return df

    def save_data(self, df):

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_csv(
            self.output_path,
            index=False,
            encoding="utf-8-sig"
        )

        print("\nĐã lưu dữ liệu:", self.output_path)

    def show_summary(self, df):

        feature_columns = [
            "description_length",
            "description_word_count",
            "has_description",
            "has_location_info",
            "has_bedrooms",
            "has_bathrooms"
        ]

        print("\n========= TEXT FEATURE SUMMARY =========")

        for column in feature_columns:
            print(f"\n{column}")

            if column.startswith("has_"):
                print(df[column].value_counts().sort_index())
            else:
                print(df[column].describe())

        print("\n========= FINAL SUMMARY =========")
        print("Tổng số bản ghi:", len(df))
        print("Tổng số cột:", len(df.columns))

    def run(self):

        df = self.load_data()

        df = self.extract_text_features(df)

        self.show_summary(df)

        self.save_data(df)


if __name__ == "__main__":
    engineer = TextFeatureEngineer()
    engineer.run()
