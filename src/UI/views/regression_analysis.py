import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RQ6_DIR = ROOT / "outputs" / "eda" / "rq6"

def render(df):
    st.title("Phân tích mô hình hồi quy — RQ6")
    st.write("Trang này đọc các kết quả RQ6 đã xuất ra, không tự tạo số liệu mô hình.")
    comparison_path = RQ6_DIR / "model_comparison.csv"
    if not comparison_path.exists():
        st.warning(f"Chưa tìm thấy `{comparison_path}`.")
        st.info("Hãy đặt file model_comparison.csv vào outputs/eda/rq6/.")
        st.caption("Khi có file, trang này sẽ hiển thị bảng so sánh các mô hình.")
        return

    result = pd.read_csv(comparison_path)
    st.subheader("So sánh mô hình")
    st.dataframe(result, use_container_width=True)
    numeric_cols = [c for c in result.select_dtypes(include="number").columns
                    if c.lower() in ["r2", "r_squared", "adj_r2", "adjusted_r2", "rmse", "rmse_log"]]
    if numeric_cols:
        model_col = next((c for c in result.columns if c not in numeric_cols), None)
        if model_col:
            metric = st.selectbox("Chọn chỉ tiêu", numeric_cols)
            fig = px.bar(result, x=model_col, y=metric, title=f"So sánh {metric}")
            st.plotly_chart(fig, use_container_width=True)

    st.caption("Chỉ so sánh trực tiếp chất lượng mô hình khi chúng được đánh giá trên cùng tập quan sát và cùng biến mục tiêu.")
