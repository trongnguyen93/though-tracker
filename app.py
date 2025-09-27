#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thought Tracker Web App - Giao diện web để quản lý suy nghĩ
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from thought_tracker import ThoughtTracker, Thought
import json
import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = 'thought_tracker_secret_key_2024'

# Cấu hình upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Tạo thư mục upload nếu chưa có
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Khởi tạo tracker
tracker = ThoughtTracker()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image_path, max_size=(800, 600)):
    """Resize ảnh để tối ưu kích thước"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(image_path, optimize=True, quality=85)
    except Exception as e:
        print(f"Lỗi resize ảnh: {e}")

@app.route('/')
def index():
    """Trang chủ - hiển thị form thêm thought và danh sách"""
    thoughts = tracker.db.get_all_thoughts()
    return render_template('index.html', thoughts=thoughts)

@app.route('/add', methods=['POST'])
def add_thought():
    """Thêm thought mới"""
    try:
        content = request.form.get('content', '').strip()
        keywords_str = request.form.get('keywords', '').strip()
        weight = int(request.form.get('weight', 1))
        
        if not content:
            flash('Vui lòng nhập nội dung suy nghĩ!', 'error')
            return redirect(url_for('index'))
        
        if not keywords_str:
            flash('Vui lòng nhập ít nhất một keyword!', 'error')
            return redirect(url_for('index'))
        
        if not 1 <= weight <= 5:
            flash('Trọng số phải từ 1 đến 5!', 'error')
            return redirect(url_for('index'))
        
        # Chuyển keywords thành list
        keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
        
        # Xử lý upload ảnh
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Tạo tên file unique
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4()}.{file_extension}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                file.save(file_path)
                resize_image(file_path)  # Resize để tối ưu
                image_path = f"uploads/{unique_filename}"
            elif file and file.filename:
                flash('Định dạng file không được hỗ trợ! Chỉ chấp nhận: PNG, JPG, JPEG, GIF, WEBP', 'error')
                return redirect(url_for('index'))
        
        # Thêm thought
        thought_id = tracker.add_thought(content, keywords, weight, image_path)
        flash(f'✅ Đã thêm thought thành công! (ID: {thought_id})', 'success')
        
    except Exception as e:
        flash(f'❌ Lỗi: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:thought_id>')
def delete_thought(thought_id):
    """Xóa thought"""
    try:
        if tracker.db.delete_thought(thought_id):
            flash(f'🗑️ Đã xóa thought ID: {thought_id}', 'success')
        else:
            flash(f'❌ Không tìm thấy thought ID: {thought_id}', 'error')
    except Exception as e:
        flash(f'❌ Lỗi: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/search')
def search_thoughts():
    """Tìm kiếm thoughts"""
    keyword = request.args.get('keyword', '').strip()
    min_weight = request.args.get('min_weight', type=int)
    max_weight = request.args.get('max_weight', type=int)
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    
    # Debug log
    print(f"DEBUG: keyword='{keyword}', min_weight={min_weight}, max_weight={max_weight}")
    
    # Nếu không có tham số tìm kiếm, hiển thị tất cả
    if not keyword and min_weight is None and max_weight is None and not start_date and not end_date:
        thoughts = tracker.db.get_all_thoughts()
    else:
        thoughts = tracker.db.search_thoughts(keyword, min_weight, max_weight, start_date, end_date)
    
    print(f"DEBUG: Found {len(thoughts)} thoughts")
    
    return render_template('search_results.html', 
                         thoughts=thoughts, 
                         keyword=keyword,
                         min_weight=min_weight,
                         max_weight=max_weight,
                         start_date=start_date,
                         end_date=end_date)

@app.route('/api/thoughts')
def api_thoughts():
    """API endpoint để lấy thoughts dưới dạng JSON"""
    thoughts = tracker.db.get_all_thoughts()
    return jsonify([thought.to_dict() for thought in thoughts])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/stats')
def stats():
    """Trang thống kê"""
    # Lấy tham số filter
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    
    # Lấy thoughts theo filter
    if start_date or end_date:
        thoughts = tracker.db.search_thoughts(start_date=start_date, end_date=end_date)
    else:
        thoughts = tracker.db.get_all_thoughts()
    
    # Thống kê cơ bản
    total_thoughts = len(thoughts)
    weight_stats = {}
    keyword_stats = {}
    keyword_weight_stats = {}  # Tổng trọng số cho mỗi keyword
    daily_stats = {}
    
    for thought in thoughts:
        # Thống kê theo trọng số
        weight = thought.weight
        weight_stats[weight] = weight_stats.get(weight, 0) + 1
        
        # Thống kê theo keyword
        for keyword in thought.keywords:
            keyword_stats[keyword] = keyword_stats.get(keyword, 0) + 1
            # Tổng trọng số cho keyword
            keyword_weight_stats[keyword] = keyword_weight_stats.get(keyword, 0) + weight
        
        # Thống kê theo ngày
        date_only = thought.date.split(' ')[0]  # Lấy phần ngày
        daily_stats[date_only] = daily_stats.get(date_only, 0) + 1
    
    # Sắp xếp keywords theo tần suất
    top_keywords = sorted(keyword_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Sắp xếp keywords theo tổng trọng số cho bubble chart
    bubble_keywords = sorted(keyword_weight_stats.items(), key=lambda x: x[1], reverse=True)[:15]
    
    # Sắp xếp daily stats theo ngày
    sorted_daily = sorted(daily_stats.items())
    
    return render_template('stats.html', 
                         total_thoughts=total_thoughts,
                         weight_stats=weight_stats,
                         top_keywords=top_keywords,
                         bubble_keywords=bubble_keywords,
                         daily_stats=sorted_daily,
                         start_date=start_date,
                         end_date=end_date)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    if debug_mode:
        print("🚀 Khởi động Thought Tracker Web App...")
        print("📱 Truy cập: http://localhost:8081")
        print("📊 Thống kê: http://localhost:8081/stats")
        print("🔍 Tìm kiếm: http://localhost:8081/search")
        print("\n💡 Nhấn Ctrl+C để dừng server")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
