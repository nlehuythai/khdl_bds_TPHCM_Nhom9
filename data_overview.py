
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. XÁC ĐỊNH ĐƯỜNG DẪN
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "real_estate_text_features.csv"
)

# ==========================================
# 2. ĐỌC DỮ LIỆU
# ==========================================

df = pd.read_csv(CSV_PATH)

N = len(df)

print(f"Tổng số bản ghi: N = {N}")

# ==========================================
# 3. TÍNH TỶ LỆ THIẾU DỮ LIỆU
# ==========================================

missing_count = df.isnull().sum()

missing_percent = (missing_count / N) * 100

missing_data = pd.DataFrame({
    "Số lượng thiếu": missing_count,
    "Tỷ lệ thiếu (%)": missing_percent
})

# Chỉ giữ những trường có dữ liệu thiếu
missing_data = missing_data[
    missing_data["Số lượng thiếu"] > 0
]

# Sắp xếp giảm dần theo tỷ lệ thiếu
missing_data = missing_data.sort_values(
    by="Tỷ lệ thiếu (%)",
    ascending=True
)

print("\nThống kê dữ liệu thiếu:")
print(missing_data.sort_values(
    by="Tỷ lệ thiếu (%)",
    ascending=False
).round(2))

# ==========================================
# 4. VẼ BIỂU ĐỒ THANH NGANG
# ==========================================

plt.figure(figsize=(11, 7))

bars = plt.barh(
    missing_data.index,
    missing_data["Tỷ lệ thiếu (%)"]
)

# Ghi tỷ lệ phần trăm ở cuối mỗi thanh
for bar, value in zip(bars, missing_data["Tỷ lệ thiếu (%)"]):
    plt.text(
        bar.get_width() + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.1f}%",
        va="center",
        fontsize=9
    )

plt.title(
    f"Tỷ lệ thiếu dữ liệu theo từng trường (N = {N:,})",
    fontsize=14,
    fontweight="bold",
    pad=15
)

plt.xlabel("Tỷ lệ thiếu dữ liệu (%)", fontsize=11)
plt.ylabel("Tên trường dữ liệu", fontsize=11)

plt.xlim(
    0,
    max(missing_data["Tỷ lệ thiếu (%)"].max() + 10, 10)
)

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

# ==========================================
# 5. LƯU BIỂU ĐỒ VÀO NOTEBOOKS
# ==========================================

NOTEBOOK_DIR = BASE_DIR / "notebooks"
NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)

output_path = NOTEBOOK_DIR / "missing_values_distribution.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(f"\nĐã lưu biểu đồ tại: {output_path}")
