# GitHub Pages 部署指南

## 步骤1：创建GitHub仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `video-review-system` (或您喜欢的名称)
   - **Description**: `视频审核管理系统 - 基于Web的视频生产审核平台`
   - **Visibility**: 选择 "Public" (GitHub Pages需要公开仓库)
   - **Initialize**: 不要勾选任何初始化选项
4. 点击 "Create repository"

## 步骤2：推送代码到GitHub

在终端中执行以下命令：

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/video-review-system.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

## 步骤3：启用GitHub Pages

1. 在GitHub仓库页面，点击 "Settings" 标签
2. 在左侧菜单中找到 "Pages"
3. 在 "Source" 部分选择 "Deploy from a branch"
4. 选择 "main" 分支和 "/ (root)" 文件夹
5. 点击 "Save"

## 步骤4：配置GitHub Pages

由于这是一个Flask应用，需要特殊配置：

### 4.1 创建GitHub Actions工作流

在仓库根目录创建 `.github/workflows/deploy.yml` 文件：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Initialize database
      run: |
        python init_database.py
        python import_excel_data.py
        python add_artwork_video_field.py
        python add_screenshots_table.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
```

### 4.2 创建静态文件版本

由于GitHub Pages主要支持静态网站，我们需要创建一个静态版本：

```bash
# 创建静态版本目录
mkdir static-site
cp templates/index.html static-site/
cp -r screenshots static-site/ 2>/dev/null || true
cp -r uploads static-site/ 2>/dev/null || true
```

## 步骤5：访问您的网站

部署完成后，您的网站将在以下地址可用：
`https://YOUR_USERNAME.github.io/video-review-system`

## 注意事项

1. **数据库文件**: GitHub Pages不支持动态数据库，您可能需要：
   - 使用静态JSON文件替代数据库
   - 或者使用外部数据库服务（如Firebase、Supabase等）

2. **后端API**: GitHub Pages不支持Python后端，您可能需要：
   - 将后端部署到Heroku、Railway、Vercel等平台
   - 或者使用纯前端实现

3. **文件上传**: 静态网站无法处理文件上传，需要：
   - 使用云存储服务（如AWS S3、Cloudinary等）
   - 或者集成第三方文件上传服务

## 替代方案

### 方案1：使用Vercel部署
```bash
# 安装Vercel CLI
npm i -g vercel

# 部署到Vercel
vercel --prod
```

### 方案2：使用Railway部署
1. 访问 [Railway](https://railway.app)
2. 连接GitHub仓库
3. 自动部署Flask应用

### 方案3：使用Heroku部署
```bash
# 安装Heroku CLI
# 创建Procfile
echo "web: python start_simple.py" > Procfile

# 部署到Heroku
heroku create your-app-name
git push heroku main
```

## 推荐部署方案

对于您的Flask应用，我推荐使用 **Railway** 或 **Vercel**，因为它们：
- 支持Python Flask应用
- 提供免费额度
- 自动部署
- 支持数据库和文件存储
- 配置简单
