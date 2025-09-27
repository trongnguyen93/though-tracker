# Thought Tracker 📝

Ứng dụng Python để theo dõi và quản lý những suy nghĩ của bạn với các tính năng:
- **Keywords**: Gắn từ khóa cho mỗi suy nghĩ
- **Ngày tháng**: Tự động ghi nhận thời gian
- **Trọng số**: Đánh giá mức độ quan trọng từ 1-5

## Cài đặt

```bash
# Clone hoặc tải project
cd "Tracking what I think"

# Không cần cài đặt thư viện bên ngoài
python3 thought_tracker.py --help
```

## Cách sử dụng

### 1. Thêm một thought mới
```bash
python3 thought_tracker.py add "Tôi cần học Python" "học tập, python, lập trình" 4
```

### 2. Xem danh sách thoughts
```bash
# Xem tất cả
python3 thought_tracker.py list

# Giới hạn số lượng
python3 thought_tracker.py list --limit 5
```

### 3. Tìm kiếm thoughts
```bash
# Tìm theo keyword
python3 thought_tracker.py search --keyword "học tập"

# Tìm theo trọng số
python3 thought_tracker.py search --min-weight 4

# Tìm kết hợp
python3 thought_tracker.py search --keyword "python" --min-weight 3
```

### 4. Xóa thought
```bash
python3 thought_tracker.py delete 1
```

## Cấu trúc dữ liệu

Mỗi thought bao gồm:
- **ID**: Số thứ tự tự động
- **Content**: Nội dung suy nghĩ
- **Keywords**: Danh sách từ khóa (phân cách bằng dấu phẩy)
- **Weight**: Trọng số từ 1-5
- **Date**: Ngày giờ tạo (tự động)

## Ví dụ sử dụng

```bash
# Thêm một số thoughts mẫu
python3 thought_tracker.py add "Hôm nay tôi cảm thấy rất hạnh phúc" "cảm xúc, hạnh phúc, tích cực" 5
python3 thought_tracker.py add "Cần lên kế hoạch cho dự án mới" "công việc, kế hoạch, dự án" 4
python3 thought_tracker.py add "Mua sắm cuối tuần" "mua sắm, cuối tuần, cá nhân" 2

# Xem tất cả
python3 thought_tracker.py list

# Tìm thoughts quan trọng
python3 thought_tracker.py search --min-weight 4

# Tìm thoughts về công việc
python3 thought_tracker.py search --keyword "công việc"
```

## Lưu trữ dữ liệu

Dữ liệu được lưu trong file `thoughts.db` (SQLite database) trong cùng thư mục với script.

## Tính năng

- ✅ Thêm, xem, tìm kiếm, xóa thoughts
- ✅ Tìm kiếm theo keyword và trọng số
- ✅ Lưu trữ dữ liệu persistent với SQLite
- ✅ CLI interface dễ sử dụng
- ✅ Hỗ trợ tiếng Việt
