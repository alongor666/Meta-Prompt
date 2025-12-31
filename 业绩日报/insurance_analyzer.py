#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保险业务业绩分析系统
功能：涵盖A-G七个维度的深度数据分析与可视化
作者：AI助手
版本：1.0.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os
from typing import Dict, List, Tuple, Any

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class InsuranceAnalyzer:
    """保险业务数据分析器"""
    
    def __init__(self, data_path: str = None):
        """
        初始化分析器
        Args:
            data_path: 数据文件路径
        """
        self.data = None
        self.analysis_results = {}
        self.charts_dir = "业绩日报/charts"
        self.data_dir = "业绩日报/data"
        
        # 创建必要目录
        os.makedirs(self.charts_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs("业绩日报/templates", exist_ok=True)
        
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, file_path: str) -> bool:
        """
        加载Excel数据文件
        Args:
            file_path: Excel文件路径
        Returns:
            bool: 加载是否成功
        """
        try:
            self.data = pd.read_excel(file_path)
            print(f"✅ 数据加载成功，共{len(self.data)}条记录")
            return True
        except Exception as e:
            print(f"❌ 数据加载失败: {e}")
            return False
    
    def create_sample_data(self) -> None:
        """
        创建示例数据用于演示
        包含A-G七个维度所需的字段
        """
        np.random.seed(42)
        n_records = 500
        
        # 生成日期范围（最近30天）
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=30),
            end=datetime.now(),
            periods=n_records
        )
        
        # 业务员列表
        salespersons = ['张三', '李四', '王五', '赵六', '陈七', '刘八', '周九', '吴十']
        branches = ['总部', '北京分部', '上海分部', '广州分部', '深圳分部']
        
        # 生成示例数据
        sample_data = {
            '日期': dates,
            '业务员': np.random.choice(salespersons, n_records),
            '三级机构': np.random.choice(branches, n_records),
            '签单保费': np.random.uniform(1000, 50000, n_records).round(2),
            '险别': np.random.choice(['交强险', '商业险', '综合险', '三者险', '车损险'], n_records),
            '交叉销售': np.random.choice(['是', '否'], n_records, p=[0.3, 0.7]),
            '客户类别': np.random.choice(['个人', '企业', '团体'], n_records, p=[0.7, 0.2, 0.1]),
            '车辆类型': np.random.choice(['新车', '旧车'], n_records, p=[0.4, 0.6]),
            '是否续保': np.random.choice(['是', '否'], n_records, p=[0.6, 0.4]),
            '终端来源': np.random.choice(['官网', 'APP', '代理人', '合作渠道', '电话营销'], n_records),
            '是否新能源': np.random.choice(['是', '否'], n_records, p=[0.2, 0.8]),
            '是否过户车': np.random.choice(['是', '否'], n_records, p=[0.15, 0.85])
        }
        
        self.data = pd.DataFrame(sample_data)
        
        # 保存示例数据
        sample_file = os.path.join(self.data_dir, "sample_data.xlsx")
        self.data.to_excel(sample_file, index=False)
        print(f"📊 示例数据已创建: {sample_file}")
        
        return sample_file
    
    def analyze_a_premium_total(self) -> Dict[str, Any]:
        """
        A维度分析：签单保费总额统计
        """
        if self.data is None:
            return {}
        
        # 按日期汇总保费
        daily_premium = self.data.groupby('日期')['签单保费'].agg(['sum', 'count']).reset_index()
        daily_premium.columns = ['日期', '总保费', '签单数']
        
        # 计算同比增长（如果有足够数据）
        daily_premium['日期'] = pd.to_datetime(daily_premium['日期'])
        daily_premium = daily_premium.sort_values('日期')
        
        # 计算移动平均
        daily_premium['7天均线'] = daily_premium['总保费'].rolling(window=7, min_periods=1).mean()
        
        # 统计信息
        total_premium = daily_premium['总保费'].sum()
        avg_daily_premium = daily_premium['总保费'].mean()
        max_daily_premium = daily_premium['总保费'].max()
        
        analysis = {
            'daily_data': daily_premium,
            'total_premium': total_premium,
            'avg_daily_premium': avg_daily_premium,
            'max_daily_premium': max_daily_premium,
            'total_orders': len(self.data)
        }
        
        # 创建趋势图
        self._create_premium_trend_chart(daily_premium)
        
        return analysis
    
    def analyze_b_performance(self) -> Dict[str, Any]:
        """
        B维度分析：业务员业绩和三级机构业绩
        """
        if self.data is None:
            return {}
        
        # 业务员业绩分析
        salesperson_performance = self.data.groupby('业务员').agg({
            '签单保费': ['sum', 'count', 'mean'],
            '日期': 'max'
        }).round(2)
        salesperson_performance.columns = ['总保费', '签单数', '平均保费', '最后活动日']
        salesperson_performance = salesperson_performance.sort_values('总保费', ascending=False)
        
        # 三级机构业绩分析
        branch_performance = self.data.groupby('三级机构').agg({
            '签单保费': ['sum', 'count', 'mean'],
            '业务员': 'nunique'
        }).round(2)
        branch_performance.columns = ['总保费', '签单数', '平均保费', '业务员数量']
        branch_performance = branch_performance.sort_values('总保费', ascending=False)
        
        analysis = {
            'salesperson_performance': salesperson_performance,
            'branch_performance': branch_performance,
            'top_salesperson': salesperson_performance.index[0],
            'top_branch': branch_performance.index[0]
        }
        
        # 创建业绩对比图
        self._create_performance_charts(salesperson_performance, branch_performance)
        
        return analysis
    
    def analyze_c_product_mix(self) -> Dict[str, Any]:
        """
        C维度分析：险别组合和交叉销售效果
        """
        if self.data is None:
            return {}
        
        # 险别组合分析
        insurance_type_stats = self.data.groupby('险别').agg({
            '签单保费': ['sum', 'count', 'mean'],
            '交叉销售': lambda x: (x == '是').sum()
        }).round(2)
        insurance_type_stats.columns = ['总保费', '签单数', '平均保费', '交叉销售数']
        insurance_type_stats['交叉销售率'] = (
            insurance_type_stats['交叉销售数'] / insurance_type_stats['签单数'] * 100
        ).round(2)
        
        # 交叉销售效果分析
        cross_sell_analysis = self.data.groupby('交叉销售').agg({
            '签单保费': ['sum', 'count', 'mean']
        }).round(2)
        cross_sell_analysis.columns = ['总保费', '签单数', '平均保费']
        
        analysis = {
            'insurance_type_stats': insurance_type_stats,
            'cross_sell_analysis': cross_sell_analysis,
            'cross_sell_rate': (self.data['交叉销售'] == '是').sum() / len(self.data) * 100
        }
        
        # 创建产品组合图
        self._create_product_mix_charts(insurance_type_stats, cross_sell_analysis)
        
        return analysis
    
    def analyze_d_customer_segments(self) -> Dict[str, Any]:
        """
        D维度分析：客户类别、新旧车、续保分析
        """
        if self.data is None:
            return {}
        
        # 客户类别分析
        customer_type_stats = self.data.groupby('客户类别').agg({
            '签单保费': ['sum', 'count', 'mean']
        }).round(2)
        customer_type_stats.columns = ['总保费', '客户数', '平均保费']
        
        # 新旧车分析
        vehicle_type_stats = self.data.groupby('车辆类型').agg({
            '签单保费': ['sum', 'count', 'mean']
        }).round(2)
        vehicle_type_stats.columns = ['总保费', '车数', '平均保费']
        
        # 续保分析
        renewal_stats = self.data.groupby('是否续保').agg({
            '签单保费': ['sum', 'count', 'mean']
        }).round(2)
        renewal_stats.columns = ['总保费', '单数', '平均保费']
        renewal_rate = (self.data['是否续保'] == '是').sum() / len(self.data) * 100
        
        analysis = {
            'customer_type_stats': customer_type_stats,
            'vehicle_type_stats': vehicle_type_stats,
            'renewal_stats': renewal_stats,
            'renewal_rate': renewal_rate
        }
        
        # 创建客户细分图
        self._create_customer_segment_charts(customer_type_stats, vehicle_type_stats, renewal_stats)
        
        return analysis
    
    def analyze_e_channel_sources(self) -> Dict[str, Any]:
        """
        E维度分析：终端来源统计
        """
        if self.data is None:
            return {}
        
        # 渠道来源分析
        channel_stats = self.data.groupby('终端来源').agg({
            '签单保费': ['sum', 'count', 'mean'],
            '业务员': 'nunique'
        }).round(2)
        channel_stats.columns = ['总保费', '单数', '平均保费', '业务员数']
        channel_stats = channel_stats.sort_values('总保费', ascending=False)
        
        # 计算转化率（基于总单数）
        total_orders = len(self.data)
        channel_stats['转化率'] = (channel_stats['单数'] / total_orders * 100).round(2)
        
        analysis = {
            'channel_stats': channel_stats,
            'top_channel': channel_stats.index[0],
            'channel_diversity': len(channel_stats)
        }
        
        # 创建渠道分析图
        self._create_channel_charts(channel_stats)
        
        return analysis
    
    def analyze_f_premium_trends(self) -> Dict[str, Any]:
        """
        F维度分析：签单保费趋势
        """
        if self.data is None:
            return {}
        
        # 确保日期格式正确
        self.data['日期'] = pd.to_datetime(self.data['日期'])
        
        # 按周和月汇总
        self.data['周'] = self.data['日期'].dt.isocalendar().week
        self.data['月'] = self.data['日期'].dt.month
        
        # 周趋势
        weekly_trend = self.data.groupby('周')['签单保费'].agg(['sum', 'count']).reset_index()
        weekly_trend.columns = ['周次', '周保费', '周单数']
        
        # 月趋势
        monthly_trend = self.data.groupby('月')['签单保费'].agg(['sum', 'count']).reset_index()
        monthly_trend.columns = ['月份', '月保费', '月单数']
        
        # 计算增长率
        weekly_trend['周增长率'] = weekly_trend['周保费'].pct_change().fillna(0) * 100
        monthly_trend['月增长率'] = monthly_trend['月保费'].pct_change().fillna(0) * 100
        
        analysis = {
            'weekly_trend': weekly_trend,
            'monthly_trend': monthly_trend,
            'trend_direction': '上升' if weekly_trend['周增长率'].mean() > 0 else '下降'
        }
        
        # 创建趋势分析图
        self._create_trend_analysis_charts(weekly_trend, monthly_trend)
        
        return analysis
    
    def analyze_g_special_business(self) -> Dict[str, Any]:
        """
        G维度分析：新能源车、过户车业务
        """
        if self.data is None:
            return {}
        
        # 新能源车分析
        new_energy_stats = self.data.groupby('是否新能源').agg({
            '签单保费': ['sum', 'count', 'mean']
        }).round(2)
        new_energy_stats.columns = ['总保费', '单数', '平均保费']
        
        # 过户车分析
        transfer_stats = self.data.groupby('是否过户车').agg({
            '签单保费': ['sum', 'count', 'mean']
        }).round(2)
        transfer_stats.columns = ['总保费', '单数', '平均保费']
        
        # 计算占比
        new_energy_rate = (self.data['是否新能源'] == '是').sum() / len(self.data) * 100
        transfer_rate = (self.data['是否过户车'] == '是').sum() / len(self.data) * 100
        
        analysis = {
            'new_energy_stats': new_energy_stats,
            'transfer_stats': transfer_stats,
            'new_energy_rate': new_energy_rate,
            'transfer_rate': transfer_rate
        }
        
        # 创建特殊业务分析图
        self._create_special_business_charts(new_energy_stats, transfer_stats)
        
        return analysis
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        运行完整的A-G七个维度分析
        """
        print("🚀 开始运行完整业绩分析...")
        
        results = {
            'A_签单保费总额': self.analyze_a_premium_total(),
            'B_业绩统计': self.analyze_b_performance(),
            'C_产品组合': self.analyze_c_product_mix(),
            'D_客户细分': self.analyze_d_customer_segments(),
            'E_渠道来源': self.analyze_e_channel_sources(),
            'F_保费趋势': self.analyze_f_premium_trends(),
            'G_特殊业务': self.analyze_g_special_business()
        }
        
        self.analysis_results = results
        
        # 生成HTML报告
        self._generate_html_report(results)
        
        print("✅ 分析完成！报告已生成。")
        return results
    
    def _create_premium_trend_chart(self, daily_data: pd.DataFrame) -> None:
        """创建保费趋势图"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_data['日期'],
            y=daily_data['总保费'],
            mode='lines+markers',
            name='每日保费',
            line=dict(color='#007AFF', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_data['日期'],
            y=daily_data['7天均线'],
            mode='lines',
            name='7天均线',
            line=dict(color='#34C759', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='签单保费趋势分析',
            xaxis_title='日期',
            yaxis_title='保费金额',
            template='plotly_white',
            font=dict(family="Arial, sans-serif")
        )
        
        fig.write_html(os.path.join(self.charts_dir, 'premium_trend.html'))
    
    def _create_performance_charts(self, salesperson_data: pd.DataFrame, branch_data: pd.DataFrame) -> None:
        """创建业绩对比图"""
        # 业务员业绩图
        fig1 = go.Figure(data=[
            go.Bar(x=salesperson_data.index, y=salesperson_data['总保费'])
        ])
        fig1.update_layout(title='业务员业绩排行', xaxis_title='业务员', yaxis_title='总保费')
        fig1.write_html(os.path.join(self.charts_dir, 'salesperson_performance.html'))
        
        # 机构业绩图
        fig2 = go.Figure(data=[
            go.Bar(x=branch_data.index, y=branch_data['总保费'])
        ])
        fig2.update_layout(title='三级机构业绩对比', xaxis_title='机构', yaxis_title='总保费')
        fig2.write_html(os.path.join(self.charts_dir, 'branch_performance.html'))
    
    def _create_product_mix_charts(self, insurance_data: pd.DataFrame, cross_sell_data: pd.DataFrame) -> None:
        """创建产品组合分析图"""
        # 险别分布饼图
        fig1 = go.Figure(data=[
            go.Pie(labels=insurance_data.index, values=insurance_data['总保费'])
        ])
        fig1.update_layout(title='险别保费分布')
        fig1.write_html(os.path.join(self.charts_dir, 'insurance_distribution.html'))
        
        # 交叉销售对比图
        fig2 = go.Figure(data=[
            go.Bar(x=cross_sell_data.index, y=cross_sell_data['总保费'])
        ])
        fig2.update_layout(title='交叉销售效果对比', xaxis_title='是否交叉销售', yaxis_title='总保费')
        fig2.write_html(os.path.join(self.charts_dir, 'cross_sell_comparison.html'))
    
    def _create_customer_segment_charts(self, customer_data: pd.DataFrame, vehicle_data: pd.DataFrame, renewal_data: pd.DataFrame) -> None:
        """创建客户细分分析图"""
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('客户类别', '车辆类型', '续保情况', '平均保费对比'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # 添加各种图表
        fig.add_trace(go.Bar(x=customer_data.index, y=customer_data['总保费'], name='客户类别'), row=1, col=1)
        fig.add_trace(go.Bar(x=vehicle_data.index, y=vehicle_data['总保费'], name='车辆类型'), row=1, col=2)
        fig.add_trace(go.Bar(x=renewal_data.index, y=renewal_data['总保费'], name='续保情况'), row=2, col=1)
        fig.add_trace(go.Bar(x=['个人', '企业', '团体'], y=customer_data['平均保费'], name='平均保费'), row=2, col=2)
        
        fig.update_layout(title_text="客户细分分析", showlegend=False)
        fig.write_html(os.path.join(self.charts_dir, 'customer_segments.html'))
    
    def _create_channel_charts(self, channel_data: pd.DataFrame) -> None:
        """创建渠道分析图"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('渠道保费分布', '渠道转化率'),
            specs=[[{"type": "bar"}, {"type": "bar"}]
        )
        )
        
        fig.add_trace(go.Bar(x=channel_data.index, y=channel_data['总保费'], name='总保费'), row=1, col=1)
        fig.add_trace(go.Bar(x=channel_data.index, y=channel_data['转化率'], name='转化率'), row=1, col=2)
        
        fig.update_layout(title_text="渠道来源分析")
        fig.write_html(os.path.join(self.charts_dir, 'channel_analysis.html'))
    
    def _create_trend_analysis_charts(self, weekly_data: pd.DataFrame, monthly_data: pd.DataFrame) -> None:
        """创建趋势分析图"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('周保费趋势', '周增长率', '月保费趋势', '月增长率'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(go.Scatter(x=weekly_data['周次'], y=weekly_data['周保费'], name='周保费'), row=1, col=1)
        fig.add_trace(go.Bar(x=weekly_data['周次'], y=weekly_data['周增长率'], name='周增长率'), row=1, col=2)
        fig.add_trace(go.Scatter(x=monthly_data['月份'], y=monthly_data['月保费'], name='月保费'), row=2, col=1)
        fig.add_trace(go.Bar(x=monthly_data['月份'], y=monthly_data['月增长率'], name='月增长率'), row=2, col=2)
        
        fig.update_layout(title_text="保费趋势深度分析")
        fig.write_html(os.path.join(self.charts_dir, 'trend_analysis.html'))
    
    def _create_special_business_charts(self, new_energy_data: pd.DataFrame, transfer_data: pd.DataFrame) -> None:
        """创建特殊业务分析图"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('新能源车业务', '过户车业务'),
            specs=[[{"type": "bar"}, {"type": "bar"}]
        )
        
        fig.add_trace(go.Bar(x=new_energy_data.index, y=new_energy_data['总保费'], name='新能源车'), row=1, col=1)
        fig.add_trace(go.Bar(x=transfer_data.index, y=transfer_data['总保费'], name='过户车'), row=1, col=2)
        
        fig.update_layout(title_text="特殊业务分析")
        fig.write_html(os.path.join(self.charts_dir, 'special_business.html'))
    
    def _generate_html_report(self, results: Dict[str, Any]) -> None:
        """生成HTML分析报告"""
        html_template = self._create_html_template(results)
        
        with open("业绩日报/templates/daily_report.html", 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print("📊 HTML报告已生成: 业绩日报/templates/daily_report.html")
    
    def _create_html_template(self, results: Dict[str, Any]) -> str:
        """创建HTML报告模板"""
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
                    background: #f5f5f7;
                }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .header {{ 
                    background: linear-gradient(135deg, #007AFF, #5856D6);
                    color: white; 
                    padding: 30px; 
                    border-radius: 12px; 
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .dashboard {{ 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
                    gap: 20px; 
                    margin-bottom: 30px;
                }}
                .card {{ 
                    background: white; 
                    border-radius: 12px; 
                    padding: 25px; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.07);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }}
                .card:hover {{ 
                    transform: translateY(-2px); 
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                }}
                .card h3 {{ 
                    color: #007AFF; 
                    margin-bottom: 15px; 
                    font-size: 1.3em;
                    border-bottom: 2px solid #f0f0f0;
                    padding-bottom: 10px;
                }}
                .metric {{ 
                    display: flex; 
                    justify-content: space-between; 
                    margin: 10px 0;
                    padding: 8px 0;
                    border-bottom: 1px solid #f5f5f5;
                }}
                .metric-label {{ color: #8e8e93; font-weight: 500; }}
                .metric-value {{ color: #1d1d1f; font-weight: 600; }}
                .highlight {{ background: #f0f9ff; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                .chart-links {{ margin-top: 20px; }}
                .chart-link {{ 
                    display: inline-block; 
                    background: #007AFF; 
                    color: white; 
                    padding: 8px 16px; 
                    text-decoration: none; 
                    border-radius: 6px; 
                    margin: 5px;
                    transition: background 0.2s ease;
                }}
                .chart-link:hover {{ background: #0056CC; }}
                .footer {{ 
                    text-align: center; 
                    color: #8e8e93; 
                    margin-top: 40px; 
                    padding: 20px;
                    border-top: 1px solid #e5e5e7;
                }}
                @media (max-width: 768px) {{
                    .dashboard {{ grid-template-columns: 1fr; }}
                    .container {{ padding: 10px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚗 保险业务业绩分析报告</h1>
                    <p>数据驱动决策，洞察引领增长 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="dashboard">
        """
        
        # A维度：签单保费总额
        if 'A_签单保费总额' in results and results['A_签单保费总额']:
            a_data = results['A_签单保费总额']
            html += f"""
                    <div class="card">
                        <h3>💰 A. 签单保费总额</h3>
                        <div class="metric">
                            <span class="metric-label">总保费</span>
                            <span class="metric-value">¥{a_data.get('total_premium', 0):,.2f}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">日均保费</span>
                            <span class="metric-value">¥{a_data.get('avg_daily_premium', 0):,.2f}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">单日最高</span>
                            <span class="metric-value">¥{a_data.get('max_daily_premium', 0):,.2f}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">总签单数</span>
                            <span class="metric-value">{a_data.get('total_orders', 0):,}</span>
                        </div>
                        <div class="highlight">
                            <strong>关键洞察：</strong>业务规模稳定，日均保费表现良好
                        </div>
                        <div class="chart-links">
                            <a href="../charts/premium_trend.html" class="chart-link">📈 查看趋势图</a>
                        </div>
                    </div>
            """
        
        # B维度：业绩统计
        if 'B_业绩统计' in results and results['B_业绩统计']:
            b_data = results['B_业绩统计']
            html += f"""
                    <div class="card">
                        <h3>🏆 B. 业绩统计分析</h3>
                        <div class="metric">
                            <span class="metric-label">最佳业务员</span>
                            <span class="metric-value">{b_data.get('top_salesperson', 'N/A')}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">最佳机构</span>
                            <span class="metric-value">{b_data.get('top_branch', 'N/A')}</span>
                        </div>
                        <div class="highlight">
                            <strong>管理建议：</strong>重点关注业绩突出人员，分享成功经验
                        </div>
                        <div class="chart-links">
                            <a href="../charts/salesperson_performance.html" class="chart-link">👥 业务员排行</a>
                            <a href="../charts/branch_performance.html" class="chart-link">🏢 机构对比</a>
                        </div>
                    </div>
            """
        
        # C维度：产品组合
        if 'C_产品组合' in results and results['C_产品组合']:
            c_data = results['C_产品组合']
            html += f"""
                    <div class="card">
                        <h3>📊 C. 产品组合分析</h3>
                        <div class="metric">
                            <span class="metric-label">交叉销售率</span>
                            <span class="metric-value">{c_data.get('cross_sell_rate', 0):.1f}%</span>
                        </div>
                        <div class="highlight">
                            <strong>优化方向：</strong>提升交叉销售，增加客户价值
                        </div>
                        <div class="chart-links">
                            <a href="../charts/insurance_distribution.html" class="chart-link">🥧 险别分布</a>
                            <a href="../charts/cross_sell_comparison.html" class="chart-link">🔄 交叉销售</a>
                        </div>
                    </div>
            """
        
        # D维度：客户细分
        if 'D_客户细分' in results and results['D_客户细分']:
            d_data = results['D_客户细分']
            html += f"""
                    <div class="card">
                        <h3>👥 D. 客户细分分析</h3>
                        <div class="metric">
                            <span class="metric-label">续保率</span>
                            <span class="metric-value">{d_data.get('renewal_rate', 0):.1f}%</span>
                        </div>
                        <div class="highlight">
                            <strong>客户策略：</strong>提升续保率，维护老客户价值
                        </div>
                        <div class="chart-links">
                            <a href="../charts/customer_segments.html" class="chart-link">🎯 客户画像</a>
                        </div>
                    </div>
            """
        
        # E维度：渠道来源
        if 'E_渠道来源' in results and results['E_渠道来源']:
            e_data = results['E_渠道来源']
            html += f"""
                    <div class="card">
                        <h3>📱 E. 渠道来源分析</h3>
                        <div class="metric">
                            <span class="metric-label">最佳渠道</span>
                            <span class="metric-value">{e_data.get('top_channel', 'N/A')}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">渠道多样性</span>
                            <span class="metric-value">{e_data.get('channel_diversity', 0)}个</span>
                        </div>
                        <div class="highlight">
                            <strong>渠道策略：</strong>优化高效渠道，拓展新兴渠道
                        </div>
                        <div class="chart-links">
                            <a href="../charts/channel_analysis.html" class="chart-link">📊 渠道效果</a>
                        </div>
                    </div>
            """
        
        # F维度：保费趋势
        if 'F_保费趋势' in results and results['F_保费趋势']:
            f_data = results['F_保费趋势']
            html += f"""
                    <div class="card">
                        <h3>📈 F. 保费趋势分析</h3>
                        <div class="metric">
                            <span class="metric-label">趋势方向</span>
                            <span class="metric-value">{f_data.get('trend_direction', 'N/A')}</span>
                        </div>
                        <div class="highlight">
                            <strong>趋势洞察：</strong>关注季节性波动，把握市场节奏
                        </div>
                        <div class="chart-links">
                            <a href="../charts/trend_analysis.html" class="chart-link">📊 趋势详情</a>
                        </div>
                    </div>
            """
        
        # G维度：特殊业务
        if 'G_特殊业务' in results and results['G_特殊业务']:
            g_data = results['G_特殊业务']
            html += f"""
                    <div class="card">
                        <h3>⚡ G. 特殊业务分析</h3>
                        <div class="metric">
                            <span class="metric-label">新能源车占比</span>
                            <span class="metric-value">{g_data.get('new_energy_rate', 0):.1f}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">过户车占比</span>
                            <span class="metric-value">{g_data.get('transfer_rate', 0):.1f}%</span>
                        </div>
                        <div class="highlight">
                            <strong>市场机会：</strong>新能源车市场潜力巨大
                        </div>
                        <div class="chart-links">
                            <a href="../charts/special_business.html" class="chart-link">🚗 特殊业务</a>
                        </div>
                    </div>
            """
        
        html += """
                </div>
                
                <div class="footer">
                    <p>📊 本报告由保险业务分析系统自动生成</p>
                    <p>💡 建议定期更新数据，持续跟踪业绩变化</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

def main():
    """主函数 - 演示系统功能"""
    print("🚗 保险业务业绩分析系统")
    print("=" * 50)
    
    # 创建分析器实例
    analyzer = InsuranceAnalyzer()
    
    # 创建示例数据（如果没有数据文件）
    sample_file = analyzer.create_sample_data()
    
    # 加载数据
    analyzer.load_data(sample_file)
    
    # 运行完整分析
    results = analyzer.run_complete_analysis()
    
    # 输出关键指标摘要
    print("\n" + "=" * 50)
    print("📊 关键业绩指标摘要")
    print("=" * 50)
    
    if 'A_签单保费总额' in results:
        a_data = results['A_签单保费总额']
        print(f"💰 总保费: ¥{a_data.get('total_premium', 0):,.2f}")
        print(f"📈 日均保费: ¥{a_data.get('avg_daily_premium', 0):,.2f}")
    
    if 'B_业绩统计' in results:
        b_data = results['B_业绩统计']
        print(f"🏆 最佳业务员: {b_data.get('top_salesperson', 'N/A')}")
        print(f"🏢 最佳机构: {b_data.get('top_branch', 'N/A')}")
    
    if 'C_产品组合' in results:
        c_data = results['C_产品组合']
        print(f"🔄 交叉销售率: {c_data.get('cross_sell_rate', 0):.1f}%")
    
    if 'D_客户细分' in results:
        d_data = results['D_客户细分']
        print(f"🔁 续保率: {d_data.get('renewal_rate', 0):.1f}%")
    
    print("\n✅ 分析完成！")
    print("📊 查看详细报告: 业绩日报/templates/daily_report.html")
    print("📈 查看图表: 业绩日报/charts/")

if __name__ == "__main__":
    main()