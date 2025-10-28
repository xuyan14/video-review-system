# 🚀 视频审核管理系统 - GitHub Pages 部署指南

## 📋 部署概览

本项目已配置支持GitHub Pages部署，包含以下内容：
- ✅ 静态演示页面 (`index.html`)
- ✅ GitHub Actions工作流 (`.github/workflows/deploy.yml`)
- ✅ 完整的项目文档
- ✅ 部署指南和说明

## 🎯 快速部署步骤

### 步骤1：创建GitHub仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   ```
   Repository name: video-review-system
   Description: 视频审核管理系统 - 基于Web的视频生产审核平台
   Visibility: Public ✅
   Initialize: 不要勾选任何选项
   ```
4. 点击 "Create repository"

### 步骤2：推送代码到GitHub

在项目目录中执行以下命令：

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/video-review-system.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

### 步骤3：启用GitHub Pages

1. 在GitHub仓库页面，点击 **"Settings"** 标签
2. 在左侧菜单中找到 **"Pages"**
3. 在 **"Source"** 部分选择 **"GitHub Actions"**
4. 保存设置

### 步骤4：等待部署完成

- GitHub Actions会自动开始部署
- 部署完成后，您的网站将在以下地址可用：
  ```
  https://YOUR_USERNAME.github.io/video-review-system
  ```

## 🌐 访问您的网站

部署成功后，您可以通过以下方式访问：

1. **GitHub Pages URL**: `https://YOUR_USERNAME.github.io/video-review-system`
2. **自定义域名**（可选）：在Pages设置中配置自定义域名

## 📁 项目结构

```
video-review-system/
├── index.html                    # GitHub Pages静态演示页面
├── templates/
│   └── index.html               # 完整功能页面（需要后端）
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions部署工作流
├── start_simple.py              # Flask应用主文件
├── requirements.txt             # Python依赖
├── README.md                    # 项目说明
├── 产品需求文档.md              # 产品需求文档
├── 开发文档.md                  # 开发文档
└── GitHub部署指南.md            # 本文件
```

## 🔧 功能说明

### GitHub Pages版本
- **静态演示页面**：展示项目介绍、功能特性、技术架构
- **部署指南**：详细的部署和使用说明
- **项目文档**：完整的产品需求和开发文档

### 完整功能版本
- **需要本地部署**：由于GitHub Pages不支持Python后端
- **完整功能**：视频播放、审核、截图、文件上传等
- **数据库支持**：SQLite数据库和文件存储

## 🚀 本地运行完整功能

如果您需要运行完整功能，请按照以下步骤：

```bash
# 1. 克隆项目
git clone https://github.com/YOUR_USERNAME/video-review-system.git
cd video-review-system

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库
python init_database.py
python import_excel_data.py
python add_artwork_video_field.py
python add_screenshots_table.py

# 5. 启动应用
python start_simple.py

# 6. 访问系统
# 打开浏览器访问：http://localhost:3000
```

## 🌟 功能特性

### 核心功能
- ✅ **视频管理**：视频信息展示、分类管理、状态跟踪
- ✅ **审核工作流**：标注审核 → 加艺术字 → UED审核
- ✅ **在线审核**：视频播放、截图、审核意见填写
- ✅ **人员管理**：审核员分配、批量操作
- ✅ **文件管理**：视频上传、批量下载
- ✅ **数据统计**：审核进度统计和展示

### 技术特性
- ✅ **响应式设计**：适配不同屏幕尺寸
- ✅ **自定义列显示**：用户可自定义表格列
- ✅ **多维度筛选**：按多种条件筛选数据
- ✅ **实时状态更新**：审核状态实时同步
- ✅ **截图管理**：审核截图存储和展示

## 📊 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端 (HTML)   │    │   后端 (Flask)  │    │   数据库 (SQLite)│
│                 │    │                 │    │                 │
│  - Bootstrap 5  │◄──►│  - Python Flask │◄──►│  - SQLite3      │
│  - JavaScript   │    │  - RESTful API  │    │  - 关系型数据库  │
│  - CSS3         │    │  - 文件上传     │    │  - 事务支持      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 更新和维护

### 更新代码
```bash
# 修改代码后
git add .
git commit -m "Update: 描述您的更改"
git push origin main
```

### 重新部署
- GitHub Actions会自动检测到代码更新
- 自动重新部署到GitHub Pages
- 无需手动操作

## 🆘 常见问题

### Q: GitHub Pages显示404错误？
A: 检查以下项目：
- 确保仓库是Public
- 确保Pages源设置为"GitHub Actions"
- 等待Actions部署完成

### Q: 如何运行完整功能？
A: GitHub Pages只支持静态网站，完整功能需要：
- 本地部署Flask应用
- 或使用支持Python的平台（如Railway、Heroku）

### Q: 如何自定义域名？
A: 在Pages设置中添加自定义域名，并配置DNS记录

## 📞 支持和反馈

- **GitHub Issues**: [项目Issues](https://github.com/YOUR_USERNAME/video-review-system/issues)
- **文档**: [产品需求文档](./产品需求文档.md) | [开发文档](./开发文档.md)
- **演示**: [GitHub Pages演示](https://YOUR_USERNAME.github.io/video-review-system)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

🎉 **恭喜！** 您的视频审核管理系统已成功部署到GitHub Pages！