
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


ROOT_DIR = Path(__file__).resolve().parents[3]
RQ6_DIR = ROOT_DIR / "outputs" / "eda" / "rq6"

COMPARISON_FILE = RQ6_DIR / "model_comparison.csv"


def render_rq6_comparison():

    st.title("Phân tích hồi quy đa biến")
    st.markdown(
        "So sánh mô hình hồi quy cơ bản và mô hình hồi quy mở rộng "
        "trên cùng tập dữ liệu."
    )

    # Kiểm tra file kết quả
    if not COMPARISON_FILE.exists():
        st.error(
            f"Không tìm thấy file kết quả: {COMPARISON_FILE}"
        )
        st.info(
            "Hãy chạy lại eda_multivariate_analysis.py "
            "để tạo dữ liệu so sánh mô hình."
        )
        return

    df = pd.read_csv(COMPARISON_FILE)

    required_columns = [
        "model",
        "n_train",
        "n_test",
        "r_squared_train",
        "adjusted_r_squared_train",
        "RMSE_train_log",
        "RMSE_test_log",
        "AIC_train",
        "BIC_train"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        st.error(
            f"File model_comparison.csv thiếu các cột: {missing}"
        )
        st.info(
            "File CSV có thể đang là kết quả từ phiên bản code cũ. "
            "Hãy chạy lại file phân tích RQ6 đã cập nhật."
        )
        return

    if len(df) != 2:
        st.warning(
            "Bảng so sánh cần có đúng hai dòng: "
            "Model 1 - Matched và Model 2 - Extended."
        )
        return

    # Tên hiển thị
    display_names = {
        "model_1_matched": "Model 1 - Basic",
        "model_2_extended": "Model 2 - Extended"
    }

    df["model_display"] = (
        df["model"].map(display_names).fillna(df["model"])
    )

    # ==================================================
    # 1. TỔNG QUAN DỮ LIỆU
    # ==================================================

    st.subheader("1. Quy mô dữ liệu đánh giá")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Số mô hình",
        len(df)
    )

    col2.metric(
        "Số quan sát Train",
        int(df["n_train"].iloc[0])
    )

    col3.metric(
        "Số quan sát Test",
        int(df["n_test"].iloc[0])
    )

    st.caption(
        "Cả hai mô hình được đánh giá trên cùng tập Train/Test."
    )

    st.divider()

    # ==================================================
    # 2. BẢNG SO SÁNH
    # ==================================================

    st.subheader("2. Bảng so sánh hiệu quả mô hình")

    table = df[
        [
            "model_display",
            "n_train",
            "n_test",
            "r_squared_train",
            "adjusted_r_squared_train",
            "RMSE_train_log",
            "RMSE_test_log",
            "AIC_train",
            "BIC_train"
        ]
    ].copy()

    table.columns = [
        "Mô hình",
        "Train",
        "Test",
        "R²",
        "Adjusted R²",
        "RMSE Train",
        "RMSE Test",
        "AIC",
        "BIC"
    ]

    st.dataframe(
        table.style.format({
            "R²": "{:.4f}",
            "Adjusted R²": "{:.4f}",
            "RMSE Train": "{:.4f}",
            "RMSE Test": "{:.4f}",
            "AIC": "{:.2f}",
            "BIC": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================================
    # 3. BIỂU ĐỒ R-SQUARED
    # ==================================================

    st.subheader("3. So sánh khả năng giải thích")

    r2_data = df.melt(
        id_vars="model_display",
        value_vars=[
            "r_squared_train",
            "adjusted_r_squared_train"
        ],
        var_name="metric",
        value_name="value"
    )

    r2_data["metric"] = r2_data["metric"].map({
        "r_squared_train": "R²",
        "adjusted_r_squared_train": "Adjusted R²"
    })

    fig_r2 = px.bar(
        r2_data,
        x="model_display",
        y="value",
        color="metric",
        barmode="group",
        text_auto=".3f",
        title="R² và Adjusted R² giữa hai mô hình",
        labels={
            "model_display": "Mô hình",
            "value": "Giá trị",
            "metric": "Chỉ số"
        }
    )

    fig_r2.update_layout(
        yaxis=dict(range=[0, 1]),
        legend_title="Chỉ số",
        height=430
    )

    st.plotly_chart(
        fig_r2,
        use_container_width=True
    )

    st.caption(
        "R² và Adjusted R² càng cao cho thấy mô hình giải thích "
        "được nhiều biến thiên của giá hơn trên tập huấn luyện."
    )

    st.divider()

    # ==================================================
    # 4. BIỂU ĐỒ RMSE
    # ==================================================

    st.subheader("4. So sánh sai số dự đoán")

    rmse_data = df.melt(
        id_vars="model_display",
        value_vars=[
            "RMSE_train_log",
            "RMSE_test_log"
        ],
        var_name="dataset",
        value_name="rmse"
    )

    rmse_data["dataset"] = rmse_data["dataset"].map({
        "RMSE_train_log": "Train",
        "RMSE_test_log": "Test"
    })

    fig_rmse = px.bar(
        rmse_data,
        x="model_display",
        y="rmse",
        color="dataset",
        barmode="group",
        text_auto=".4f",
        title="RMSE trên tập Train và Test",
        labels={
            "model_display": "Mô hình",
            "rmse": "RMSE (log price)",
            "dataset": "Tập dữ liệu"
        }
    )

    fig_rmse.update_layout(height=430)

    st.plotly_chart(
        fig_rmse,
        use_container_width=True
    )

    st.caption(
        "RMSE càng thấp thì sai số dự đoán càng nhỏ. "
        "Ưu tiên đối chiếu RMSE trên tập Test."
    )

    st.divider()

    # ==================================================
    # 5. BIỂU ĐỒ AIC VÀ BIC
    # ==================================================

    st.subheader("5. So sánh tiêu chí thông tin")

    information_data = df.melt(
        id_vars="model_display",
        value_vars=["AIC_train", "BIC_train"],
        var_name="criterion",
        value_name="value"
    )

    information_data["criterion"] = (
        information_data["criterion"].map({
            "AIC_train": "AIC",
            "BIC_train": "BIC"
        })
    )

    fig_information = px.bar(
        information_data,
        x="model_display",
        y="value",
        color="criterion",
        barmode="group",
        text_auto=".2f",
        title="So sánh AIC và BIC",
        labels={
            "model_display": "Mô hình",
            "value": "Giá trị",
            "criterion": "Tiêu chí"
        }
    )

    fig_information.update_layout(height=430)

    st.plotly_chart(
        fig_information,
        use_container_width=True
    )

    st.caption(
        "AIC và BIC thấp hơn thường cho thấy sự cân bằng tốt hơn "
        "giữa độ phù hợp và độ phức tạp của mô hình. "
        "Chỉ so sánh khi dùng cùng tập huấn luyện và biến phụ thuộc."
    )

    st.divider()

    # ==================================================
    # 6. BIỂU ĐỒ CHẨN ĐOÁN
    # ==================================================

    st.subheader("6. Chẩn đoán mô hình")

    diagnostic_files = {
        "Model 1 - Basic": (
            RQ6_DIR / "model_1_matched_diagnostics.png"
        ),
        "Model 2 - Extended": (
            RQ6_DIR / "model_2_extended_diagnostics.png"
        )
    }

    col1, col2 = st.columns(2)

    for col, (name, image_path) in zip(
        [col1, col2],
        diagnostic_files.items()
    ):
        with col:
            st.markdown(f"**{name}**")

            if image_path.exists():
                st.image(
                    str(image_path),
                    use_container_width=True
                )
            else:
                st.warning(
                    f"Chưa tìm thấy hình: {image_path.name}"
                )

    st.divider()

    # ==================================================
    # 7. KẾT LUẬN TỰ ĐỘNG THEO RMSE TEST
    # ==================================================

    st.subheader("7. Nhận xét kết quả")

    best_model = df.loc[
        df["RMSE_test_log"].idxmin()
    ]

    st.info(
        f"Mô hình có RMSE trên tập kiểm tra thấp hơn là "
        f"**{display_names.get(best_model['model'], best_model['model'])}** "
        f"với RMSE = {best_model['RMSE_test_log']:.4f}."
    )

    st.caption(
        "Kết luận này chỉ phản ánh kết quả trên lần chia Train/Test "
        "hiện tại, không khẳng định mô hình luôn tốt hơn trên mọi dữ liệu."
    )
