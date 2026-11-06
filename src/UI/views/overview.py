import streamlit as st
import plotly.express as px
from src.UI.components.metrics import render_metrics

def render(df):
    st.title("Tổng quan thị trường bất động sản")
    st.write("Tổng quan bộ dữ liệu tin đăng bất động sản tại TP.HCM.")
    render_metrics(df)

    c1, c2 = st.columns(2)
    with c1:
        if "property_type" in df:
            counts = df["property_type"].value_counts(dropna=False).rename_axis("Loại").reset_index(name="Số tin")
            fig = px.pie(counts, names="Loại", values="Số tin", hole=0.48,
                         title="Cơ cấu loại bất động sản")
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if "price_billion" in df:
            data = df.dropna(subset=["price_billion"])
            fig = px.histogram(data, x="price_billion", color="property_type" if "property_type" in data else None,
                               nbins=30, title="Phân phối giá đăng bán")
            fig.update_layout(xaxis_title="Giá đăng bán (tỷ đồng)", yaxis_title="Số tin")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Xem trước dữ liệu")
    st.dataframe(df.head(20), use_container_width=True)
    st.caption("Đây là dữ liệu tin đăng và giá chào bán, không phải dữ liệu giao dịch thành công.")
