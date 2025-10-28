#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加screenshots表到数据库
用于存储真实的截图数据
"""

import sqlite3
import os

def add_screenshots_table():
    """添加screenshots表"""
    
    DATABASE = 'video_review.db'
    
    print("📊 添加screenshots表到数据库:")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(DATABASE)
        
        # 创建screenshots表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS screenshots (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                review_type TEXT NOT NULL, -- 'annotation' 或 'ued'
                screenshot_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES video_projects (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ screenshots表创建成功")
        print("📋 表结构:")
        print("   - id: 主键")
        print("   - project_id: 项目ID")
        print("   - review_type: 审核类型 (annotation/ued)")
        print("   - screenshot_path: 截图文件路径")
        print("   - created_at: 创建时间")
        
        print("\n💡 功能说明:")
        print("   - 存储真实的截图数据")
        print("   - 支持标注审核和UED审核截图")
        print("   - 提供缩略图显示")
        print("   - 支持点击放大查看")
        
    except Exception as e:
        print(f"❌ 创建表失败: {e}")

if __name__ == "__main__":
    add_screenshots_table()
