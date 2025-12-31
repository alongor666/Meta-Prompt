#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPTX转PDF转换器
将PowerPoint文件转换为PDF格式
"""

import os
import sys
import subprocess
from pathlib import Path

def convert_pptx_to_pdf_with_libreoffice(pptx_path, output_dir=None):
    """
    使用LibreOffice将PPTX文件转换为PDF
    
    Args:
        pptx_path: PPTX文件路径
        output_dir: 输出目录，默认为原文件所在目录
    
    Returns:
        PDF文件路径，转换失败返回None
    """
    # 检查文件是否存在
    if not os.path.exists(pptx_path):
        print(f"错误: 文件不存在 - {pptx_path}")
        return None
    
    # 设置输出目录
    if output_dir is None:
        output_dir = os.path.dirname(pptx_path)
    
    # 获取文件名（不含扩展名）
    file_name = Path(pptx_path).stem
    
    try:
        # 使用LibreOffice命令行工具转换
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            pptx_path
        ]
        
        print(f"正在转换: {pptx_path}")
        print(f"输出目录: {output_dir}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            pdf_path = os.path.join(output_dir, f"{file_name}.pdf")
            if os.path.exists(pdf_path):
                print(f"转换成功: {pdf_path}")
                return pdf_path
            else:
                print("转换完成但未找到PDF文件")
                return None
        else:
            print(f"转换失败: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("转换超时")
        return None
    except FileNotFoundError:
        print("错误: 未找到LibreOffice (soffice)")
        print("请确保已安装LibreOffice")
        return None
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")
        return None

def main():
    """主函数"""
    # 设置文件路径
    pptx_file = "/Users/xuechenglong/Downloads/01-公司开发项目/Meta-prompt/新能源网约车定价模型/网约车保险风险解决方案介绍2025年12月.pptx"
    
    # 检查文件是否存在
    if not os.path.exists(pptx_file):
        print(f"错误: 源文件不存在 - {pptx_file}")
        return 1
    
    # 执行转换
    pdf_path = convert_pptx_to_pdf_with_libreoffice(pptx_file)
    
    if pdf_path:
        print(f"✅ 转换成功！PDF文件保存在: {pdf_path}")
        return 0
    else:
        print("❌ 转换失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())