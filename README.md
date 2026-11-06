
# 🏠 PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU BẤT ĐỘNG SẢN TP. HỒ CHÍ MINH

## 1. Giới thiệu

Đây là dự án thuộc học phần **Khoa học dữ liệu**, với mục tiêu xây dựng bộ dữ liệu bất động sản, thực hiện xử lý dữ liệu, phân tích thống kê, tìm hiểu các yếu tố liên quan đến giá bất động sản và trực quan hóa kết quả thông qua Dashboard.

Phạm vi nghiên cứu tập trung vào thị trường bất động sản tại TP. Hồ Chí Minh, gồm hai loại hình:

- Nhà.
- Căn hộ chung cư.

Dự án sử dụng Python để xử lý và phân tích dữ liệu, kết hợp Streamlit và Plotly để xây dựng giao diện trực quan hóa kết quả.

### Mục tiêu chính

- Thu thập và tổ chức dữ liệu bất động sản.
- Làm sạch, chuẩn hóa và kiểm tra chất lượng dữ liệu.
- Xây dựng các đặc trưng phục vụ phân tích.
- Phân tích phân bố giá, giá/m² và diện tích.
- So sánh giá giữa nhà và căn hộ chung cư.
- Phân tích sự khác biệt về giá giữa các khu vực.
- Tìm hiểu mối liên hệ giữa giá và các đặc điểm bất động sản.
- Xây dựng mô hình hồi quy đa biến.
- Phát triển Dashboard giúp theo dõi kết quả nghiên cứu.

---

## 2. Công nghệ sử dụng

| Công nghệ | Mục đích |
|---|---|
| Python | Ngôn ngữ lập trình chính |
| Pandas | Đọc, xử lý và phân tích dữ liệu |
| NumPy | Tính toán số học |
| Matplotlib | Trực quan hóa dữ liệu |
| Seaborn | Xây dựng biểu đồ thống kê |
| Statsmodels | Phân tích thống kê và hồi quy OLS |
| Plotly | Biểu đồ tương tác trên Dashboard |
| Streamlit | Xây dựng giao diện Dashboard |
| Jupyter Notebook | Khám phá và thử nghiệm dữ liệu |

---

## 3. Nguồn dữ liệu

Dữ liệu được sử dụng trong dự án lấy từ:

**Vietnam Real Estate Dataset**

- Nguồn: Hugging Face.
- Dataset: `vduydong/vietnam-real-estates-2`.
- Phạm vi nghiên cứu: TP. Hồ Chí Minh.
- Số lượng dữ liệu sử dụng: 1.000 tin đăng.
- Số trường dữ liệu ban đầu: 15.
- Số trường trong bảng đặc trưng sau xử lý: 25.
- Loại hình bất động sản: Nhà và Căn hộ chung cư.

**Lưu ý:** Dữ liệu phản ánh thông tin giá đăng tin, không phải giá giao dịch đã được xác nhận. Các kết quả phân tích được hiểu trong phạm vi bộ dữ liệu nghiên cứu.

---

## 4. Cấu trúc thư mục

```text
Source_Code/
│
├── data/
│   ├── raw/                         # Dữ liệu ban đầu
│   └── processed/                   # Dữ liệu sau xử lý
│       └── real_estate_text_features.csv
│
├── docs/                            # Tài liệu dự án
│
├── notebooks/                       # Notebook khám phá dữ liệu
│
├── outputs/
│   └── eda/
│       ├── rq1/                     # Kết quả phân tích RQ1
│       ├── rq2/                     # Kết quả phân tích RQ2
│       ├── rq3/                     # Kết quả phân tích RQ3
│       ├── rq4/                     # Kết quả phân tích RQ4
│       ├── rq5/                     # Kết quả phân tích RQ5
│       └── rq6/                     # Kết quả phân tích RQ6
│
├── reports/                         # Báo cáo kết quả
│
├── src/
│   ├── Data/                        # Các chức năng liên quan đến dữ liệu
│   ├── features/                    # Xây dựng đặc trưng
│   ├── analysis/                    # Các chương trình phân tích
│   │
│   └── UI/
│       ├── app.py                   # File khởi chạy Dashboard
│       ├── components/              # Thành phần giao diện dùng chung
│       └── views/                   # Các trang phân tích
│           ├── overview.py
│           ├── price_analysis.py
│           ├── location_analysis.py
│           ├── property_analysis.py
│           └── regression_analysis.py
│
├── main.py
├── requirements.txt
└── README.md
```

*Lưu ý: Cấu trúc trên mô tả các thư mục và thành phần chính. Một số file có thể được bổ sung tùy theo quá trình phát triển dự án.*

---

## 5. Cài đặt môi trường

### Bước 1. Clone hoặc tải dự án

Nếu dự án đã có trên máy tính, mở thư mục dự án bằng VS Code:

```bash
cd D:\KHDL\Source_Code
```

### Bước 2. Tạo môi trường ảo

```bash
python -m venv .venv
```

### Bước 3. Kích hoạt môi trường ảo

Đối với Windows:

```bash
.venv\Scripts\activate
```

Sau khi kích hoạt thành công, terminal sẽ hiển thị tiền tố `(.venv)`.

### Bước 4. Cài đặt thư viện

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Các thư viện chính được sử dụng:

```bash
pip install pandas numpy matplotlib seaborn statsmodels plotly streamlit
```

---

## 6. Dữ liệu đầu vào

Dashboard sử dụng bảng dữ liệu đã được xử lý tại:

```text
data/processed/real_estate_text_features.csv
```

Bảng dữ liệu này chứa 1.000 bản ghi và 25 trường đặc trưng, được sử dụng làm đầu vào cho các trang phân tích.

Trước khi chạy Dashboard, cần đảm bảo file dữ liệu tồn tại đúng vị trí.

---

## 7. Nội dung phân tích

Dự án triển khai sáu câu hỏi nghiên cứu chính:

| Câu hỏi | Nội dung |
|---|---|
| RQ1 | Phân tích phân bố giá đăng tin, giá/m² và diện tích |
| RQ2 | So sánh giá giữa nhà và căn hộ chung cư |
| RQ3 | Phân tích sự khác biệt về giá giữa các khu vực |
| RQ4 | Phân tích mối liên hệ giữa diện tích và giá bất động sản |
| RQ5 | Phân tích mối liên hệ giữa số phòng ngủ, phòng tắm, số tầng và giá |
| RQ6 | Xây dựng và đánh giá mô hình hồi quy đa biến |

### Các phương pháp được sử dụng

- Thống kê mô tả: Mean, Median, Quartile, Percentile.
- Phân tích phân bố: Histogram, Boxplot.
- So sánh nhóm: Groupby và thống kê theo loại hình.
- Phân tích tương quan: Pearson và Spearman.
- Hồi quy đa biến: Ordinary Least Squares (OLS).
- Đánh giá mô hình: R², Adjusted R², RMSE, AIC và BIC.

---

## 8. Khởi chạy Dashboard

Đảm bảo đã kích hoạt môi trường ảo và đang đứng tại thư mục gốc dự án.

Chạy lệnh:

```bash
python -m streamlit run src/UI/app.py
```

Sau khi khởi chạy thành công, Streamlit sẽ cung cấp địa chỉ truy cập trên trình duyệt, thường là:

```text
http://localhost:8501
```

### Các chức năng trên Dashboard

**1. Tổng quan**
- Hiển thị số lượng bản ghi.
- Thống kê các chỉ số cơ bản.
- Phân bố dữ liệu theo loại hình bất động sản.

**2. Phân tích giá**
- Phân tích phân bố giá đăng tin.
- Phân tích giá trên mỗi mét vuông.
- Phân tích diện tích.
- So sánh nhà và căn hộ chung cư.

**3. Phân tích khu vực**
- Thống kê số lượng tin đăng theo khu vực.
- So sánh giá/m² giữa các quận, huyện.
- Xác định các khu vực có mức giá trung vị cao và thấp trong mẫu.

**4. Phân tích đặc điểm bất động sản**
- Phân tích diện tích và giá.
- Phân tích số phòng ngủ và giá.
- Phân tích số phòng tắm và giá.
- Phân tích số tầng và giá.

**5. Phân tích hồi quy**
- Hiển thị thông tin các mô hình hồi quy.
- So sánh các chỉ số đánh giá mô hình.
- Theo dõi hệ số hồi quy và kết quả phân tích.

---

## 9. Kết quả đầu ra

Các kết quả phân tích được lưu trong thư mục:

```text
outputs/eda/
```

Trong đó:

- `rq1/`: Biểu đồ và kết quả thống kê phân bố giá, giá/m² và diện tích.
- `rq2/`: Kết quả so sánh nhà và căn hộ.
- `rq3/`: Kết quả phân tích giá theo khu vực.
- `rq4/`: Kết quả phân tích tương quan diện tích và giá.
- `rq5/`: Kết quả phân tích tương quan đặc điểm bất động sản và giá.
- `rq6/`: Kết quả mô hình hồi quy, bảng so sánh mô hình và biểu đồ chẩn đoán.

Dashboard sử dụng các kết quả đã xuất ra từ quá trình phân tích để hiển thị và hỗ trợ người dùng theo dõi.

---

## 10. Một số lưu ý khi sử dụng

- Cần chạy các chương trình xử lý dữ liệu trước khi sử dụng Dashboard nếu dữ liệu đầu vào chưa được tạo.
- Không tự ý thay đổi tên hoặc vị trí file CSV nếu chưa cập nhật lại đường dẫn trong mã nguồn.
- Khi cập nhật dữ liệu, cần chạy lại các bước xử lý và phân tích để đảm bảo kết quả trên Dashboard được đồng bộ.
- Các giá trị thiếu không phải lúc nào cũng được thay thế bằng giá trị trung bình hoặc trung vị; cần xem xét ý nghĩa của từng trường.
- Các giá trị ngoại lệ được giữ lại để kiểm tra và đánh giá, không tự động loại bỏ.
- Kết quả tương quan và hồi quy thể hiện mối liên hệ thống kê, không mặc nhiên chứng minh quan hệ nhân quả.

---

## 11. Kết luận

Dự án đã xây dựng quy trình phân tích dữ liệu bất động sản từ dữ liệu đầu vào đến dữ liệu sau xử lý, phân tích thống kê, mô hình hồi quy và trực quan hóa kết quả.

Thông qua Dashboard, người dùng có thể quan sát các chỉ số quan trọng, so sánh giá giữa các loại hình và khu vực, đồng thời tìm hiểu mối liên hệ giữa giá bất động sản với các đặc điểm của tài sản.

Đây là nền tảng để tiếp tục mở rộng dữ liệu, cải thiện chất lượng phân tích và phát triển các chức năng hỗ trợ tham khảo giá bất động sản trong tương lai.
