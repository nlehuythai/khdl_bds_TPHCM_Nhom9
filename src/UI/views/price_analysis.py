import streamlit as st
import plotly.express as px
from src.UI.components.charts import price_histogram, box_by_type

def render(df):
    st.title("Phân tích giá bất động sản")
    required = ["price_billion", "price_per_m2", "property_type"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.warning(f"Thiếu cột cần thiết: {', '.join(missing)}")
        return

    st.subheader("RQ1 — Phân phối giá")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(price_histogram(df, "price_billion",
                         "Phân phối giá đăng bán", "Giá (tỷ đồng)"),
                         use_container_width=True)
    with c2:
        tmp = df.dropna(subset=["price_billion"])
        fig = px.box(tmp, y="price_billion", points="outliers",
                     title="Boxplot giá đăng bán")
        fig.update_layout(yaxis_title="Giá (tỷ đồng)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("RQ2 — So sánh nhà và căn hộ")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(box_by_type(df, "price_billion",
                         "Giá đăng bán theo loại", "Giá (tỷ đồng)"),
                         use_container_width=True)
    with c2:
        st.plotly_chart(box_by_type(df, "price_per_m2",
                         "Giá trên mỗi m² theo loại", "Giá (VND/m²)"),
                         use_container_width=True)

    summary = df.groupby("property_type", dropna=False).agg(
        so_tin=("price_vnd", "count"),
        gia_trung_vi=("price_vnd", "median"),
        gia_m2_trung_vi=("price_per_m2", "median"),
    ).reset_index()
    summary["gia_trung_vi_ty"] = summary["gia_trung_vi"] / 1e9
    summary["gia_m2_trung_vi_trieu"] = summary["gia_m2_trung_vi"] / 1e6
    st.dataframe(summary[["property_type", "so_tin", "gia_trung_vi_ty",
                          "gia_m2_trung_vi_trieu"]].rename(columns={
        "property_type": "Loại BĐS", "so_tin": "Số tin",
        "gia_trung_vi_ty": "Giá trung vị (tỷ)",
        "gia_m2_trung_vi_trieu": "Giá/m² trung vị (triệu)"
    }), use_container_width=True)
    st.caption("Giá/m² của nhà và căn hộ có thể khác nhau về định nghĩa diện tích trong dữ liệu nguồn.")
