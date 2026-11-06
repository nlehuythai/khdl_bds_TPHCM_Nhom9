import streamlit as st
import plotly.express as px

def render(df):
    st.title("Phân tích theo khu vực")
    if "district" not in df or "price_per_m2" not in df:
        st.warning("Dữ liệu cần có district và price_per_m2.")
        return

    data = df.dropna(subset=["district", "price_per_m2"]).copy()
    min_n = st.slider("Số tin tối thiểu để hiển thị mỗi khu vực", 1, 30, 5)
    summary = data.groupby("district").agg(
        so_tin=("price_per_m2", "size"),
        gia_m2_trung_vi=("price_per_m2", "median"),
        gia_trung_vi=("price_vnd", "median"),
    ).reset_index()
    summary = summary[summary["so_tin"] >= min_n].sort_values("gia_m2_trung_vi", ascending=False)
    if summary.empty:
        st.info("Không có khu vực đáp ứng điều kiện lọc.")
        return

    st.subheader("RQ3 — Giá/m² trung vị theo khu vực")
    fig = px.bar(summary, x="district", y="gia_m2_trung_vi",
                 hover_data=["so_tin"], title="Giá/m² trung vị theo quận/huyện")
    fig.update_layout(xaxis_title="Khu vực", yaxis_title="Giá trung vị (VND/m²)",
                      xaxis_tickangle=-45, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Bảng xếp hạng khu vực")
    summary["gia_m2_trieu"] = summary["gia_m2_trung_vi"] / 1e6
    summary["gia_ty"] = summary["gia_trung_vi"] / 1e9
    st.dataframe(summary[["district", "so_tin", "gia_ty", "gia_m2_trieu"]].rename(columns={
        "district": "Khu vực", "so_tin": "Số tin",
        "gia_ty": "Giá trung vị (tỷ)", "gia_m2_trieu": "Giá/m² trung vị (triệu)"
    }), use_container_width=True)
    st.caption("Các khu vực có ít tin đăng có thể cho kết quả thiếu ổn định; hãy xem đồng thời số lượng quan sát.")
