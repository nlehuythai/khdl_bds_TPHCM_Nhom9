
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


class LocationAnalysisEDA:

    def __init__(self):
        self.input_path = Path(
            "data/processed/real_estate_text_features.csv"
        )

        self.output_dir = Path("outputs/eda/rq3")
        self.df = None
        self.min_group_size = 5

    def load_data(self):

        self.df = pd.read_csv(self.input_path)

        self.df["price_billion"] = pd.to_numeric(
            self.df["price_billion"],
            errors="coerce"
        )

        self.df["price_per_m2_million"] = (
            pd.to_numeric(
                self.df["price_per_m2"],
                errors="coerce"
            ) / 1_000_000
        )

        self.df["district"] = (
            self.df["district"]
            .astype("string")
            .str.strip()
        )

        self.df["district"] = self.df["district"].replace(
            "", pd.NA
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        print("Đã tải dữ liệu thành công.")
        print("Tổng số bản ghi:", len(self.df))
        print(
            "Số bản ghi thiếu quận:",
            self.df["district"].isna().sum()
        )

    def analyze_district(self):

        print("\n========= RQ3: DISTRICT ANALYSIS =========")

        valid_df = self.df.dropna(
            subset=["district"]
        )

        # Thống kê tổng quan theo quận
        district_summary = (
            valid_df.groupby("district")
            .agg(
                listing_count=("name", "count"),
                median_price_billion=("price_billion", "median"),
                median_price_per_m2_million=(
                    "price_per_m2_million", "median"
                ),
                mean_price_per_m2_million=(
                    "price_per_m2_million", "mean"
                )
            )
            .reset_index()
        )

        district_summary = district_summary.sort_values(
            "median_price_per_m2_million",
            ascending=False
        )

        print("\n--- Thống kê theo quận ---")
        print(district_summary.to_string(index=False))

        district_summary.to_csv(
            self.output_dir / "rq3_district_summary.csv",
            index=False,
            encoding="utf-8-sig"
        )

        # Thống kê riêng theo loại bất động sản
        type_summary = (
            valid_df.groupby(["district", "property_type"])
            .agg(
                listing_count=("name", "count"),
                median_price_billion=("price_billion", "median"),
                median_price_per_m2_million=(
                    "price_per_m2_million", "median"
                )
            )
            .reset_index()
        )

        type_summary = type_summary.sort_values(
            ["property_type", "median_price_per_m2_million"],
            ascending=[True, False]
        )

        print("\n--- Thống kê theo quận và loại bất động sản ---")
        print(type_summary.to_string(index=False))

        type_summary.to_csv(
            self.output_dir / "rq3_district_by_type.csv",
            index=False,
            encoding="utf-8-sig"
        )

        return type_summary

    def plot_price_per_m2_by_type(self, summary):

        print("\n--- Tạo biểu đồ giá/m² theo quận ---")

        for property_type in summary["property_type"].unique():

            group = summary[
                (summary["property_type"] == property_type)
                & (summary["listing_count"] >= self.min_group_size)
            ].copy()

            if group.empty:
                print(
                    f"Bỏ qua {property_type}: "
                    "không có nhóm đủ số lượng tin đăng."
                )
                continue

            group = group.sort_values(
                "median_price_per_m2_million",
                ascending=True
            )

            plt.figure(figsize=(11, max(6, len(group) * 0.4)))

            bars = plt.barh(
                group["district"],
                group["median_price_per_m2_million"]
            )

            plt.title(
                f"Trung vị giá/m² theo quận - {property_type}"
            )
            plt.xlabel("Trung vị giá/m² (triệu đồng)")
            plt.ylabel("Quận")

            plt.grid(axis="x", alpha=0.3)

            for bar, value in zip(
                bars,
                group["median_price_per_m2_million"]
            ):
                plt.text(
                    bar.get_width(),
                    bar.get_y() + bar.get_height() / 2,
                    f" {value:.1f}",
                    va="center"
                )

            plt.tight_layout()

            filename = (
                "rq3_apartment_price_by_district.png"
                if property_type == "Căn hộ chung cư"
                else "rq3_house_price_by_district.png"
            )

            plt.savefig(
                self.output_dir / filename,
                dpi=300,
                bbox_inches="tight"
            )

            plt.close()

            print("Đã tạo:", filename)

    def plot_listing_count(self):

        counts = (
            self.df.dropna(subset=["district"])
            .groupby("district")
            .size()
            .sort_values(ascending=True)
        )

        plt.figure(
            figsize=(11, max(6, len(counts) * 0.4))
        )

        plt.barh(
            counts.index,
            counts.values
        )

        plt.title("Số lượng tin đăng theo quận")
        plt.xlabel("Số lượng tin đăng")
        plt.ylabel("Quận")
        plt.grid(axis="x", alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            self.output_dir / "rq3_listing_count_by_district.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("Đã tạo rq3_listing_count_by_district.png")

    def run(self):

        self.load_data()

        summary = self.analyze_district()

        self.plot_price_per_m2_by_type(summary)

        self.plot_listing_count()

        print("\n========= RQ3 COMPLETED =========")
        print("Thư mục kết quả:", self.output_dir)


if __name__ == "__main__":
    eda = LocationAnalysisEDA()
    eda.run()
