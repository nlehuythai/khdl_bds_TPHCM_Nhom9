from pathlib import Path
import sys
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.UI.utils.data_loader import load_data, get_data_path
from src.UI.views.overview import render as render_overview
from src.UI.views.price_analysis import render as render_price
from src.UI.views.location_analysis import render as render_location
from src.UI.views.property_analysis import render as render_property
from src.UI.views.regression_analysis import render as render_regression
st.set_page_config(
    page_title="Real Estate Analytics | TP.HCM",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: rgba(128,128,128,0.08);
        border: 1px solid rgba(128,128,128,0.18);
        padding: 14px 16px;
        border-radius: 12px;
    }
    h1, h2, h3 {letter-spacing: -0.02em;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🏙️ Real Estate")
    st.caption("Phân tích dữ liệu bất động sản TP.HCM")
    page = st.radio(
        "Điều hướng",
        [
            "Tổng quan",
            "Phân tích giá",
            "Phân tích khu vực",
            "Phân tích đặc điểm",
            "Mô hình hồi quy",
        ],
    )
    st.divider()
    st.caption("Dữ liệu nghiên cứu")
    st.caption("1.000 tin đăng · TP.HCM")
    st.caption("Nguồn: bộ dữ liệu đã xử lý")

try:
    df = load_data()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.info(
        "Đặt real_estate_text_features.csv tại "
        "data/processed/real_estate_text_features.csv rồi tải lại trang."
    )
    st.stop()
except Exception as exc:
    st.error(f"Không thể đọc dữ liệu: {exc}")
    st.stop()

st.caption(f"Đang sử dụng: `{get_data_path()}`")

if page == "Tổng quan":
    render_overview(df)
elif page == "Phân tích giá":
    render_price(df)
elif page == "Phân tích khu vực":
    render_location(df)
elif page == "Phân tích đặc điểm":
    render_property(df)
else:
    render_regression(df)
