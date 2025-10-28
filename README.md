# 视频审核管理系统

## 项目简介

本系统是一个基于Web的视频审核管理平台，旨在将传统的离线视频生产审核流程线上化，提升视频生产审核效率。系统支持完整的视频审核工作流，包括标注审核、UED审核、加艺术字等环节。

## 功能特性

### 🎯 核心功能
- **视频管理**：支持视频信息展示、分类管理、状态跟踪
- **审核工作流**：完整的标注审核 → 加艺术字 → UED审核流程
- **在线审核**：支持视频播放、截图、审核意见填写
- **人员管理**：审核员分配、批量操作支持
- **文件管理**：视频上传、批量下载、文件预览

### 🔧 辅助功能
- **多维度筛选**：按日期、品牌、商品ID、审核状态等筛选
- **自定义列显示**：用户可自定义表格列显示
- **实时状态更新**：审核状态实时同步
- **截图管理**：审核截图存储和展示
- **数据统计**：审核进度统计和展示

## 技术架构

- **前端**：HTML5 + CSS3 + JavaScript + Bootstrap 5
- **后端**：Python 3.9+ + Flask
- **数据库**：SQLite3
- **文件存储**：本地文件系统

## 快速开始

### 环境要求
- Python 3.9+
- 现代浏览器（Chrome 80+, Firefox 75+, Safari 13+, Edge 80+）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd video_review_system
```

2. **创建虚拟环境**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **初始化数据库**
```bash
python init_database.py
python import_excel_data.py
python add_artwork_video_field.py
python add_screenshots_table.py
```

5. **启动应用**
```bash
python start_simple.py
```

6. **访问系统**
打开浏览器访问：http://localhost:3000

## 项目结构

```
video_review_system/
├── start_simple.py              # Flask应用主文件
├── templates/
│   └── index.html              # 前端页面模板
├── requirements.txt             # Python依赖包
├── video_review.db             # SQLite数据库文件
├── screenshots/                # 截图文件存储目录
├── uploads/                    # 上传文件存储目录
├── init_database.py            # 数据库初始化脚本
├── import_excel_data.py        # Excel数据导入脚本
├── add_artwork_video_field.py  # 数据库字段添加脚本
├── add_screenshots_table.py    # 截图表创建脚本
├── 产品需求文档.md             # 产品需求文档
├── 开发文档.md                 # 开发文档
└── 工作簿3.xlsx               # 原始Excel数据文件
```

## 使用说明

### 审核流程

1. **视频生产完成** → 系统显示"待标注审核"状态
2. **分配标注审核员** → 在任务列表中分配审核员
3. **标注审核** → 点击原始视频眼睛图标进入审核页面
4. **审核操作** → 播放视频、截取问题画面、填写审核意见
5. **提交审核** → 选择通过/不通过，提交审核结果
6. **加艺术字** → 审核通过后上传加艺术字视频
7. **UED审核** → UED审核员审核加艺术字视频
8. **流程完成** → 审核通过后流程结束

### 主要操作

- **筛选数据**：使用顶部筛选条件快速找到目标视频
- **批量操作**：选择多个视频进行批量分配或下载
- **自定义列**：点击"列设置"按钮自定义表格显示列
- **审核操作**：点击眼睛图标进入审核页面进行操作
- **文件上传**：在"待加艺术字"状态下上传加艺术字视频

## API接口

### 主要接口

- `GET /api/projects` - 获取项目列表
- `GET /api/statistics` - 获取统计数据
- `POST /api/update-reviewer` - 更新审核员
- `POST /api/toggle-status` - 切换审核状态
- `POST /api/save-screenshot` - 保存截图
- `POST /api/upload-artwork-video` - 上传加艺术字视频

详细API文档请参考[开发文档.md](./开发文档.md)

## 数据库设计

### 主要表结构

- `video_projects` - 视频项目信息
- `workflow_status` - 工作流状态
- `review_records` - 审核记录
- `screenshots` - 截图信息

详细数据库设计请参考[开发文档.md](./开发文档.md)

## 开发文档

- [产品需求文档](./产品需求文档.md) - 详细的产品需求和功能说明
- [开发文档](./开发文档.md) - 技术架构、API设计、部署说明等

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

如有问题或建议，请通过以下方式联系：

- 项目Issues：[GitHub Issues](https://github.com/your-repo/issues)
- 邮箱：your-email@example.com

## 更新日志

### v1.0.1 (2025-10-27)
- 修复GitHub Pages部署问题
- 优化部署工作流配置
- 完善文档和说明

### v1.0.0 (2025-10-27)
- 初始版本发布
- 完整的视频审核工作流
- 支持标注审核和UED审核
- 截图功能和文件上传
- 自定义列显示和批量操作
