import streamlit as st
import plotly.express as px
from src.UI.components.charts import scatter_area_price

def render(df):
    st.title("Phân tích đặc điểm bất động sản")
    st.subheader("RQ4 — Diện tích và giá")
    if {"area_m2", "price_billion"}.issubset(df.columns):
        st.plotly_chart(scatter_area_price(df, "price_billion",
                         "Diện tích và giá đăng bán", "Giá (tỷ đồng)"),
                         use_container_width=True)
    if {"area_m2", "price_per_m2"}.issubset(df.columns):
        st.plotly_chart(scatter_area_price(df, "price_per_m2",
                         "Diện tích và giá trên mỗi m²", "Giá (VND/m²)"),
                         use_container_width=True)

    st.subheader("RQ5 — Đặc điểm cấu trúc và giá")
    available = [c for c in ["bedrooms", "bathrooms", "floors"] if c in df.columns]
    if not available:
        st.info("Không có trường phòng ngủ, phòng tắm hoặc số tầng.")
        return
    selected = st.selectbox("Chọn đặc điểm", available)
    metric = st.selectbox("Chỉ tiêu giá", ["price_billion", "price_per_m2"],
                          format_func=lambda x: "Giá đăng bán (tỷ)" if x == "price_billion" else "Giá/m² (VND)")
    data = df.dropna(subset=[selected, metric]).copy()
    summary = data.groupby(selected)[metric].median().reset_index()
    summary["Số tin"] = data.groupby(selected)[metric].count().values
    fig = px.bar(summary, x=selected, y=metric, hover_data=["Số tin"],
                 title=f"Giá trung vị theo {selected}")
    fig.update_layout(xaxis_title=selected, yaxis_title=metric, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Đây là mối liên hệ mô tả; chưa chứng minh đặc điểm này gây ra thay đổi giá.")
