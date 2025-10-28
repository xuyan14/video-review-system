#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加加艺术字视频字段脚本
"""

import sqlite3

def add_artwork_video_field():
    """添加artwork_video_url字段到video_projects表"""
    
    # 连接数据库
    conn = sqlite3.connect('video_review.db')
    cursor = conn.cursor()
    
    try:
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(video_projects)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'artwork_video_url' not in columns:
            # 添加artwork_video_url字段
            cursor.execute("""
                ALTER TABLE video_projects 
                ADD COLUMN artwork_video_url TEXT
            """)
            print("✅ 成功添加artwork_video_url字段")
        else:
            print("✅ artwork_video_url字段已存在")
        
        # 提交更改
        conn.commit()
        print("✅ 数据库结构更新完成")
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_artwork_video_field()


