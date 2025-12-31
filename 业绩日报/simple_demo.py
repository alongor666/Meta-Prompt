#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版保险业务分析演示
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_demo_analysis():
    """创建演示分析结果"""
    
    # 创建目录
    os.makedirs("业绩日报/data", exist_ok=True)
    os.makedirs("业绩日报/charts", exist_ok=True) 
    os.makedirs("业绩日报/templates", exist_ok=True)
    
    # 生成示例数据摘要
    demo_results = {
        'A_签单保费总额': {
            'total_premium': 4250000,
            'avg_daily_premium': 850000,
            'max_daily_premium': 1200000,
            'total_orders': 2094
        },
        'B_业绩统计': {
            'top_salesperson': '张三',
            'top_branch': '北京分部',
            'performance_summary': 'TOP 3 业务员贡献35%'
        },
        'C_产品组合': {
            'cross_sell_rate': 28.5,
            'top_insurance': '商业险',
            'product_diversity': '产品组合均衡'
        },
        'D_客户细分': {
            'renewal_rate': 65.2,
            'new_car_ratio': 42.3,
            'customer_type': '个人客户占78%'
        },
        'E_渠道来源': {
            'top_channel': '移动展业(App)',
            'channel_diversity': 5,
            'digital_ratio': '线上渠道占62%'
        },
        'F_保费趋势': {
            'trend_direction': '上升',
            'weekly_growth': 12.8,
            'stability': '增长稳定'
        },
        'G_特殊业务': {
            'new_energy_rate': 15.6,
            'transfer_rate': 8.2,
            'opportunity': '新能源车潜力大'
        }
    }
    
    # 生成HTML报告
    html_content = generate_html_report(demo_results)
    
    with open("业绩日报/templates/daily_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("🚗 保险业务业绩分析演示报告已生成！")
    print("📊 报告位置: 业绩日报/templates/daily_report.html")
    print("📈 A-G七个维度分析完成")
    
    return demo_results

def generate_html_report(results):
    """生成HTML报告"""
    
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>保险业务业绩分析报告</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6; 
                color: #1d1d1f; 
                background: linear-gradient(135deg, #f5f5f7 0%, #e8e8ed 100%);
                min-height: 100vh;
            }}
            .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
            .header {{ 
                background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
                color: white; 
                padding: 40px; 
                border-radius: 16px; 
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 8px 32px rgba(0,122,255,0.15);
            }}
            .header h1 {{ font-size: 2.5em; margin-bottom: 10px; font-weight: 700; }}
            .header p {{ font-size: 1.2em; opacity: 0.9; }}
            .dashboard {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); 
                gap: 25px; 
                margin-bottom: 40px;
            }}
            .card {{ 
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 16px; 
                padding: 30px; 
                box-shadow: 0 8px 32px rgba(0,0,0,0.08);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid rgba(255,255,255,0.2);
            }}
            .card:hover {{ 
                transform: translateY(-8px) scale(1.02); 
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
            }}
            .card h3 {{ 
                color: #007AFF; 
                margin-bottom: 20px; 
                font-size: 1.4em;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .card-icon {{ font-size: 1.2em; }}
            .metric {{ 
                display: flex; 
                justify-content: space-between; 
                margin: 15px 0;
                padding: 12px 0;
                border-bottom: 1px solid rgba(0,0,0,0.05);
            }}
            .metric-label {{ color: #8e8e93; font-weight: 500; font-size: 0.95em; }}
            .metric-value {{ color: #1d1d1f; font-weight: 700; font-size: 1.1em; }}
            .highlight {{ 
                background: linear-gradient(135deg, rgba(0,122,255,0.1) 0%, rgba(88,86,214,0.1) 100%);
                padding: 20px; 
                border-radius: 12px; 
                margin: 20px 0;
                border-left: 4px solid #007AFF;
            }}
            .highlight strong {{ color: #007AFF; }}
            .footer {{ 
                text-align: center; 
                color: #8e8e93; 
                margin-top: 50px; 
                padding: 30px;
                background: rgba(255,255,255,0.5);
                border-radius: 16px;
            }}
            .status-good {{ color: #34C759; }}
            .status-warning {{ color: #FF9500; }}
            .status-info {{ color: #007AFF; }}
            
            @media (max-width: 768px) {{
                .dashboard {{ grid-template-columns: 1fr; }}
                .container {{ padding: 15px; }}
                .header {{ padding: 25px; }}
                .header h1 {{ font-size: 2em; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚗 保险业务业绩分析报告</h1>
                <p>数据驱动决策 · AI智能分析 · 苹果风格设计</p>
                <p>生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            </div>
            
            <div class="dashboard">
    """
    
    # A维度：签单保费总额
    if 'A_签单保费总额' in results:
        a_data = results['A_签单保费总额']
        html += f"""
                <div class="card">
                    <h3><span class="card-icon">💰</span> A. 签单保费总额</h3>
                    <div class="metric">
                        <span class="metric-label">总保费</span>
                        <span class="metric-value">¥{a_data['total_premium']:,}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">日均保费</span>
                        <span class="metric-value">¥{a_data['avg_daily_premium']:,}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">单日最高</span>
                        <span class="metric-value">¥{a_data['max_daily_premium']:,}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">总签单数</span>
                        <span class="metric-value">{a_data['total_orders']:,}笔</span>
                    </div>
                    <div class="highlight">
                        <strong>💡 关键洞察：</strong>保费规模健康，日均表现良好
                    </div>
                </div>
        """
    
    # B维度：业绩统计
    if 'B_业绩统计' in results:
        b_data = results['B_业绩统计']
        html += f"""
                <div class="card">
                    <h3><span class="card-icon">🏆</span> B. 业绩统计分析</h3>
                    <div class="metric">
                        <span class="metric-label">最佳业务员</span>
                        <span class="metric-value status-good">{b_data['top_salesperson']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">最佳机构</span>
                        <span class="metric-value status-info">{b_data['top_branch']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">业绩集中度</span>
                        <span class="metric-value">{b_data['performance_summary']}</span>
                    </div>
                    <div class="highlight">
                        <strong>🎯 管理建议：</strong>分享成功经验，提升团队整体水平
                    </div>
                </div>
        """
    
    # C维度：产品组合
    if 'C_产品组合' in results:
        c_data = results['C_产品组合']
        html += f"""
                <div class="card">
                    <h3><span class="card-icon">📊</span> C. 产品组合分析</h3>
                    <div class="metric">
                        <span class="metric-label">交叉销售率</span>
                        <span class="metric-value status-good">{c_data['cross_sell_rate']}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">主要险种</span>
                        <span class="metric-value">{c_data['top_insurance']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">产品状况</span>
                        <span class="metric-value">{c_data['product_diversity']}</span>
                    </div>
                    <div class="highlight">
                        <strong>📈 优化方向：</strong>进一步提升交叉销售，增加客户价值
                    </div>
                </div>
        """
    
    # D维度：客户细分
    if 'D_客户细分' in results:
        d_data = results['D_客户细分']
        html += f"""
                <div class="card">
                    <h3><span class="card-icon">👥</span> D. 客户细分分析</h3>
                    <div class="metric">
                        <span class="metric-label">续保率</span>
                        <span class="metric-value status-warning">{d_data['renewal_rate']}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">新车占比</span>
                        <span class="metric-value status-info">{d_data['new_car_ratio']}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">客户结构</span>
                        <span class="metric-value">{d_data['customer_type']}</span>
                    </div>
                    <div class="highlight">
                        <strong>🔁 客户策略：</strong>重点提升续保率，维护老客户价值
                    </div>
                </div>
        """
    
    # E维度：渠道来源
    if 'E_渠道来源' in results:
        e_data = results['E_渠道来源']
        html += f"""
                <div class="card">
                    <h3><span class="card-icon">📱</span> E. 渠道来源分析</h3>
                    <div class="metric">
                        <span class="metric-label">最佳渠道</span>
                        <span class="metric-value status-good">{e_data['top_channel']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">渠道多样性</span>
                        <span class="metric-value">{e_data['channel_diversity']}个渠道</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">数字化程度</span>
                        <span class="metric-value status-info">{e_data['digital_ratio']}</span>
                    </div>
                    <div class="highlight">
                        <strong>🚀 渠道策略：</strong>强化高效渠道，拓展新兴渠道
                    </div>
                </div>
        """
    
    # F维度：保费趋势
    if 'F_保费趋势' in results:
        f_data = results['F_保费趋势']
        html += f"""
                <div class="card">
                    <h3><span class="card-icon">📈</span> F. 保费趋势分析</h3>
                    <div class="metric">
                        <span class="metric-label">趋势方向</span>
                        <span class="metric-value status-good">{f_data['trend_direction']}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">周增长率</span>
                        <span class="metric-value status-good">+{f_data['weekly_growth']}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">稳定性</span>
                        <span class="metric-value status-info">{f_data['stability']}</span>
                    </div>
                    <div class="highlight">
                        <strong>📊 趋势洞察：</strong>增长态势良好，建议保持当前策略
                    </div>
                </div>
        """
    
    # G维度：特殊业务
    if 'G_特殊业务' in results:
        g_data = results['G_特殊业务']
        html += f"""
                <div class="card">
                    <h3><span class="card-icon">⚡</span> G. 特殊业务分析</h3>
                    <div class="metric">
                        <span class="metric-label">新能源车占比</span>
                        <span class="metric-value status-warning">{g_data['new_energy_rate']}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">过户车占比</span>
                        <span class="metric-value status-info">{g_data['transfer_rate']}%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">市场机会</span>
                        <span class="metric-value status-good">{g_data['opportunity']}</span>
                    </div>
                    <div class="highlight">
                        <strong>🚗 市场策略：</strong>新能源车是未来增长重点
                    </div>
                </div>
        """
    
    html += """
            </div>
            
            <div class="footer">
                <p>📊 本报告由AI保险业务分析系统自动生成</p>
                <p>💡 建议定期更新数据，持续跟踪业绩变化</p>
                <p>🎨 采用苹果风格设计，提供最佳用户体验</p>
                <p>⚡ 支持A-G七个维度的深度业务分析</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def main():
    """主演示函数"""
    print("🚗 保险业务业绩分析系统 - 演示版")
    print("=" * 60)
    
    # 创建演示分析
    results = create_demo_analysis()
    
    # 输出关键指标
    print("\n" + "=" * 60)
    print("📊 A-G七个维度核心业绩指标")
    print("=" * 60)
    
    print(f"💰 A. 签单保费总额: ¥{results['A_签单保费总额']['total_premium']:,}")
    print(f"🏆 B. 最佳业务员: {results['B_业绩统计']['top_salesperson']}")
    print(f"📊 C. 交叉销售率: {results['C_产品组合']['cross_sell_rate']}%")
    print(f"👥 D. 续保率: {results['D_客户细分']['renewal_rate']}%")
    print(f"📱 E. 最佳渠道: {results['E_渠道来源']['top_channel']}")
    print(f"📈 F. 趋势方向: {results['F_保费趋势']['trend_direction']}")
    print(f"⚡ G. 新能源车占比: {results['G_特殊业务']['new_energy_rate']}%")
    
    print("\n✅ 分析完成！")
    print("📊 查看详细报告: 业绩日报/templates/daily_report.html")
    print("🎨 苹果风格界面，A-G七个维度全面分析")
    
    return results

if __name__ == "__main__":
    main()