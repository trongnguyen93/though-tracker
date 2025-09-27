# 🌐 Thought Tracker Web App - Hướng dẫn sử dụng

## 🚀 Khởi động Web App

### Cách 1: Sử dụng virtual environment (Khuyến nghị)
```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Chạy web app
python app.py
```

### Cách 2: Cài đặt trực tiếp
```bash
# Cài đặt Flask
pip3 install Flask==2.3.3 Werkzeug==2.3.7 --break-system-packages

# Chạy web app
python app.py
```

## 📱 Truy cập Web App

Sau khi chạy thành công, mở trình duyệt và truy cập:

- **Trang chủ**: http://localhost:8080
- **Tìm kiếm**: http://localhost:8080/search  
- **Thống kê**: http://localhost:8080/stats

## ✨ Tính năng Web App

### 🏠 Trang chủ (Home)
- **Form thêm thought mới** với giao diện thân thiện
- **Danh sách thoughts** hiển thị đẹp mắt với:
  - Nội dung thought
  - Keywords (badges màu sắc)
  - Trọng số (sao đánh giá)
  - Ngày giờ tạo
  - Nút xóa
- **Thống kê nhanh** hiển thị số lượng thoughts

### 🔍 Tìm kiếm (Search)
- **Tìm theo keyword** - tìm trong nội dung và keywords
- **Lọc theo trọng số** - min/max weight
- **Kết quả hiển thị** tương tự trang chủ
- **Form tìm kiếm** với các bộ lọc

### 📊 Thống kê (Stats)
- **Tổng quan** số lượng thoughts
- **Phân bố theo trọng số** với biểu đồ thanh tiến trình
- **Top keywords** được sử dụng nhiều nhất
- **Hành động nhanh** để thêm/tìm kiếm

## 🎨 Giao diện

### Thiết kế hiện đại
- **Bootstrap 5** - Responsive design
- **Font Awesome** - Icons đẹp
- **Custom CSS** - Màu sắc và animation
- **Mobile-friendly** - Hoạt động tốt trên điện thoại

### Màu sắc theo trọng số
- 🔴 **Đỏ** - Trọng số 4-5 (Quan trọng)
- 🟡 **Vàng** - Trọng số 3 (Bình thường)  
- 🔵 **Xanh** - Trọng số 1-2 (Ít quan trọng)

## 💡 Cách sử dụng

### 1. Thêm thought mới
1. Mở http://localhost:8080
2. Điền **Nội dung suy nghĩ**
3. Nhập **Keywords** (phân cách bằng dấu phẩy)
4. Chọn **Trọng số** từ 1-5
5. Nhấn **"Lưu suy nghĩ"**

### 2. Tìm kiếm thoughts
1. Vào trang **Tìm kiếm**
2. Nhập từ khóa hoặc chọn trọng số
3. Nhấn **"Tìm kiếm"**
4. Xem kết quả được lọc

### 3. Xem thống kê
1. Vào trang **Thống kê**
2. Xem phân tích dữ liệu
3. Sử dụng **Hành động nhanh**

### 4. Xóa thought
1. Tìm thought cần xóa
2. Nhấn nút **🗑️** (thùng rác)
3. Xác nhận xóa

## 🔧 Tính năng nâng cao

### Auto-suggestions
- Gợi ý keywords phổ biến khi nhập
- Click để thêm vào danh sách

### Responsive Design
- Tự động điều chỉnh trên mobile
- Touch-friendly buttons

### Real-time Feedback
- Thông báo thành công/lỗi
- Auto-hide alerts sau 5 giây

## 🛠️ Troubleshooting

### Port đã được sử dụng
```bash
# Nếu port 8080 bị chiếm, sửa trong app.py
app.run(debug=True, host='0.0.0.0', port=8081)  # Đổi port
```

### Lỗi cài đặt Flask
```bash
# Sử dụng virtual environment
python3 -m venv venv
source venv/bin/activate
pip install Flask==2.3.3 Werkzeug==2.3.7
```

### Database không tồn tại
- Web app sẽ tự động tạo database `thoughts.db`
- Dữ liệu CLI và Web app dùng chung

## 📱 Mobile Usage

Web app được tối ưu cho mobile:
- **Touch gestures** - Vuốt, chạm
- **Responsive layout** - Tự động điều chỉnh
- **Fast loading** - Tải nhanh trên 3G/4G

## 🎯 Tips sử dụng hiệu quả

1. **Keywords nhất quán** - Dùng cùng từ khóa cho chủ đề tương tự
2. **Trọng số hợp lý** - 5 cho việc quan trọng, 1 cho việc nhỏ
3. **Tìm kiếm thường xuyên** - Sử dụng tính năng search
4. **Xem thống kê** - Hiểu pattern suy nghĩ của bạn
5. **Backup dữ liệu** - Copy file `thoughts.db` để backup

---

**🎉 Chúc bạn sử dụng Thought Tracker hiệu quả!**
