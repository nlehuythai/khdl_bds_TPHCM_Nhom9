import pandas as pd
from pathlib import Path


class OutlierMarker:
    def __init__(self):
        self.input_path = Path(
            "data/processed/real_estate_features.csv"
        )

        self.output_path = Path(
            "data/processed/real_estate_features_flagged.csv"
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

    def mark_outliers(self, df):
        df["is_outlier_price_per_m2"] = 0

        for property_type, group in df.groupby("property_type"):
            q1 = group["price_per_m2"].quantile(0.25)
            q3 = group["price_per_m2"].quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            mask = (
                (df["property_type"] == property_type)
                & (
                    (df["price_per_m2"] < lower_bound)
                    | (df["price_per_m2"] > upper_bound)
                )
            )

            df.loc[mask, "is_outlier_price_per_m2"] = 1

            print(f"\nLoại bất động sản: {property_type}")
            print(f"Q1: {q1:.2f}")
            print(f"Q3: {q3:.2f}")
            print(f"IQR: {iqr:.2f}")
            print(f"Ngưỡng dưới: {lower_bound:.2f}")
            print(f"Ngưỡng trên: {upper_bound:.2f}")
            print(f"Số outliers: {mask.sum()}")

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

    def run(self):
        df = self.load_data()

        df = self.mark_outliers(df)

        self.save_data(df)

        print("\n========= FINAL SUMMARY =========")
        print("Tổng số bản ghi:", len(df))
        print(
            "Bản ghi bình thường:",
            (df["is_outlier_price_per_m2"] == 0).sum()
        )
        print(
            "Bản ghi ngoại lệ:",
            (df["is_outlier_price_per_m2"] == 1).sum()
        )
        print("Số cột:", len(df.columns))


if __name__ == "__main__":
    marker = OutlierMarker()
    marker.run()