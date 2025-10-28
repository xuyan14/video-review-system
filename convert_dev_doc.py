#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的Markdown转PDF工具
专门处理开发文档的转换
"""

import markdown
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import sys
from pathlib import Path

def register_chinese_fonts():
    """注册中文字体"""
    try:
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/Helvetica.ttc',
            '/Library/Fonts/Arial Unicode MS.ttf'
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    return 'ChineseFont'
                except:
                    continue
        
        return 'Helvetica'
    except:
        return 'Helvetica'

def clean_markdown_content(content):
    """清理Markdown内容，移除HTML代码块"""
    # 移除HTML代码块
    content = re.sub(r'```html.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    # 移除HTML标签
    content = re.sub(r'<[^>]+>', '', content)
    
    return content

def markdown_to_pdf_simple(md_file_path, pdf_file_path, title="文档"):
    """
    将Markdown文件转换为PDF（简化版本）
    """
    try:
        # 注册中文字体
        font_name = register_chinese_fonts()
        
        # 读取Markdown文件
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 清理内容
        md_content = clean_markdown_content(md_content)
        
        # 创建PDF文档
        doc = SimpleDocTemplate(pdf_file_path, pagesize=A4,
                              rightMargin=2*cm, leftMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        # 获取样式
        styles = getSampleStyleSheet()
        
        # 创建自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=font_name,
            fontSize=18,
            spaceAfter=20,
            textColor=colors.HexColor('#2c3e50')
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontName=font_name,
            fontSize=16,
            spaceAfter=15,
            textColor=colors.HexColor('#2c3e50')
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontName=font_name,
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#2c3e50')
        )
        
        heading3_style = ParagraphStyle(
            'CustomHeading3',
            parent=styles['Heading3'],
            fontName=font_name,
            fontSize=12,
            spaceAfter=10,
            textColor=colors.HexColor('#2c3e50')
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=11,
            spaceAfter=8,
            textColor=colors.black
        )
        
        code_style = ParagraphStyle(
            'CodeStyle',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=9,
            spaceAfter=8,
            textColor=colors.black,
            leftIndent=20,
            rightIndent=20,
            backColor=colors.HexColor('#f8f9fa')
        )
        
        # 解析Markdown内容
        story = []
        
        # 添加标题
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 20))
        
        # 按行处理内容
        lines = md_content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                story.append(Spacer(1, 6))
                i += 1
                continue
            
            # 处理标题
            if line.startswith('# '):
                text = line[2:].strip()
                story.append(Paragraph(text, heading1_style))
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, heading2_style))
            elif line.startswith('### '):
                text = line[4:].strip()
                story.append(Paragraph(text, heading3_style))
            elif line.startswith('#### '):
                text = line[5:].strip()
                story.append(Paragraph(text, heading3_style))
            
            # 处理列表
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                story.append(Paragraph(f"• {text}", normal_style))
            
            # 处理代码块
            elif line.startswith('```'):
                # 收集代码内容
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                if code_lines:
                    code_text = '\n'.join(code_lines)
                    story.append(Paragraph(code_text, code_style))
            
            # 处理表格
            elif '|' in line and not line.startswith('|'):
                # 收集表格行
                table_data = []
                while i < len(lines) and '|' in lines[i]:
                    row = [cell.strip() for cell in lines[i].split('|') if cell.strip()]
                    if row:  # 跳过空行
                        table_data.append(row)
                    i += 1
                
                if table_data:
                    # 创建表格
                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), font_name),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(table)
                continue
            
            # 处理普通段落
            else:
                # 简单的Markdown格式化
                text = line
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # 粗体
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # 斜体
                
                if text.strip():
                    story.append(Paragraph(text, normal_style))
            
            i += 1
        
        # 构建PDF
        doc.build(story)
        
        print(f"✅ 成功转换: {md_file_path} -> {pdf_file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {md_file_path}")
        print(f"错误信息: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始转换开发文档为PDF...")
    
    # 获取当前目录
    current_dir = Path.cwd()
    
    # 转换开发文档
    md_path = current_dir / '开发文档.md'
    pdf_path = current_dir / '开发文档.pdf'
    
    if md_path.exists():
        if markdown_to_pdf_simple(str(md_path), str(pdf_path), '视频审核管理系统 - 开发文档'):
            print(f"\n📁 生成的PDF文件:")
            if pdf_path.exists():
                file_size = pdf_path.stat().st_size / 1024  # KB
                print(f"   - 开发文档.pdf ({file_size:.1f} KB)")
        print("\n✨ 转换完成！")
    else:
        print(f"⚠️  文件不存在: {md_path}")

if __name__ == "__main__":
    main()
