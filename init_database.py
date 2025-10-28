#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
"""

import sqlite3
import os

def init_database():
    """初始化数据库和表结构"""
    db_file = "video_review.db"
    
    # 如果数据库文件存在，先删除
    if os.path.exists(db_file):
        os.remove(db_file)
        print("删除现有数据库文件")
    
    # 创建数据库连接
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    try:
        # 创建视频项目表
        cursor.execute("""
            CREATE TABLE video_projects (
                id TEXT PRIMARY KEY,
                video_provide_date TEXT,
                video_selection_date TEXT,
                brand_name TEXT,
                category_level1 TEXT,
                category_level2 TEXT,
                category_level3 TEXT,
                video_url TEXT,
                product_id TEXT,
                product_url TEXT,
                material_name_vip TEXT,
                material_name_full TEXT,
                material_price INTEGER,
                material_selling_points TEXT,
                video_file_path TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ 创建视频项目表")
        
        # 创建审核记录表
        cursor.execute("""
            CREATE TABLE review_records (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                review_type TEXT,
                reviewer_name TEXT,
                review_status TEXT,
                problem_description TEXT,
                screenshot_path TEXT,
                review_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES video_projects (id)
            )
        """)
        print("✅ 创建审核记录表")
        
        # 创建工作流状态表
        cursor.execute("""
            CREATE TABLE workflow_status (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                current_stage TEXT,
                annotation_reviewer TEXT,
                ued_reviewer TEXT,
                artwork_person TEXT,
                completion_status TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES video_projects (id)
            )
        """)
        print("✅ 创建工作流状态表")
        
        # 提交事务
        conn.commit()
        print("🎉 数据库初始化完成！")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()


