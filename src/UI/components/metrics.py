import streamlit as st

def render_metrics(df):
    total = len(df)
    median_price = df["price_vnd"].median() / 1e9 if "price_vnd" in df else None
    median_area = df["area_m2"].median() if "area_m2" in df else None
    median_m2 = df["price_per_m2"].median() / 1e6 if "price_per_m2" in df else None

    cols = st.columns(4)
    cols[0].metric("Tổng tin đăng", f"{total:,}")
    cols[1].metric("Giá trung vị", f"{median_price:,.2f} tỷ" if median_price is not None else "N/A")
    cols[2].metric("Diện tích trung vị", f"{median_area:,.1f} m²" if median_area is not None else "N/A")
    cols[3].metric("Giá/m² trung vị", f"{median_m2:,.1f} triệu" if median_m2 is not None else "N/A")
