
from datasets import load_dataset
import pandas as pd
import os
from datetime import datetime

# =====================================
# CONFIGURATION
# =====================================

DATASET_NAME = "vduydong/vietnam-real-estates-2"

TARGET_TOTAL = 1000
TARGET_HOUSE = 600
TARGET_APARTMENT = 400

ALLOWED_TYPES = {
    "Nhà",
    "Căn hộ chung cư"
}

ALLOWED_PROVINCES = {
    "Hồ Chí Minh",
    "Thành phố Hồ Chí Minh"
}

OUTPUT_FILE = "data/raw/huggingface_data.csv"

# =====================================
# LOAD DATA
# =====================================

def main():

    print("Dang ket noi dataset...")

    dataset = load_dataset(
        DATASET_NAME,
        split="train",
        streaming=True
    )

    dataset = dataset.shuffle(
        seed=42,
        buffer_size=100000
    )

    samples = []

    type_counts = {
        "Nhà": 0,
        "Căn hộ chung cư": 0
    }

    print("Bat dau loc du lieu...")

    # =====================================
    # FILTER AND EXTRACT
    # =====================================

    for row in dataset:

        province = str(
            row.get("province_name") or ""
        ).strip()

        property_type = str(
            row.get("property_type_name") or ""
        ).strip()

        if province not in ALLOWED_PROVINCES:
            continue

        if property_type not in ALLOWED_TYPES:
            continue

        # Check quota
        if property_type == "Nhà":
            if type_counts["Nhà"] >= TARGET_HOUSE:
                continue

        if property_type == "Căn hộ chung cư":
            if type_counts["Căn hộ chung cư"] >= TARGET_APARTMENT:
                continue

        # Validate price and area
        try:
            price = float(row.get("price"))
            area = float(row.get("area"))
        except (TypeError, ValueError):
            continue

        if pd.isna(price) or pd.isna(area):
            continue

        if price <= 0 or area <= 0:
            continue

        # Extract only required fields
        samples.append({
            "source": DATASET_NAME,
            "source_url": None,
            "name": row.get("name"),
            "property_type": property_type,
            "province": province,
            "district": row.get("district_name"),
            "ward": row.get("ward_name"),
            "price_vnd": price,
            "area_m2": area,
            "bedrooms": row.get("bedroom_count"),
            "bathrooms": row.get("bathroom_count"),
            "floors": row.get("floor_count"),
            "description": row.get("description"),
            "published_at": row.get("published_at"),
            "collected_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        })

        type_counts[property_type] += 1

        total = sum(type_counts.values())

        if total % 100 == 0:
            print(
                f"Da thu thap: {total}/{TARGET_TOTAL}"
            )

        if total >= TARGET_TOTAL:
            break

    # =====================================
    # SAVE DATA
    # =====================================

    if not samples:
        print("Khong tim thay du lieu phu hop.")
        return

    df = pd.DataFrame(samples)

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================
    # SUMMARY
    # =====================================

    print("\n========== COLLECTION REPORT ==========")

    print("Tong so mau:", len(df))

    print("\nPhan bo loai bat dong san:")
    print(df["property_type"].value_counts())

    print("\nPhan bo theo nguon:")
    print(df["source"].value_counts())

    print("\nDu lieu thieu:")
    print(df.isnull().sum())

    print("\nDa luu tai:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
