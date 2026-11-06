import pandas as pd

DATA_PATH = "data/raw/huggingface_data.csv"


def inspect_selected_records():
    df = pd.read_csv(DATA_PATH)

    # Trường hợp 1: Căn hộ chung cư có 16 tầng
    print("\n========== APARTMENT WITH 16 FLOORS ==========")

    apartment = df[
        (df["property_type"] == "Căn hộ chung cư")
        & (df["floors"] >= 10)
    ]

    print(
        apartment[
            [
                "name",
                "property_type",
                "district",
                "ward",
                "area_m2",
                "bedrooms",
                "bathrooms",
                "floors",
                "description"
            ]
        ].to_string(index=False)
    )

    # Trường hợp 2: Kiểm tra ngày đăng
    print("\n========== PUBLISHED DATE ==========")

    invalid_date = df[
        df["published_at"].astype(str).str.contains(
            "2026-03-24T07:01:24",
            na=False
        )
    ]

    print(
        invalid_date[
            ["name", "published_at", "description"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    inspect_selected_records()