

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


class PropertyComparisonEDA:

    def __init__(self):
        self.input_path = Path(
            "data/processed/real_estate_text_features.csv"
        )

        self.output_dir = Path("outputs/eda/rq2")
        self.df = None

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

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        print("Đã tải dữ liệu thành công.")
        print("Số bản ghi:", len(self.df))

    def descriptive_statistics(self):

        print("\n========= RQ2: PROPERTY COMPARISON =========")

        columns = [
            "price_billion",
            "price_per_m2_million"
        ]

        results = []

        for property_type, group in self.df.groupby("property_type"):

            print(f"\n--- {property_type} ---")

            for column in columns:

                series = group[column].dropna()

                stats = {
                    "property_type": property_type,
                    "metric": column,
                    "count": series.count(),
                    "mean": series.mean(),
                    "median": series.median(),
                    "std": series.std(),
                    "q1": series.quantile(0.25),
                    "q3": series.quantile(0.75),
                    "min": series.min(),
                    "max": series.max()
                }

                results.append(stats)

                print(f"\n{column}")
                print("Số lượng:", stats["count"])
                print("Trung bình:", round(stats["mean"], 2))
                print("Trung vị:", round(stats["median"], 2))
                print("Độ lệch chuẩn:", round(stats["std"], 2))
                print("Q1:", round(stats["q1"], 2))
                print("Q3:", round(stats["q3"], 2))

        result_df = pd.DataFrame(results)

        result_df.to_csv(
            self.output_dir / "rq2_statistics.csv",
            index=False,
            encoding="utf-8-sig"
        )

    def plot_boxplot(self, column, title, ylabel, filename):

        types = self.df["property_type"].dropna().unique()

        data = [
            self.df.loc[
                self.df["property_type"] == property_type,
                column
            ].dropna()
            for property_type in types
        ]

        plt.figure(figsize=(10, 6))

        plt.boxplot(
            data,
            tick_labels=types,
            showmeans=True
        )

        plt.yscale("log")
        plt.title(title)
        plt.xlabel("Loại bất động sản")
        plt.ylabel(ylabel + " (thang logarit)")
        plt.grid(axis="y", alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            self.output_dir / filename,
            dpi=300
        )

        plt.close()

    def plot_median_comparison(
        self,
        column,
        title,
        ylabel,
        filename
    ):

        medians = (
            self.df.groupby("property_type")[column]
            .median()
        )

        plt.figure(figsize=(9, 6))

        bars = plt.bar(
            medians.index,
            medians.values
        )

        plt.title(title)
        plt.xlabel("Loại bất động sản")
        plt.ylabel(ylabel)
        plt.grid(axis="y", alpha=0.3)

        for bar, value in zip(bars, medians.values):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:,.2f}",
                ha="center",
                va="bottom"
            )

        plt.tight_layout()

        plt.savefig(
            self.output_dir / filename,
            dpi=300
        )

        plt.close()

    def generate_charts(self):

        self.plot_boxplot(
            "price_billion",
            "So sánh tổng giá theo loại bất động sản",
            "Tổng giá (tỷ đồng)",
            "rq2_total_price_boxplot.png"
        )

        self.plot_boxplot(
            "price_per_m2_million",
            "So sánh giá/m² theo loại bất động sản",
            "Giá/m² (triệu đồng)",
            "rq2_price_per_m2_boxplot.png"
        )

        self.plot_median_comparison(
            "price_billion",
            "Trung vị tổng giá theo loại bất động sản",
            "Tổng giá (tỷ đồng)",
            "rq2_total_price_median.png"
        )

        self.plot_median_comparison(
            "price_per_m2_million",
            "Trung vị giá/m² theo loại bất động sản",
            "Giá/m² (triệu đồng)",
            "rq2_price_per_m2_median.png"
        )

        print("\nĐã tạo thành công 4 biểu đồ.")

    def run(self):

        self.load_data()
        self.descriptive_statistics()
        self.generate_charts()

        print("\n========= RQ2 COMPLETED =========")
        print("Thư mục kết quả:", self.output_dir)


if __name__ == "__main__":
    eda = PropertyComparisonEDA()
    eda.run()
