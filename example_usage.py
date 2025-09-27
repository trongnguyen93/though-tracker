#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ví dụ sử dụng Thought Tracker
"""

from thought_tracker import ThoughtTracker

def demo_usage():
    """Demo cách sử dụng Thought Tracker"""
    print("🚀 Demo Thought Tracker")
    print("=" * 50)
    
    # Khởi tạo tracker
    tracker = ThoughtTracker()
    
    # Thêm một số thoughts mẫu
    print("\n1. Thêm thoughts mẫu:")
    print("-" * 30)
    
    sample_thoughts = [
        ("Hôm nay tôi cảm thấy rất hạnh phúc và biết ơn", ["cảm xúc", "hạnh phúc", "biết ơn"], 5),
        ("Cần lên kế hoạch cho dự án Python mới", ["công việc", "kế hoạch", "python", "dự án"], 4),
        ("Mua sắm cuối tuần cho gia đình", ["mua sắm", "cuối tuần", "gia đình"], 2),
        ("Học thêm về machine learning", ["học tập", "machine learning", "AI"], 4),
        ("Đi chơi với bạn bè tối nay", ["giải trí", "bạn bè", "tối"], 3),
        ("Cần tập thể dục thường xuyên hơn", ["sức khỏe", "tập thể dục", "thói quen"], 3),
    ]
    
    for content, keywords, weight in sample_thoughts:
        tracker.add_thought(content, keywords, weight)
    
    # Hiển thị tất cả thoughts
    print("\n2. Danh sách tất cả thoughts:")
    print("-" * 30)
    tracker.list_thoughts()
    
    # Tìm kiếm theo keyword
    print("\n3. Tìm kiếm theo keyword 'học tập':")
    print("-" * 30)
    tracker.search_thoughts(keyword="học tập")
    
    # Tìm kiếm theo trọng số
    print("\n4. Tìm kiếm thoughts có trọng số >= 4:")
    print("-" * 30)
    tracker.search_thoughts(min_weight=4)
    
    # Tìm kiếm kết hợp
    print("\n5. Tìm kiếm thoughts về 'công việc' với trọng số >= 3:")
    print("-" * 30)
    tracker.search_thoughts(keyword="công việc", min_weight=3)

if __name__ == "__main__":
    demo_usage()
