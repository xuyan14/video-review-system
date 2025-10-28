#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转PDF工具
将产品需求文档和开发文档转换为PDF格式
"""

import markdown
import weasyprint
import os
import sys
from pathlib import Path

def markdown_to_pdf(md_file_path, pdf_file_path, title="文档"):
    """
    将Markdown文件转换为PDF
    
    Args:
        md_file_path (str): Markdown文件路径
        pdf_file_path (str): 输出PDF文件路径
        title (str): PDF标题
    """
    try:
        # 读取Markdown文件
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 转换为HTML
        html = markdown.markdown(md_content, extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        
        # 创建完整的HTML文档
        full_html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    font-size: 12pt;
                    background-color: #fff;
                }}
                
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 20pt;
                    margin-bottom: 10pt;
                    font-weight: 600;
                    page-break-after: avoid;
                }}
                
                h1 {{
                    font-size: 18pt;
                    border-bottom: 2pt solid #3498db;
                    padding-bottom: 8pt;
                    page-break-before: always;
                }}
                
                h1:first-child {{
                    page-break-before: avoid;
                }}
                
                h2 {{
                    font-size: 16pt;
                    border-bottom: 1pt solid #bdc3c7;
                    padding-bottom: 6pt;
                }}
                
                h3 {{
                    font-size: 14pt;
                }}
                
                h4 {{
                    font-size: 13pt;
                }}
                
                p {{
                    margin-bottom: 10pt;
                    text-align: justify;
                    orphans: 2;
                    widows: 2;
                }}
                
                ul, ol {{
                    margin-bottom: 10pt;
                    padding-left: 20pt;
                }}
                
                li {{
                    margin-bottom: 3pt;
                }}
                
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 15pt;
                    font-size: 10pt;
                    page-break-inside: avoid;
                }}
                
                th, td {{
                    border: 1pt solid #ddd;
                    padding: 8pt;
                    text-align: left;
                    vertical-align: top;
                }}
                
                th {{
                    background-color: #f8f9fa;
                    font-weight: 600;
                    color: #2c3e50;
                }}
                
                tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                
                code {{
                    background-color: #f4f4f4;
                    padding: 1pt 3pt;
                    border-radius: 2pt;
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                    font-size: 10pt;
                }}
                
                pre {{
                    background-color: #f8f9fa;
                    border: 1pt solid #e9ecef;
                    border-radius: 3pt;
                    padding: 10pt;
                    overflow-x: auto;
                    margin-bottom: 15pt;
                    font-size: 9pt;
                    page-break-inside: avoid;
                }}
                
                pre code {{
                    background-color: transparent;
                    padding: 0;
                }}
                
                blockquote {{
                    border-left: 3pt solid #3498db;
                    margin: 15pt 0;
                    padding: 8pt 15pt;
                    background-color: #f8f9fa;
                    font-style: italic;
                }}
                
                .page-break {{
                    page-break-before: always;
                }}
                
                /* 确保表格和代码块不会跨页断开 */
                table, pre, blockquote {{
                    page-break-inside: avoid;
                }}
                
                /* 标题后不单独留在一页 */
                h1, h2, h3, h4, h5, h6 {{
                    page-break-after: avoid;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # 转换为PDF
        html_doc = weasyprint.HTML(string=full_html)
        html_doc.write_pdf(pdf_file_path)
        
        print(f"✅ 成功转换: {md_file_path} -> {pdf_file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {md_file_path}")
        print(f"错误信息: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始转换Markdown文档为PDF...")
    
    # 获取当前目录
    current_dir = Path.cwd()
    
    # 定义要转换的文件
    documents = [
        {
            'md_file': '产品需求文档.md',
            'pdf_file': '产品需求文档.pdf',
            'title': '视频审核管理系统 - 产品需求文档'
        },
        {
            'md_file': '开发文档.md',
            'pdf_file': '开发文档.pdf',
            'title': '视频审核管理系统 - 开发文档'
        }
    ]
    
    success_count = 0
    total_count = len(documents)
    
    for doc in documents:
        md_path = current_dir / doc['md_file']
        pdf_path = current_dir / doc['pdf_file']
        
        if md_path.exists():
            if markdown_to_pdf(str(md_path), str(pdf_path), doc['title']):
                success_count += 1
        else:
            print(f"⚠️  文件不存在: {md_path}")
    
    print(f"\n📊 转换完成: {success_count}/{total_count} 个文档成功转换")
    
    if success_count > 0:
        print("\n📁 生成的PDF文件:")
        for doc in documents:
            pdf_path = current_dir / doc['pdf_file']
            if pdf_path.exists():
                file_size = pdf_path.stat().st_size / 1024  # KB
                print(f"   - {doc['pdf_file']} ({file_size:.1f} KB)")
    
    print("\n✨ 转换完成！")

if __name__ == "__main__":
    main()