
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class RealEstateAreaAnalysis:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parents[2]

        self.input_path = (
            self.root_dir
            / "data"
            / "processed"
            / "real_estate_text_features.csv"
        )

        self.output_dir = (
            self.root_dir
            / "outputs"
            / "eda"
            / "rq4"
        )

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.df = None

    def load_data(self):
        print("\n========== LOADING DATA ==========")

        if not self.input_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file: {self.input_path}"
            )

        self.df = pd.read_csv(self.input_path)

        required_columns = [
            "property_type",
            "area_m2",
            "price_vnd",
            "price_per_m2",
        ]

        missing_columns = [
            col for col in required_columns
            if col not in self.df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Thiếu các cột cần thiết: {missing_columns}"
            )

        numeric_columns = [
            "area_m2",
            "price_vnd",
            "price_per_m2",
        ]

        for col in numeric_columns:
            self.df[col] = pd.to_numeric(
                self.df[col],
                errors="coerce"
            )

        self.df["property_type"] = (
            self.df["property_type"]
            .astype("string")
            .str.strip()
        )

        self.df["price_billion"] = (
            self.df["price_vnd"] / 1_000_000_000
        )

        self.df["price_per_m2_million"] = (
            self.df["price_per_m2"] / 1_000_000
        )

        self.df = self.df.replace(
            [np.inf, -np.inf],
            np.nan
        )

        self.df = self.df.dropna(
            subset=[
                "property_type",
                "area_m2",
                "price_vnd",
                "price_per_m2",
            ]
        )

        self.df = self.df[
            (self.df["area_m2"] > 0)
            & (self.df["price_vnd"] > 0)
            & (self.df["price_per_m2"] > 0)
        ].copy()

        print(f"Tổng số bản ghi hợp lệ: {len(self.df)}")
        print("\nSố lượng theo loại bất động sản:")
        print(self.df["property_type"].value_counts())

    def descriptive_analysis(self):
        print("\n========== DESCRIPTIVE STATISTICS ==========")

        columns = [
            "area_m2",
            "price_billion",
            "price_per_m2_million",
        ]

        overall = self.df[columns].describe().T

        overall.to_csv(
            self.output_dir / "rq4_descriptive_statistics.csv",
            encoding="utf-8-sig"
        )

        print("\nThống kê toàn bộ dữ liệu:")
        print(overall.round(2))

        grouped = (
            self.df.groupby("property_type")[columns]
            .agg(["count", "mean", "median", "std", "min", "max"])
            .round(2)
        )

        print("\nThống kê theo loại bất động sản:")
        print(grouped)

        grouped.to_csv(
            self.output_dir / "rq4_statistics_by_type.csv",
            encoding="utf-8-sig"
        )

    def correlation_analysis(self):
        print("\n========== CORRELATION ANALYSIS ==========")

        variables = [
            "area_m2",
            "price_billion",
            "price_per_m2_million",
        ]

        records = []

        groups = {
            "Toàn bộ": self.df,
        }

        for property_type, group in self.df.groupby("property_type"):
            groups[property_type] = group

        for group_name, group in groups.items():
            for x in [
                "price_billion",
                "price_per_m2_million",
            ]:
                pair = group[["area_m2", x]].dropna()

                pearson = pair["area_m2"].corr(
                    pair[x],
                    method="pearson"
                )

                spearman = pair["area_m2"].corr(
                    pair[x],
                    method="spearman"
                )

                records.append({
                    "group": group_name,
                    "relationship": f"area_m2 vs {x}",
                    "sample_count": len(pair),
                    "pearson_correlation": pearson,
                    "spearman_correlation": spearman,
                })

        result = pd.DataFrame(records)

        result.to_csv(
            self.output_dir / "rq4_correlation_statistics.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print(result.round(4).to_string(index=False))

        return result

    def plot_scatter(self, x_column, y_column, filename, title, y_label):
        print(f"\nĐang tạo biểu đồ: {filename}")

        fig, ax = plt.subplots(figsize=(11, 7))

        groups = [
            ("Toàn bộ", self.df),
        ]

        for property_type, group in self.df.groupby("property_type"):
            groups.append((property_type, group))

        for group_name, group in groups:
            ax.scatter(
                group[x_column],
                group[y_column],
                alpha=0.35 if group_name == "Toàn bộ" else 0.65,
                s=28,
                label=f"{group_name} (n={len(group)})"
            )

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel("Diện tích (m²)", fontsize=11)
        ax.set_ylabel(y_label, fontsize=11)

        ax.grid(
            True,
            linestyle="--",
            alpha=0.3
        )

        ax.legend()
        plt.tight_layout()

        plt.savefig(
            self.output_dir / filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print(f"Đã tạo: {filename}")

    def plot_correlation_heatmap(self):
        print("\nĐang tạo correlation heatmap...")

        variables = [
            "area_m2",
            "price_billion",
            "price_per_m2_million",
        ]

        correlation = self.df[variables].corr(
            method="pearson"
        )

        fig, ax = plt.subplots(figsize=(8, 6))

        image = ax.imshow(
            correlation,
            cmap="coolwarm",
            vmin=-1,
            vmax=1
        )

        ax.set_xticks(range(len(variables)))
        ax.set_yticks(range(len(variables)))

        labels = [
            "Diện tích",
            "Tổng giá",
            "Giá/m²",
        ]

        ax.set_xticklabels(labels)
        ax.set_yticklabels(labels)

        for i in range(len(variables)):
            for j in range(len(variables)):
                ax.text(
                    j,
                    i,
                    f"{correlation.iloc[i, j]:.2f}",
                    ha="center",
                    va="center",
                    fontsize=12
                )

        ax.set_title(
            "Ma trận tương quan Pearson",
            fontsize=14,
            fontweight="bold"
        )

        fig.colorbar(image, ax=ax, label="Correlation")

        plt.tight_layout()

        plt.savefig(
            self.output_dir / "rq4_correlation_heatmap.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("Đã tạo rq4_correlation_heatmap.png")

    def outlier_sensitivity_analysis(self):
        print("\n========== OUTLIER SENSITIVITY ==========")

        if "is_outlier_price_per_m2" not in self.df.columns:
            print("Không tìm thấy cột đánh dấu outlier. Bỏ qua.")
            return

        records = []

        groups = {
            "Toàn bộ": self.df,
        }

        for property_type, group in self.df.groupby("property_type"):
            groups[property_type] = group

        for group_name, group in groups.items():
            for condition, subset in [
                ("Giữ tất cả", group),
                (
                    "Không gồm outlier",
                    group[
                        ~group["is_outlier_price_per_m2"]
                        .astype(str)
                        .str.lower()
                        .isin(["true", "1"])
                    ]
                ),
            ]:
                for target in [
                    "price_billion",
                    "price_per_m2_million",
                ]:
                    pair = subset[["area_m2", target]].dropna()

                    records.append({
                        "group": group_name,
                        "condition": condition,
                        "relationship": target,
                        "sample_count": len(pair),
                        "pearson": pair["area_m2"].corr(
                            pair[target],
                            method="pearson"
                        ),
                        "spearman": pair["area_m2"].corr(
                            pair[target],
                            method="spearman"
                        ),
                    })

        result = pd.DataFrame(records)

        result.to_csv(
            self.output_dir / "rq4_outlier_sensitivity.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print(result.round(4).to_string(index=False))

    def run(self):
        self.load_data()

        self.descriptive_analysis()

        self.correlation_analysis()

        self.plot_scatter(
            x_column="area_m2",
            y_column="price_billion",
            filename="rq4_area_price_scatter.png",
            title="Mối quan hệ giữa diện tích và tổng giá",
            y_label="Tổng giá (tỷ đồng)"
        )

        self.plot_scatter(
            x_column="area_m2",
            y_column="price_per_m2_million",
            filename="rq4_area_price_per_m2_scatter.png",
            title="Mối quan hệ giữa diện tích và giá/m²",
            y_label="Giá/m² (triệu đồng)"
        )

        self.plot_correlation_heatmap()

        self.outlier_sensitivity_analysis()

        print("\n========== RQ4 COMPLETED ==========")
        print(f"Thư mục kết quả: {self.output_dir}")


if __name__ == "__main__":
    analysis = RealEstateAreaAnalysis()
    analysis.run()
