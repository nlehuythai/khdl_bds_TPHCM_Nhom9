
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


ROOT_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT_DIR / "data" / "processed" / "real_estate_text_features.csv"
OUTPUT_DIR = ROOT_DIR / "outputs" / "eda" / "rq6"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_data():
    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "price_vnd",
        "area_m2",
        "property_type",
        "district",
        "bedrooms",
        "bathrooms"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Thiếu các cột: {missing_columns}")

    numeric_columns = [
        "price_vnd",
        "area_m2",
        "bedrooms",
        "bathrooms"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["property_type"] = (
        df["property_type"]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    df["district"] = (
        df["district"]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    df = df[
        (df["price_vnd"] > 0) &
        (df["area_m2"] > 0) &
        df["property_type"].notna()
    ].copy()

    df["district_model"] = df["district"].fillna("Không rõ")

    district_counts = df.loc[
        df["district_model"] != "Không rõ",
        "district_model"
    ].value_counts()

    rare_districts = district_counts[
        district_counts < 10
    ].index

    df.loc[
        df["district_model"].isin(rare_districts),
        "district_model"
    ] = "Nhóm ít mẫu (<10)"

    df["log_price"] = np.log(df["price_vnd"])
    df["log_area"] = np.log(df["area_m2"])

    return df


def save_model_outputs(model, model_name, metrics):
    # Lưu kết quả thống kê mô hình
    summary_path = OUTPUT_DIR / f"{model_name}_summary.txt"

    with open(summary_path, "w", encoding="utf-8") as file:
        file.write(model.summary().as_text())

    # Lưu hệ số hồi quy
    coefficients = pd.DataFrame({
        "feature": model.params.index,
        "coefficient": model.params.values,
        "p_value": model.pvalues.values,
        "std_error_HC3": model.bse.values,
        "ci_lower": model.conf_int()[0].values,
        "ci_upper": model.conf_int()[1].values
    })

    coefficients["significant_5_percent"] = (
        coefficients["p_value"] < 0.05
    )

    coefficients.to_csv(
        OUTPUT_DIR / f"{model_name}_coefficients.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return metrics


def fit_full_model(df, model_name, formula):
    """
    Mô hình cơ bản trên toàn bộ dữ liệu hợp lệ.
    Kết quả dùng để phân tích bổ sung, không dùng so sánh
    trực tiếp với mô hình mở rộng 750 quan sát.
    """

    model = smf.ols(
        formula=formula,
        data=df
    ).fit(cov_type="HC3")

    metrics = {
        "model": model_name,
        "sample_size": int(model.nobs),
        "r_squared": model.rsquared,
        "adjusted_r_squared": model.rsquared_adj,
        "AIC": model.aic,
        "BIC": model.bic,
        "RMSE_in_sample_log": np.sqrt(
            np.mean(model.resid ** 2)
        )
    }

    save_model_outputs(model, model_name, metrics)

    plot_model_diagnostics(model, model_name)

    return model, metrics


def fit_and_evaluate(
    train_df,
    test_df,
    model_name,
    formula
):
    """
    Huấn luyện và đánh giá mô hình trên cùng quy trình.

    - R2, Adjusted R2, AIC, BIC: tính trên tập train.
    - RMSE train: sai số trên tập train.
    - RMSE test: sai số trên tập test.
    - Cả hai mô hình dùng cùng train/test.
    """

    model = smf.ols(
        formula=formula,
        data=train_df
    ).fit(cov_type="HC3")

    # Dự đoán trên tập train
    train_predictions = model.predict(train_df)

    # Dự đoán trên tập test
    test_predictions = model.predict(test_df)

    # RMSE trên log(price)
    rmse_train = np.sqrt(
        mean_squared_error(
            train_df["log_price"],
            train_predictions
        )
    )

    rmse_test = np.sqrt(
        mean_squared_error(
            test_df["log_price"],
            test_predictions
        )
    )

    metrics = {
        "model": model_name,
        "n_train": len(train_df),
        "n_test": len(test_df),
        "r_squared_train": model.rsquared,
        "adjusted_r_squared_train": model.rsquared_adj,
        "RMSE_train_log": rmse_train,
        "RMSE_test_log": rmse_test,
        "AIC_train": model.aic,
        "BIC_train": model.bic
    }

    save_model_outputs(model, model_name, metrics)

    # Lưu dự đoán trên tập test
    test_results = pd.DataFrame({
        "actual_log_price": test_df["log_price"],
        "predicted_log_price": test_predictions,
        "residual": test_df["log_price"] - test_predictions
    }, index=test_df.index)

    test_results.to_csv(
        OUTPUT_DIR / f"{model_name}_test_predictions.csv",
        index_label="original_index",
        encoding="utf-8-sig"
    )

    # Lưu phần dư trên tập train để kiểm tra mô hình
    train_diagnostics = pd.DataFrame({
        "actual_log_price": train_df["log_price"],
        "predicted_log_price": train_predictions,
        "residual": train_df["log_price"] - train_predictions
    }, index=train_df.index)

    train_diagnostics.to_csv(
        OUTPUT_DIR / f"{model_name}_diagnostics.csv",
        index_label="original_index",
        encoding="utf-8-sig"
    )

    plot_model_diagnostics(model, model_name)

    return model, metrics


def plot_model_diagnostics(model, model_name):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.scatterplot(
        x=model.fittedvalues,
        y=model.resid,
        alpha=0.5,
        ax=axes[0]
    )

    axes[0].axhline(0, linestyle="--")
    axes[0].set_title("Residuals vs Fitted")
    axes[0].set_xlabel("Predicted log(price)")
    axes[0].set_ylabel("Residuals")

    sns.histplot(
        model.resid,
        bins=30,
        kde=True,
        ax=axes[1]
    )

    axes[1].set_title("Residual Distribution")
    axes[1].set_xlabel("Residual")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"{model_name}_diagnostics.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def main():
    print("=" * 65)
    print("RQ6 - MULTIVARIATE ANALYSIS")
    print("=" * 65)

    df = load_data()

    print(f"\nTổng số bản ghi hợp lệ: {len(df)}")

    print("\nSố lượng theo loại bất động sản:")
    print(df["property_type"].value_counts())

    print("\nSố lượng giá trị thiếu:")
    print(
        df[["district", "bedrooms", "bathrooms"]]
        .isna()
        .sum()
    )

    # ==================================================
    # MODEL 1: BASIC - TOÀN BỘ DỮ LIỆU
    # ==================================================

    formula_1 = (
        "log_price ~ log_area "
        "+ C(property_type) "
        "+ C(district_model)"
    )

    model_1_basic, metrics_1_basic = fit_full_model(
        df,
        "model_1_basic",
        formula_1
    )

    # ==================================================
    # TẠO TẬP DỮ LIỆU CHUNG CHO SO SÁNH
    # ==================================================

    common_df = df.dropna(
        subset=[
            "bedrooms",
            "bathrooms"
        ]
    ).copy()

    print("\n" + "=" * 65)
    print("COMMON DATASET")
    print("=" * 65)

    print(f"Số quan sát dùng để so sánh: {len(common_df)}")

    if len(common_df) < 2:
        raise ValueError("Không đủ dữ liệu để chia train/test.")

    # ==================================================
    # CHIA TRAIN/TEST MỘT LẦN DUY NHẤT
    # ==================================================

    train_indices, test_indices = train_test_split(
        common_df.index,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    train_df = common_df.loc[train_indices].copy()
    test_df = common_df.loc[test_indices].copy()

    print(f"Số quan sát train: {len(train_df)}")
    print(f"Số quan sát test: {len(test_df)}")

    # ==================================================
    # MODEL 1: MATCHED - CÙNG TẬP DỮ LIỆU VỚI MODEL 2
    # ==================================================

    model_1_matched, metrics_1_matched = fit_and_evaluate(
        train_df,
        test_df,
        "model_1_matched",
        formula_1
    )

    # ==================================================
    # MODEL 2: EXTENDED
    # BỔ SUNG BEDROOMS VÀ BATHROOMS
    # ==================================================

    formula_2 = (
        "log_price ~ log_area "
        "+ C(property_type) "
        "+ C(district_model) "
        "+ bedrooms "
        "+ bathrooms"
    )

    model_2_extended, metrics_2_extended = fit_and_evaluate(
        train_df,
        test_df,
        "model_2_extended",
        formula_2
    )

    # ==================================================
    # SO SÁNH HAI MÔ HÌNH TRÊN CÙNG DỮ LIỆU
    # ==================================================

    comparison = pd.DataFrame([
        metrics_1_matched,
        metrics_2_extended
    ])

    comparison.to_csv(
        OUTPUT_DIR / "model_comparison_matched.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n" + "=" * 65)
    print("MODEL 1 - BASIC (TOÀN BỘ DỮ LIỆU)")
    print("=" * 65)
    print(model_1_basic.summary())

    print("\n" + "=" * 65)
    print("MODEL 1 - MATCHED (CÙNG TẬP DỮ LIỆU)")
    print("=" * 65)
    print(model_1_matched.summary())

    print("\n" + "=" * 65)
    print("MODEL 2 - EXTENDED")
    print("=" * 65)
    print(model_2_extended.summary())

    print("\n" + "=" * 65)
    print("MODEL COMPARISON - MATCHED DATA")
    print("=" * 65)
    print(comparison.to_string(index=False))

    print("\nĐã lưu kết quả tại:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
