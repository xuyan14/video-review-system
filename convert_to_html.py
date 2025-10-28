#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转HTML工具
将产品需求文档和开发文档转换为HTML格式，便于打印为PDF
"""

import markdown
import os
import sys
from pathlib import Path

def markdown_to_html(md_file_path, html_file_path, title="文档"):
    """
    将Markdown文件转换为HTML
    
    Args:
        md_file_path (str): Markdown文件路径
        html_file_path (str): 输出HTML文件路径
        title (str): HTML标题
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
                @media print {{
                    @page {{
                        size: A4;
                        margin: 2cm;
                    }}
                    
                    body {{
                        font-size: 12pt;
                        line-height: 1.4;
                    }}
                    
                    h1 {{
                        font-size: 18pt;
                        page-break-before: always;
                    }}
                    
                    h1:first-child {{
                        page-break-before: avoid;
                    }}
                    
                    h2 {{
                        font-size: 16pt;
                    }}
                    
                    h3 {{
                        font-size: 14pt;
                    }}
                    
                    table {{
                        font-size: 10pt;
                        page-break-inside: avoid;
                    }}
                    
                    pre, code {{
                        font-size: 9pt;
                    }}
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                }}
                
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 30px;
                    margin-bottom: 15px;
                    font-weight: 600;
                }}
                
                h1 {{
                    font-size: 28px;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                
                h2 {{
                    font-size: 24px;
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 8px;
                }}
                
                h3 {{
                    font-size: 20px;
                }}
                
                h4 {{
                    font-size: 18px;
                }}
                
                p {{
                    margin-bottom: 15px;
                    text-align: justify;
                }}
                
                ul, ol {{
                    margin-bottom: 15px;
                    padding-left: 30px;
                }}
                
                li {{
                    margin-bottom: 5px;
                }}
                
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 20px;
                    font-size: 14px;
                }}
                
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
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
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                    font-size: 13px;
                }}
                
                pre {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 5px;
                    padding: 15px;
                    overflow-x: auto;
                    margin-bottom: 20px;
                }}
                
                pre code {{
                    background-color: transparent;
                    padding: 0;
                }}
                
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin: 20px 0;
                    padding: 10px 20px;
                    background-color: #f8f9fa;
                    font-style: italic;
                }}
                
                .print-instructions {{
                    background-color: #e3f2fd;
                    border: 1px solid #2196f3;
                    border-radius: 5px;
                    padding: 15px;
                    margin-bottom: 20px;
                    font-size: 14px;
                }}
                
                .print-instructions h3 {{
                    margin-top: 0;
                    color: #1976d2;
                }}
                
                .print-instructions ul {{
                    margin-bottom: 0;
                }}
            </style>
        </head>
        <body>
            <div class="print-instructions">
                <h3>📄 打印为PDF说明</h3>
                <ul>
                    <li>按 <strong>Ctrl+P</strong> (Windows) 或 <strong>Cmd+P</strong> (Mac) 打开打印对话框</li>
                    <li>选择"另存为PDF"或"保存为PDF"</li>
                    <li>确保页面设置为A4纸张，边距为2cm</li>
                    <li>点击"保存"即可生成PDF文件</li>
                </ul>
            </div>
            
            {html}
        </body>
        </html>
        """
        
        # 写入HTML文件
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"✅ 成功转换: {md_file_path} -> {html_file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {md_file_path}")
        print(f"错误信息: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始转换Markdown文档为HTML...")
    
    # 获取当前目录
    current_dir = Path.cwd()
    
    # 定义要转换的文件
    documents = [
        {
            'md_file': '产品需求文档.md',
            'html_file': '产品需求文档.html',
            'title': '视频审核管理系统 - 产品需求文档'
        },
        {
            'md_file': '开发文档.md',
            'html_file': '开发文档.html',
            'title': '视频审核管理系统 - 开发文档'
        }
    ]
    
    success_count = 0
    total_count = len(documents)
    
    for doc in documents:
        md_path = current_dir / doc['md_file']
        html_path = current_dir / doc['html_file']
        
        if md_path.exists():
            if markdown_to_html(str(md_path), str(html_path), doc['title']):
                success_count += 1
        else:
            print(f"⚠️  文件不存在: {md_path}")
    
    print(f"\n📊 转换完成: {success_count}/{total_count} 个文档成功转换")
    
    if success_count > 0:
        print("\n📁 生成的HTML文件:")
        for doc in documents:
            html_path = current_dir / doc['html_file']
            if html_path.exists():
                file_size = html_path.stat().st_size / 1024  # KB
                print(f"   - {doc['html_file']} ({file_size:.1f} KB)")
        
        print("\n🖨️  打印为PDF:")
        print("   1. 用浏览器打开生成的HTML文件")
        print("   2. 按 Ctrl+P (Windows) 或 Cmd+P (Mac)")
        print("   3. 选择'另存为PDF'")
        print("   4. 设置页面为A4，边距2cm")
        print("   5. 点击保存")
    
    print("\n✨ 转换完成！")

if __name__ == "__main__":
    main()
