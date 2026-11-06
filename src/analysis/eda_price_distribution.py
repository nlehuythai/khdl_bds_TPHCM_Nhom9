
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


class PriceDistributionEDA:

    def __init__(self):
        self.input_path = Path(
            "data/processed/real_estate_text_features.csv"
        )

        self.output_dir = Path("outputs/eda/rq1")

        self.df = None

    def load_data(self):
        if not self.input_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file: {self.input_path}"
            )

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
        print("\n========= RQ1: DESCRIPTIVE STATISTICS =========")

        metrics = {
            "price_billion": "Tổng giá (tỷ đồng)",
            "price_per_m2_million": "Giá/m² (triệu đồng)"
        }

        results = []

        for column, label in metrics.items():

            series = self.df[column].dropna()

            print(f"\n--- {label} ---")
            print("Số lượng:", series.count())
            print("Trung bình:", round(series.mean(), 2))
            print("Trung vị:", round(series.median(), 2))
            print("Độ lệch chuẩn:", round(series.std(), 2))
            print("Nhỏ nhất:", round(series.min(), 2))
            print("Q1:", round(series.quantile(0.25), 2))
            print("Q3:", round(series.quantile(0.75), 2))
            print("P90:", round(series.quantile(0.90), 2))
            print("P95:", round(series.quantile(0.95), 2))
            print("Lớn nhất:", round(series.max(), 2))

            results.append({
                "metric": column,
                "count": series.count(),
                "mean": series.mean(),
                "median": series.median(),
                "std": series.std(),
                "min": series.min(),
                "q1": series.quantile(0.25),
                "q3": series.quantile(0.75),
                "p90": series.quantile(0.90),
                "p95": series.quantile(0.95),
                "max": series.max()
            })

        stats_df = pd.DataFrame(results)

        stats_df.to_csv(
            self.output_dir / "rq1_statistics.csv",
            index=False,
            encoding="utf-8-sig"
        )

    def plot_histogram(self, column, title, xlabel, filename):
        data = self.df[column].dropna()

        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=30, edgecolor="black")

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("Số lượng tin đăng")
        plt.grid(axis="y", alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            self.output_dir / filename,
            dpi=300
        )

        plt.close()

    def plot_boxplot(self, column, title, xlabel, filename):
        data = self.df[column].dropna()

        plt.figure(figsize=(10, 4))
        plt.boxplot(
            data,
            orientation="horizontal",
            showmeans=True
        )

        plt.title(title)
        plt.xlabel(xlabel)
        plt.grid(axis="x", alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            self.output_dir / filename,
            dpi=300
        )

        plt.close()

    def plot_log_histogram(self):
        data = self.df["price_billion"].dropna()

        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=30, edgecolor="black")

        plt.xscale("log")
        plt.title("Phân phối tổng giá bất động sản (trục log)")
        plt.xlabel("Tổng giá (tỷ đồng) - Log scale")
        plt.ylabel("Số lượng tin đăng")
        plt.grid(axis="y", alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            self.output_dir / "rq1_price_log_histogram.png",
            dpi=300
        )

        plt.close()

    def generate_charts(self):

        self.plot_histogram(
            "price_billion",
            "Phân phối tổng giá bất động sản",
            "Tổng giá (tỷ đồng)",
            "rq1_price_histogram.png"
        )

        self.plot_boxplot(
            "price_billion",
            "Boxplot tổng giá bất động sản",
            "Tổng giá (tỷ đồng)",
            "rq1_price_boxplot.png"
        )

        self.plot_histogram(
            "price_per_m2_million",
            "Phân phối giá bất động sản trên mỗi m²",
            "Giá/m² (triệu đồng)",
            "rq1_price_per_m2_histogram.png"
        )

        self.plot_boxplot(
            "price_per_m2_million",
            "Boxplot giá bất động sản trên mỗi m²",
            "Giá/m² (triệu đồng)",
            "rq1_price_per_m2_boxplot.png"
        )

        self.plot_log_histogram()

        print("\nĐã tạo thành công 5 biểu đồ.")

    def run(self):
        self.load_data()
        self.descriptive_statistics()
        self.generate_charts()

        print("\n========= RQ1 COMPLETED =========")
        print("Thư mục kết quả:", self.output_dir)


if __name__ == "__main__":
    eda = PriceDistributionEDA()
    eda.run()
