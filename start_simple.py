#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的视频审核管理系统启动脚本
使用Python Flask作为后端
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import os
import uuid
from datetime import datetime
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# 创建上传目录
os.makedirs('uploads', exist_ok=True)
os.makedirs('screenshots', exist_ok=True)

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect('video_review.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def add_cors_headers(response):
    """为API响应添加简单的CORS头，便于 GitHub Pages 等静态页跨域访问本地服务"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/test_screenshot_display.html')
def test_screenshot_display():
    """测试截图显示页面"""
    return send_from_directory('.', 'test_screenshot_display.html')

@app.route('/api/projects')
def get_projects():
    """获取项目列表"""
    conn = get_db_connection()
    
    # 获取查询参数
    status = request.args.get('status')
    stage = request.args.get('stage')
    reviewer = request.args.get('reviewer')
    artwork_person = request.args.get('artworkPerson')
    brand = request.args.get('brand')
    provide_date_start = request.args.get('provideDateStart')
    provide_date_end = request.args.get('provideDateEnd')
    selection_date_start = request.args.get('selectionDateStart')
    selection_date_end = request.args.get('selectionDateEnd')
    product_id = request.args.get('productId')
    annotation_status = request.args.get('annotationStatus')
    ued_status = request.args.get('uedStatus')
    
    query = """
        SELECT vp.*, ws.current_stage, ws.completion_status, ws.annotation_reviewer, ws.ued_reviewer, ws.artwork_person,
               (SELECT review_status FROM review_records WHERE project_id = vp.id AND review_type = 'annotation' ORDER BY review_time DESC LIMIT 1) as annotation_status,
               (SELECT review_status FROM review_records WHERE project_id = vp.id AND review_type = 'ued' ORDER BY review_time DESC LIMIT 1) as ued_status
        FROM video_projects vp
        LEFT JOIN workflow_status ws ON vp.id = ws.project_id
    """
    
    conditions = []
    params = []
    
    if status:
        conditions.append('ws.completion_status = ?')
        params.append(status)
    if stage:
        conditions.append('ws.current_stage = ?')
        params.append(stage)
    if reviewer:
        conditions.append('(ws.annotation_reviewer = ? OR ws.ued_reviewer = ? OR ws.artwork_person = ?)')
        params.extend([reviewer, reviewer, reviewer])
    if artwork_person:
        conditions.append('ws.artwork_person = ?')
        params.append(artwork_person)
    if brand:
        conditions.append('vp.brand_name = ?')
        params.append(brand)
    # 提供日期范围
    if provide_date_start and provide_date_end:
        conditions.append('DATE(vp.video_provide_date) BETWEEN ? AND ?')
        params.extend([provide_date_start, provide_date_end])
    elif provide_date_start:
        conditions.append('DATE(vp.video_provide_date) >= ?')
        params.append(provide_date_start)
    elif provide_date_end:
        conditions.append('DATE(vp.video_provide_date) <= ?')
        params.append(provide_date_end)

    # 选品日期范围
    if selection_date_start and selection_date_end:
        conditions.append('DATE(vp.video_selection_date) BETWEEN ? AND ?')
        params.extend([selection_date_start, selection_date_end])
    elif selection_date_start:
        conditions.append('DATE(vp.video_selection_date) >= ?')
        params.append(selection_date_start)
    elif selection_date_end:
        conditions.append('DATE(vp.video_selection_date) <= ?')
        params.append(selection_date_end)
    if product_id:
        conditions.append('vp.product_id LIKE ?')
        params.append(f'%{product_id}%')
    if annotation_status:
        if annotation_status == '未审核':
            conditions.append('(SELECT review_status FROM review_records WHERE project_id = vp.id AND review_type = "annotation" ORDER BY review_time DESC LIMIT 1) IS NULL')
        else:
            conditions.append('(SELECT review_status FROM review_records WHERE project_id = vp.id AND review_type = "annotation" ORDER BY review_time DESC LIMIT 1) = ?')
            params.append(annotation_status)
    if ued_status:
        if ued_status == '未审核':
            conditions.append('(SELECT review_status FROM review_records WHERE project_id = vp.id AND review_type = "ued" ORDER BY review_time DESC LIMIT 1) IS NULL')
        else:
            conditions.append('(SELECT review_status FROM review_records WHERE project_id = vp.id AND review_type = "ued" ORDER BY review_time DESC LIMIT 1) = ?')
            params.append(ued_status)
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' ORDER BY vp.created_at DESC'
    
    projects = conn.execute(query, params).fetchall()
    
    # 为每个项目获取截图数据
    result = []
    for project in projects:
        project_dict = dict(project)
        
        # 获取标注审核截图
        annotation_screenshots = conn.execute("""
            SELECT screenshot_path FROM screenshots 
            WHERE project_id = ? AND review_type = 'annotation'
            ORDER BY created_at DESC
        """, (project_dict['id'],)).fetchall()
        
        # 获取UED审核截图
        ued_screenshots = conn.execute("""
            SELECT screenshot_path FROM screenshots 
            WHERE project_id = ? AND review_type = 'ued'
            ORDER BY created_at DESC
        """, (project_dict['id'],)).fetchall()
        
        project_dict['annotation_screenshots'] = [dict(row) for row in annotation_screenshots]
        project_dict['ued_screenshots'] = [dict(row) for row in ued_screenshots]
        
        result.append(project_dict)
    
    conn.close()
    
    return jsonify(result)

@app.route('/api/projects/<project_id>')
def get_project(project_id):
    """获取项目详情"""
    conn = get_db_connection()
    
    project = conn.execute("""
        SELECT vp.*, ws.current_stage, ws.completion_status, ws.annotation_reviewer, ws.ued_reviewer, ws.artwork_person
        FROM video_projects vp
        LEFT JOIN workflow_status ws ON vp.id = ws.project_id
        WHERE vp.id = ?
    """, (project_id,)).fetchone()
    
    conn.close()
    
    if project:
        return jsonify(dict(project))
    else:
        return jsonify({'error': '项目不存在'}), 404

@app.route('/api/projects/<project_id>/reviews')
def get_project_reviews(project_id):
    """获取项目审核记录"""
    conn = get_db_connection()
    
    reviews = conn.execute("""
        SELECT * FROM review_records 
        WHERE project_id = ? 
        ORDER BY review_time DESC
    """, (project_id,)).fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in reviews])

@app.route('/api/statistics')
def get_statistics():
    """获取统计数据"""
    conn = get_db_connection()
    
    stats = {}
    
    # 总项目数
    stats['total'] = conn.execute('SELECT COUNT(*) FROM video_projects').fetchone()[0]
    
    # 已完成项目数
    stats['completed'] = conn.execute('SELECT COUNT(*) FROM workflow_status WHERE completion_status = "已上传"').fetchone()[0]
    
    # 待处理项目数
    stats['pending'] = conn.execute('SELECT COUNT(*) FROM workflow_status WHERE completion_status = "未上传"').fetchone()[0]
    
    # 各阶段待处理数
    stats['annotation_pending'] = conn.execute('SELECT COUNT(*) FROM workflow_status WHERE current_stage = "annotation_review"').fetchone()[0]
    stats['ued_pending'] = conn.execute('SELECT COUNT(*) FROM workflow_status WHERE current_stage = "ued_review"').fetchone()[0]
    stats['artwork_pending'] = conn.execute('SELECT COUNT(*) FROM workflow_status WHERE current_stage = "artwork"').fetchone()[0]
    
    conn.close()
    
    return jsonify(stats)

@app.route('/api/reviews', methods=['POST'])
def submit_review():
    """提交审核结果"""
    data = request.get_json()
    
    project_id = data.get('projectId')
    review_type = data.get('reviewType')
    reviewer_name = data.get('reviewerName')
    review_status = data.get('reviewStatus')
    problem_description = data.get('problemDescription')
    
    conn = get_db_connection()
    
    # 插入审核记录
    review_id = str(uuid.uuid4())
    conn.execute("""
        INSERT INTO review_records (id, project_id, review_type, reviewer_name, review_status, problem_description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (review_id, project_id, review_type, reviewer_name, review_status, problem_description))
    
    # 更新工作流状态
    if review_type == 'annotation':
        conn.execute("""
            UPDATE workflow_status SET current_stage = ?, annotation_reviewer = ?, updated_at = CURRENT_TIMESTAMP
            WHERE project_id = ?
        """, ('ued_review', reviewer_name, project_id))
    elif review_type == 'ued':
        conn.execute("""
            UPDATE workflow_status SET current_stage = ?, ued_reviewer = ?, updated_at = CURRENT_TIMESTAMP
            WHERE project_id = ?
        """, ('artwork', reviewer_name, project_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'id': review_id, 'message': '审核记录已保存'})

@app.route('/api/workflow/<project_id>', methods=['PUT'])
def update_workflow(project_id):
    """更新工作流状态"""
    data = request.get_json()
    
    current_stage = data.get('currentStage')
    artwork_person = data.get('artworkPerson')
    completion_status = data.get('completionStatus')
    
    conn = get_db_connection()
    
    update_parts = []
    params = []
    
    if current_stage:
        update_parts.append('current_stage = ?')
        params.append(current_stage)
    if artwork_person:
        update_parts.append('artwork_person = ?')
        params.append(artwork_person)
    if completion_status:
        update_parts.append('completion_status = ?')
        params.append(completion_status)
    
    update_parts.append('updated_at = CURRENT_TIMESTAMP')
    params.append(project_id)
    
    query = 'UPDATE workflow_status SET ' + ', '.join(update_parts) + ' WHERE project_id = ?'
    
    conn.execute(query, params)
    conn.commit()
    conn.close()
    
    return jsonify({'message': '工作流状态已更新'})

@app.route('/api/save-screenshot', methods=['POST'])
def save_screenshot():
    """保存截图"""
    try:
        video_id = request.form.get('videoId')
        review_type = request.form.get('reviewType')  # 'annotation' 或 'ued'
        screenshot_data = request.form.get('screenshotData')  # base64数据
        
        if not video_id or not review_type or not screenshot_data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 生成截图文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"screenshot_{video_id}_{review_type}_{timestamp}.png"
        file_path = os.path.join('screenshots', filename)
        
        # 保存base64图片数据
        import base64
        if screenshot_data.startswith('data:image'):
            screenshot_data = screenshot_data.split(',')[1]
        
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(screenshot_data))
        
        # 保存到数据库
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO screenshots (id, project_id, review_type, screenshot_path, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (str(uuid.uuid4()), video_id, review_type, f"/screenshots/{filename}"))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': '截图保存成功',
            'screenshot_path': f"/screenshots/{filename}"
        })
        
    except Exception as e:
        return jsonify({'error': f'保存截图失败: {str(e)}'}), 500

@app.route('/api/toggle-status', methods=['POST'])
def toggle_status():
    """切换验收状态"""
    data = request.get_json()
    
    video_id = data.get('videoId')
    status_type = data.get('type')  # 'annotation' 或 'ued'
    new_status = data.get('status')  # '可用' 或 '不可用'
    review_comment = data.get('comment', '')  # 审核意见
    reviewer_name = data.get('reviewer', '未分配')  # 审核员姓名
    
    conn = get_db_connection()
    
    try:
        # 更新审核记录
        conn.execute("""
            INSERT INTO review_records (id, project_id, review_type, reviewer_name, review_status, problem_description, review_time)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (str(uuid.uuid4()), video_id, status_type, reviewer_name, new_status, review_comment))
        
        # 更新工作流状态
        if status_type == 'annotation':
            conn.execute("""
                UPDATE workflow_status SET annotation_reviewer = ?, updated_at = CURRENT_TIMESTAMP
                WHERE project_id = ?
            """, (reviewer_name, video_id))
        elif status_type == 'ued':
            conn.execute("""
                UPDATE workflow_status SET ued_reviewer = ?, updated_at = CURRENT_TIMESTAMP
                WHERE project_id = ?
            """, (reviewer_name, video_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': '状态已更新'})
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-reviewer', methods=['POST'])
def update_reviewer():
    """更新审核员"""
    data = request.get_json()
    
    video_id = data.get('videoId')
    new_reviewer = data.get('reviewer')
    
    conn = get_db_connection()
    
    try:
        # 更新工作流状态中的审核员
        conn.execute("""
            UPDATE workflow_status SET annotation_reviewer = ?, updated_at = CURRENT_TIMESTAMP
            WHERE project_id = ?
        """, (new_reviewer, video_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': '审核员已更新'})
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-artwork-person', methods=['POST'])
def update_artwork_person():
    """更新加艺术字人员"""
    data = request.get_json()
    
    video_id = data.get('videoId')
    new_person = data.get('artworkPerson')
    
    conn = get_db_connection()
    
    try:
        # 更新工作流状态中的加艺术字人员
        conn.execute("""
            UPDATE workflow_status SET artwork_person = ?, updated_at = CURRENT_TIMESTAMP
            WHERE project_id = ?
        """, (new_person, video_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': '加艺术字人员已更新'})
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-artwork-video', methods=['POST'])
def upload_artwork_video():
    """上传加艺术字视频"""
    try:
        # 检查是否有文件
        if 'videoFile' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['videoFile']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 获取其他参数
        video_id = request.form.get('videoId')
        description = request.form.get('description', '')
        
        if not video_id:
            return jsonify({'error': '缺少视频ID'}), 400
        
        # 检查文件类型
        allowed_extensions = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': '不支持的文件格式，请上传 MP4、AVI、MOV 等视频文件'}), 400
        
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 添加时间戳避免重名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        # 保存文件
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 生成访问URL
        video_url = f"/uploads/{filename}"
        
        # 更新数据库
        conn = get_db_connection()
        
        try:
            # 更新视频项目的加艺术字视频URL
            conn.execute("""
                UPDATE video_projects SET artwork_video_url = ? WHERE id = ?
            """, (video_url, video_id))
            
            # 更新工作流状态到UED审核阶段
            conn.execute("""
                UPDATE workflow_status SET 
                    current_stage = 'ued_review',
                    updated_at = CURRENT_TIMESTAMP
                WHERE project_id = ?
            """, (video_id,))
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'message': '视频上传成功',
                'video_url': video_url,
                'filename': filename
            })
            
        except Exception as e:
            conn.close()
            # 删除已上传的文件
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': f'数据库更新失败: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """提供上传文件的访问"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/screenshots/<filename>')
def screenshot_file(filename):
    """提供截图文件的访问"""
    return send_from_directory('screenshots', filename)

if __name__ == '__main__':
    print("🚀 启动视频审核管理系统...")
    import os as _os
    _port = int(_os.getenv('PORT', '3000'))
    print(f"系统将在 http://localhost:{_port} 运行")
    print("按 Ctrl+C 停止服务器")
    
    app.run(debug=True, host='0.0.0.0', port=_port)
