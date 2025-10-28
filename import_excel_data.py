#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel数据导入脚本 - 将Excel数据导入到视频审核管理系统
"""

import pandas as pd
import sqlite3
import json
import os
from datetime import datetime
import uuid

def import_excel_to_database(excel_file, db_file):
    """
    将Excel数据导入到SQLite数据库
    """
    try:
        # 读取Excel文件
        print("正在读取Excel文件...")
        df = pd.read_excel(excel_file)
        print(f"成功读取 {len(df)} 条记录")
        
        # 连接数据库
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 清空现有数据
        print("清空现有数据...")
        cursor.execute("DELETE FROM review_records")
        cursor.execute("DELETE FROM workflow_status")
        cursor.execute("DELETE FROM video_projects")
        
        # 导入数据
        print("开始导入数据...")
        
        for index, row in df.iterrows():
            # 生成项目ID
            project_id = str(uuid.uuid4())
            
            # 处理日期格式
            video_provide_date = row['视频提供日期'].strftime('%Y-%m-%d') if pd.notna(row['视频提供日期']) else None
            video_selection_date = row['视频选品日期'].strftime('%Y-%m-%d') if pd.notna(row['视频选品日期']) else None
            
            # 处理素材卖点（转换为JSON字符串）
            selling_points = row['素材卖点'] if pd.notna(row['素材卖点']) else '[]'
            if isinstance(selling_points, str) and selling_points.startswith('['):
                # 已经是字符串格式，直接使用
                pass
            else:
                selling_points = '[]'
            
            # 插入视频项目数据
            cursor.execute("""
                INSERT INTO video_projects (
                    id, video_provide_date, video_selection_date, brand_name, 
                    category_level1, category_level2, category_level3, 
                    video_url, product_id, product_url, material_name_vip, 
                    material_name_full, material_price, material_selling_points, 
                    video_file_path, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                project_id,
                video_provide_date,
                video_selection_date,
                row['品牌名称'],
                row['一级品类'],
                row['二级品类'],
                row['三级品类'],
                row['视频链接'] if pd.notna(row['视频链接']) else None,
                str(row['商品ID']),
                row['商品链接'],
                row['素材命名（只要VIP字段）'],
                row['素材命名（完整字段）'],
                int(row['素材售价']) if pd.notna(row['素材售价']) else 0,
                selling_points,
                None,  # video_file_path
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            # 确定当前阶段
            current_stage = 'production'
            if pd.notna(row['标注验收']):
                current_stage = 'annotation_review'
            if pd.notna(row['ued验收']):
                current_stage = 'ued_review'
            if pd.notna(row['加艺术字人员']):
                current_stage = 'artwork'
            if row['完成情况'] == '已上传':
                current_stage = 'completed'
            
            # 插入工作流状态
            workflow_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO workflow_status (
                    id, project_id, current_stage, annotation_reviewer, 
                    ued_reviewer, artwork_person, completion_status, 
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                workflow_id,
                project_id,
                current_stage,
                row['验收人员'] if pd.notna(row['验收人员']) else None,
                None,  # ued_reviewer 从Excel中无法直接获取
                row['加艺术字人员'] if pd.notna(row['加艺术字人员']) else None,
                row['完成情况'] if pd.notna(row['完成情况']) else '未上传',
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            # 插入标注审核记录
            if pd.notna(row['标注验收']):
                review_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO review_records (
                        id, project_id, review_type, reviewer_name, 
                        review_status, problem_description, screenshot_path, review_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review_id,
                    project_id,
                    'annotation',
                    row['验收人员'] if pd.notna(row['验收人员']) else '未知',
                    row['标注验收'],
                    row['问题描述'] if pd.notna(row['问题描述']) else None,
                    None,  # screenshot_path
                    datetime.now().isoformat()
                ))
            
            # 插入UED审核记录
            if pd.notna(row['ued验收']):
                review_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO review_records (
                        id, project_id, review_type, reviewer_name, 
                        review_status, problem_description, screenshot_path, review_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review_id,
                    project_id,
                    'ued',
                    'UED审核员',  # Excel中没有UED审核员信息
                    row['ued验收'],
                    row['问题描述.1'] if pd.notna(row['问题描述.1']) else None,
                    None,  # screenshot_path
                    datetime.now().isoformat()
                ))
        
        # 提交事务
        conn.commit()
        print("✅ 数据导入完成！")
        
        # 显示统计信息
        cursor.execute("SELECT COUNT(*) FROM video_projects")
        project_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM review_records")
        review_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM workflow_status")
        workflow_count = cursor.fetchone()[0]
        
        print(f"📊 导入统计:")
        print(f"   - 项目数量: {project_count}")
        print(f"   - 审核记录: {review_count}")
        print(f"   - 工作流状态: {workflow_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

if __name__ == "__main__":
    excel_file = "工作簿3.xlsx"
    db_file = "video_review.db"
    
    if not os.path.exists(excel_file):
        print(f"❌ 错误: 找不到Excel文件 {excel_file}")
        exit(1)
    
    print("🔄 开始导入Excel数据到视频审核管理系统...")
    success = import_excel_to_database(excel_file, db_file)
    
    if success:
        print("🎉 数据导入成功！现在可以启动系统了。")
        print("运行命令: ./start.sh 或 node server.js")
    else:
        print("💥 数据导入失败，请检查错误信息。")


