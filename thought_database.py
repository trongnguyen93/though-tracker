#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thought Database - PostgreSQL version for Railway deployment
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

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
    
    def __str__(self) -> str:
        return f"[{self.date}] (Trọng số: {self.weight}) {self.content} | Keywords: {', '.join(self.keywords)}"

class ThoughtDatabase:
    """Class quản lý database PostgreSQL cho thoughts"""
    
    def __init__(self):
        # Fix cứng DATABASE_URL cho Railway
        self.conn_string = os.getenv('DATABASE_URL', 'postgresql://postgres:lzpcAASVLlVjjuAZUzvhduNLIfLPPQWZ@postgres.railway.internal:5432/railway')
        print(f"DEBUG: Using DATABASE_URL = {self.conn_string}")
        self.init_database()
    
    def get_connection(self):
        """Tạo connection đến PostgreSQL"""
        return psycopg2.connect(self.conn_string)
    
    
    def init_database(self):
        """Khởi tạo database và tạo bảng thoughts"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS thoughts (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    keywords JSONB NOT NULL,
                    weight INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    image_path TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def add_thought(self, thought: Thought) -> int:
        """Thêm thought mới vào database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO thoughts (content, keywords, weight, date, image_path)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        ''', (thought.content, json.dumps(thought.keywords), thought.weight, thought.date, thought.image_path))
        
        thought_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return thought_id
    
    def get_all_thoughts(self) -> List[Thought]:
        """Lấy tất cả thoughts"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('SELECT * FROM thoughts ORDER BY date DESC')
        rows = cursor.fetchall()
        
        thoughts = []
        for row in rows:
            thought = Thought(
                content=row['content'],
                keywords=row['keywords'],
                weight=row['weight'],
                date=row['date'],
                image_path=row['image_path']
            )
            thought.id = row['id']
            thoughts.append(thought)
        
        conn.close()
        return thoughts
    
    def search_thoughts(self, keyword: str = None, min_weight: int = None, max_weight: int = None,
                       start_date: str = None, end_date: str = None) -> List[Thought]:
        """Tìm kiếm thoughts theo keyword hoặc trọng số"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Xây dựng query cho PostgreSQL
        query = 'SELECT * FROM thoughts WHERE 1=1'
        params = []
        
        if min_weight is not None:
            query += ' AND weight >= %s'
            params.append(min_weight)
        
        if max_weight is not None:
            query += ' AND weight <= %s'
            params.append(max_weight)
        
        if start_date:
            query += ' AND date >= %s'
            params.append(start_date)
        
        if end_date:
            query += ' AND date <= %s'
            params.append(end_date)
        
        query += ' ORDER BY date DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        thoughts = []
        for row in rows:
            thought = Thought(
                content=row['content'],
                keywords=row['keywords'],
                weight=row['weight'],
                date=row['date'],
                image_path=row['image_path']
            )
            thought.id = row['id']
            
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
        """Xóa thought theo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM thoughts WHERE id = %s', (thought_id,))
        
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
