#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thought Tracker - Ứng dụng theo dõi suy nghĩ với keywords, ngày tháng và trọng số
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import argparse
import sys

class Thought:
    """Class đại diện cho một suy nghĩ"""
    
    def __init__(self, content: str, keywords: List[str], weight: int, date: str = None, image_path: str = None):
        self.content = content
        self.keywords = keywords
        self.weight = weight  # Trọng số từ 1-5
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.image_path = image_path  # Đường dẫn ảnh
        self.id = None
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'content': self.content,
            'keywords': self.keywords,
            'weight': self.weight,
            'date': self.date,
            'image_path': self.image_path
        }
    
    def __str__(self):
        return f"[{self.date}] (Trọng số: {self.weight}) {self.content} | Keywords: {', '.join(self.keywords)}"

class ThoughtDatabase:
    """Class quản lý database cho thoughts"""
    
    def __init__(self, db_path: str = "thoughts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database và tạo bảng thoughts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS thoughts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                keywords TEXT NOT NULL,
                weight INTEGER NOT NULL,
                date TEXT NOT NULL,
                image_path TEXT
            )
        ''')
        
        # Kiểm tra và thêm cột image_path nếu chưa có (cho database cũ)
        try:
            cursor.execute("ALTER TABLE thoughts ADD COLUMN image_path TEXT")
            conn.commit()
        except sqlite3.OperationalError:
            # Cột đã tồn tại, bỏ qua
            pass
        
        conn.commit()
        conn.close()
    
    def add_thought(self, thought: Thought) -> int:
        """Thêm một thought mới vào database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO thoughts (content, keywords, weight, date, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (thought.content, json.dumps(thought.keywords), thought.weight, thought.date, thought.image_path))
        
        thought_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return thought_id
    
    def get_all_thoughts(self) -> List[Thought]:
        """Lấy tất cả thoughts từ database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, content, keywords, weight, date, image_path FROM thoughts ORDER BY date DESC')
        rows = cursor.fetchall()
        
        thoughts = []
        for row in rows:
            thought = Thought(
                content=row[1],
                keywords=json.loads(row[2]),
                weight=row[3],
                date=row[4],
                image_path=row[5]
            )
            thought.id = row[0]
            thoughts.append(thought)
        
        conn.close()
        return thoughts
    
    def search_thoughts(self, keyword: str = None, min_weight: int = None, max_weight: int = None, 
                       start_date: str = None, end_date: str = None) -> List[Thought]:
        """Tìm kiếm thoughts theo keyword hoặc trọng số"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Lấy tất cả thoughts trước
        query = 'SELECT id, content, keywords, weight, date, image_path FROM thoughts WHERE 1=1'
        params = []
        
        if min_weight is not None:
            query += ' AND weight >= ?'
            params.append(min_weight)
        
        if max_weight is not None:
            query += ' AND weight <= ?'
            params.append(max_weight)
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY date DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        thoughts = []
        for row in rows:
            thought = Thought(
                content=row[1],
                keywords=json.loads(row[2]),
                weight=row[3],
                date=row[4],
                image_path=row[5]
            )
            thought.id = row[0]
            
            # Tìm kiếm keyword trong Python (hỗ trợ Unicode)
            if keyword:
                keyword_lower = keyword.lower()
                content_match = keyword_lower in thought.content.lower()
                keywords_match = any(keyword_lower in kw.lower() for kw in thought.keywords)
                
                if content_match or keywords_match:
                    thoughts.append(thought)
            else:
                thoughts.append(thought)
        
        conn.close()
        return thoughts
    
    def delete_thought(self, thought_id: int) -> bool:
        """Xóa một thought theo ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM thoughts WHERE id = ?', (thought_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted

class ThoughtTracker:
    """Class chính để quản lý thoughts"""
    
    def __init__(self):
        self.db = ThoughtDatabase()
    
    def add_thought(self, content: str, keywords: List[str], weight: int, image_path: str = None):
        """Thêm một thought mới"""
        if not 1 <= weight <= 5:
            raise ValueError("Trọng số phải từ 1 đến 5")
        
        thought = Thought(content, keywords, weight, image_path=image_path)
        thought_id = self.db.add_thought(thought)
        print(f"✅ Đã thêm thought với ID: {thought_id}")
        return thought_id
    
    def list_thoughts(self, limit: int = None):
        """Hiển thị danh sách thoughts"""
        thoughts = self.db.get_all_thoughts()
        
        if limit:
            thoughts = thoughts[:limit]
        
        if not thoughts:
            print("📝 Chưa có thought nào được lưu.")
            return
        
        print(f"\n📚 Danh sách thoughts ({len(thoughts)} thoughts):")
        print("-" * 80)
        
        for thought in thoughts:
            print(f"ID: {thought.id} | {thought}")
    
    def search_thoughts(self, keyword: str = None, min_weight: int = None, max_weight: int = None, 
                       start_date: str = None, end_date: str = None):
        """Tìm kiếm thoughts"""
        thoughts = self.db.search_thoughts(keyword, min_weight, max_weight, start_date, end_date)
        
        if not thoughts:
            print("🔍 Không tìm thấy thought nào phù hợp.")
            return
        
        print(f"\n🔍 Kết quả tìm kiếm ({len(thoughts)} thoughts):")
        print("-" * 80)
        
        for thought in thoughts:
            print(f"ID: {thought.id} | {thought}")
    
    def delete_thought(self, thought_id: int):
        """Xóa một thought"""
        if self.db.delete_thought(thought_id):
            print(f"🗑️ Đã xóa thought với ID: {thought_id}")
        else:
            print(f"❌ Không tìm thấy thought với ID: {thought_id}")

def main():
    """Hàm main cho CLI"""
    parser = argparse.ArgumentParser(description="Thought Tracker - Theo dõi suy nghĩ của bạn")
    subparsers = parser.add_subparsers(dest='command', help='Các lệnh có sẵn')
    
    # Lệnh add
    add_parser = subparsers.add_parser('add', help='Thêm một thought mới')
    add_parser.add_argument('content', help='Nội dung thought')
    add_parser.add_argument('keywords', help='Keywords (phân cách bằng dấu phẩy)')
    add_parser.add_argument('weight', type=int, help='Trọng số từ 1-5')
    
    # Lệnh list
    list_parser = subparsers.add_parser('list', help='Hiển thị danh sách thoughts')
    list_parser.add_argument('--limit', type=int, help='Giới hạn số lượng hiển thị')
    
    # Lệnh search
    search_parser = subparsers.add_parser('search', help='Tìm kiếm thoughts')
    search_parser.add_argument('--keyword', help='Từ khóa tìm kiếm')
    search_parser.add_argument('--min-weight', type=int, help='Trọng số tối thiểu')
    search_parser.add_argument('--max-weight', type=int, help='Trọng số tối đa')
    
    # Lệnh delete
    delete_parser = subparsers.add_parser('delete', help='Xóa một thought')
    delete_parser.add_argument('id', type=int, help='ID của thought cần xóa')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tracker = ThoughtTracker()
    
    try:
        if args.command == 'add':
            keywords = [k.strip() for k in args.keywords.split(',')]
            tracker.add_thought(args.content, keywords, args.weight)
        
        elif args.command == 'list':
            tracker.list_thoughts(args.limit)
        
        elif args.command == 'search':
            tracker.search_thoughts(args.keyword, args.min_weight, args.max_weight)
        
        elif args.command == 'delete':
            tracker.delete_thought(args.id)
    
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
