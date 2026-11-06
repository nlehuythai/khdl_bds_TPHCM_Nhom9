
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[3]
CANDIDATE_PATHS = [
    ROOT / "data" / "processed" / "real_estate_text_features.csv",
    ROOT / "data" / "real_estate_text_features.csv",
    ROOT / "real_estate_text_features.csv",
]

def get_data_path() -> Path:
    for path in CANDIDATE_PATHS:
        if path.exists():
            return path
    searched = "\n".join(f"- {p}" for p in CANDIDATE_PATHS)
    raise FileNotFoundError(
        "Không tìm thấy real_estate_text_features.csv. "
        "Các vị trí đã kiểm tra:\n" + searched
    )

@st.cache_data
def load_data() -> pd.DataFrame:
    path = get_data_path()
    df = pd.read_csv(path, low_memory=False)

    for col in ["price_vnd", "area_m2", "price_per_m2", "price_billion",
                "bedrooms", "bathrooms", "floors", "description_length",
                "description_word_count", "published_year", "published_month"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["property_type", "district", "ward", "province"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    if "published_at" in df.columns:
        df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")

    if "price_per_m2" not in df.columns and {"price_vnd", "area_m2"}.issubset(df.columns):
        df["price_per_m2"] = df["price_vnd"] / df["area_m2"]

    return df
