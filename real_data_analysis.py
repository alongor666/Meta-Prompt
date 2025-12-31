#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于真实数据的车险保批单业务分析脚本
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def load_real_data_analysis(file_path):
    """基于真实数据进行深度分析"""
    print("🔄 基于真实数据进行深度分析...")
    
    # 读取真实数据
    df = pd.read_excel(file_path)
    print(f"📊 真实数据加载完成，共 {len(df)} 条记录")
    
    # 基础统计
    total_policies = len(df)
    total_premium = df['签单保费'].sum()
    avg_premium = df['签单保费'].mean()
    
    # 业务员分析
    salespeople_count = df['业务员'].nunique()
    print(f"👥 真实活跃业务员：{salespeople_count} 人")
    
    # 时间分析 - 使用投保确认时间
    df['投保确认时间'] = pd.to_datetime(df['投保确认时间'])
    df['日期'] = df['投保确认时间'].dt.date
    
    # 机构分析
    org_count = df['三级机构'].nunique()
    print(f"🏢 三级机构数量：{org_count} 个")
    
    # 险种分析
    insurance_types = df['险种名称'].value_counts()
    print(f"🛡️  险种类型：{len(insurance_types)} 种")
    
    # 客户类别分析
    customer_types = df['客户类别'].value_counts()
    print(f"👤 客户类别：{len(customer_types)} 类")
    
    return {
        'total_policies': total_policies,
        'total_premium': total_premium,
        'avg_premium': avg_premium,
        'salespeople_count': salespeople_count,
        'org_count': org_count,
        'insurance_types': insurance_types,
        'customer_types': customer_types,
        'df': df
    }

def analyze_real_sales_performance(df):
    """分析真实业务员业绩"""
    print("\n👥 分析真实业务员业绩...")
    
    # 按业务员统计业绩
    sales_performance = df.groupby('业务员').agg({
        '保单号': 'count',
        '签单保费': 'sum'
    }).reset_index()
    sales_performance.columns = ['业务员', '保单笔数', '签单保费']
    sales_performance = sales_performance.sort_values('签单保费', ascending=False)
    
    # 计算占比
    total_premium = sales_performance['签单保费'].sum()
    sales_performance['占比'] = (sales_performance['签单保费'] / total_premium * 100).round(2)
    
    # 获取TOP 10（如果业务员少于10人，则显示全部）
    top_count = min(10, len(sales_performance))
    top_salespeople = sales_performance.head(top_count)
    
    print(f"📈 TOP {top_count} 业务员业绩：")
    for i, row in top_salespeople.iterrows():
        print(f"   {i+1}. {row['业务员']}: {row['保单笔数']}单, ¥{row['签单保费']:,.0f} ({row['占比']:.1f}%)")
    
    return top_salespeople, sales_performance

def analyze_real_organizations(df):
    """分析真实机构业绩"""
    print("\n🏢 分析真实机构业绩...")
    
    # 按三级机构统计
    org_performance = df.groupby('三级机构').agg({
        '保单号': 'count',
        '签单保费': 'sum'
    }).reset_index()
    org_performance.columns = ['三级机构', '保单笔数', '签单保费']
    org_performance = org_performance.sort_values('签单保费', ascending=False)
    
    # 计算占比
    total_premium = org_performance['签单保费'].sum()
    org_performance['占比'] = (org_performance['签单保费'] / total_premium * 100).round(2)
    
    print("📊 各机构业绩排名：")
    for i, row in org_performance.iterrows():
        print(f"   {row['三级机构']}: {row['保单笔数']}单, ¥{row['签单保费']:,.0f} ({row['占比']:.1f}%)")
    
    return org_performance

def analyze_real_insurance_products(df):
    """分析真实险种分布"""
    print("\n🛡️ 分析真实险种分布...")
    
    # 险种名称分布
    insurance_distribution = df.groupby('险种名称').agg({
        '保单号': 'count',
        '签单保费': 'sum'
    }).reset_index()
    insurance_distribution.columns = ['险种名称', '保单笔数', '签单保费']
    insurance_distribution = insurance_distribution.sort_values('签单保费', ascending=False)
    
    # 计算占比
    total_premium = insurance_distribution['签单保费'].sum()
    insurance_distribution['占比'] = (insurance_distribution['签单保费'] / total_premium * 100).round(2)
    
    print("📋 险种分布：")
    for i, row in insurance_distribution.iterrows():
        print(f"   {row['险种名称']}: {row['保单笔数']}单, ¥{row['签单保费']:,.0f} ({row['占比']:.1f}%)")
    
    # 险别组合分析
    if '险别组合' in df.columns:
        combo_distribution = df['险别组合'].value_counts().head(10)
        print("\n🔧 险别组合TOP 10：")
        for combo, count in combo_distribution.items():
            print(f"   {combo}: {count}单")
    
    return insurance_distribution

def analyze_real_customer_structure(df):
    """分析真实客户结构"""
    print("\n👥 分析真实客户结构...")
    
    # 客户类别分布
    customer_distribution = df.groupby('客户类别').agg({
        '保单号': 'count',
        '签单保费': 'sum'
    }).reset_index()
    customer_distribution.columns = ['客户类别', '保单笔数', '签单保费']
    customer_distribution = customer_distribution.sort_values('签单保费', ascending=False)
    
    # 计算占比
    total_policies = customer_distribution['保单笔数'].sum()
    total_premium = customer_distribution['签单保费'].sum()
    customer_distribution['笔数占比'] = (customer_distribution['保单笔数'] / total_policies * 100).round(2)
    customer_distribution['保费占比'] = (customer_distribution['签单保费'] / total_premium * 100).round(2)
    
    print("👤 客户类别分布：")
    for i, row in customer_distribution.iterrows():
        print(f"   {row['客户类别']}: {row['保单笔数']}单 ({row['笔数占比']:.1f}%), ¥{row['签单保费']:,.0f} ({row['保费占比']:.1f}%)")
    
    # 新旧车分析
    if '新旧车标志' in df.columns:
        new_old_analysis = df.groupby('新旧车标志').agg({
            '保单号': 'count',
            '签单保费': ['sum', 'mean']
        }).reset_index()
        new_old_analysis.columns = ['新旧车标志', '保单笔数', '总签单保费', '平均保费']
        
        print("\n🚗 新旧车分布：")
        for i, row in new_old_analysis.iterrows():
            print(f"   {row['新旧车标志']}: {row['保单笔数']}单, 平均保费¥{row['平均保费']:.0f}")
    
    # 续保分析
    if '是否续保' in df.columns:
        renewal_analysis = df.groupby('是否续保').agg({
            '保单号': 'count',
            '签单保费': 'sum'
        }).reset_index()
        renewal_analysis.columns = ['是否续保', '保单笔数', '签单保费']
        
        print("\n🔄 续保分析：")
        for i, row in renewal_analysis.iterrows():
            print(f"   {row['是否续保']}: {row['保单笔数']}单, ¥{row['签单保费']:,.0f}")
    
    return customer_distribution

def analyze_real_channels(df):
    """分析真实渠道分布"""
    print("\n🌐 分析真实渠道分布...")
    
    # 业务来源分析
    if '业务来源' in df.columns:
        source_distribution = df.groupby('业务来源').agg({
            '保单号': 'count',
            '签单保费': 'sum'
        }).reset_index()
        source_distribution.columns = ['业务来源', '保单笔数', '签单保费']
        source_distribution = source_distribution.sort_values('签单保费', ascending=False)
        
        # 计算占比和平均保费
        total_policies = source_distribution['保单笔数'].sum()
        source_distribution['笔数占比'] = (source_distribution['保单笔数'] / total_policies * 100).round(2)
        source_distribution['平均保费'] = (source_distribution['签单保费'] / source_distribution['保单笔数']).round(0)
        
        print("📊 业务来源分布：")
        for i, row in source_distribution.iterrows():
            print(f"   {row['业务来源']}: {row['保单笔数']}单 ({row['笔数占比']:.1f}%), 平均保费¥{row['平均保费']:.0f}")
        
        return source_distribution
    
    return None

def analyze_real_time_trends(df):
    """分析真实时间趋势"""
    print("\n📅 分析真实时间趋势...")
    
    # 按日期统计
    daily_trends = df.groupby('日期').agg({
        '保单号': 'count',
        '签单保费': 'sum'
    }).reset_index()
    daily_trends.columns = ['日期', '保单笔数', '签单保费']
    daily_trends = daily_trends.sort_values('日期')
    
    print("📈 每日业务趋势：")
    for i, row in daily_trends.iterrows():
        weekday = row['日期'].strftime('%A')
        print(f"   {row['日期']} ({weekday}): {row['保单笔数']}单, ¥{row['签单保费']:,.0f}")
    
    return daily_trends

def analyze_special_vehicles(df):
    """分析特殊车辆标识"""
    print("\n⚠️ 分析特殊车辆标识...")
    
    special_vehicles = {}
    
    # 新能源车
    if '是否新能源' in df.columns:
        new_energy = df[df['是否新能源'] == '是'].shape[0]
        new_energy_pct = round(new_energy / len(df) * 100, 2)
        special_vehicles['新能源车'] = {
            'count': new_energy,
            'percentage': new_energy_pct
        }
        print(f"🔋 新能源车: {new_energy}单 ({new_energy_pct:.1f}%)")
    
    # 过户车
    if '是否过户车' in df.columns:
        transferred = df[df['是否过户车'] == '是'].shape[0]
        transferred_pct = round(transferred / len(df) * 100, 2)
        special_vehicles['过户车'] = {
            'count': transferred,
            'percentage': transferred_pct
        }
        print(f"🔄 过户车: {transferred}单 ({transferred_pct:.1f}%)")
    
    # 网约车
    if '是否网约车' in df.columns:
        ride_hailing = df[df['是否网约车'] == '是'].shape[0]
        ride_hailing_pct = round(ride_hailing / len(df) * 100, 2)
        special_vehicles['网约车'] = {
            'count': ride_hailing,
            'percentage': ride_hailing_pct
        }
        print(f"🚖 网约车: {ride_hailing}单 ({ride_hailing_pct:.1f}%)")
    
    # 异地车
    if '是否异地车' in df.columns:
        out_of_town = df[df['是否异地车'] == '是'].shape[0]
        out_of_town_pct = round(out_of_town / len(df) * 100, 2)
        special_vehicles['异地车'] = {
            'count': out_of_town,
            'percentage': out_of_town_pct
        }
        print(f"🗺️ 异地车: {out_of_town}单 ({out_of_town_pct:.1f}%)")
    
    return special_vehicles

def generate_real_report(data, top_salespeople, org_performance, insurance_distribution, customer_distribution, source_distribution, daily_trends, special_vehicles):
    """生成基于真实数据的分析报告"""
    
    def get_trend_symbol(growth_rate):
        if growth_rate > 5:
            return "⬆️"
        elif growth_rate < -5:
            return "⬇️"
        else:
            return "➡️"
    
    report = f"""# 🚗 车险保批单业务数据分析日报（基于真实数据）

**报告日期**：2025-03-21  
**数据范围**：真实数据覆盖期间  
**生成时间**：2025-03-31 16:00  
**数据来源**：保批单业务报表-20250321.xlsx  

---

## 📊 核心指标看板（真实数据）

| 指标 | 数值 | 备注 |
|------|------|------|
| 保单笔数 | {data['total_policies']:,} 笔 | 实际统计 |
| 签单保费 | ¥{data['total_premium']:,.0f} | 实际汇总 |
| 平均单笔保费 | ¥{data['avg_premium']:.0f} | 实际计算 |
| 活跃业务员 | {data['salespeople_count']} 人 | 实际统计 |
| 三级机构 | {data['org_count']} 个 | 实际统计 |
| 险种类型 | {len(data['insurance_types'])} 种 | 实际统计 |

**🔑 关键发现**：基于真实数据分析，共{data['total_policies']}笔保单，总保费¥{data['total_premium']:,.0f}，涉及{data['salespeople_count']}名业务员和{data['org_count']}个三级机构。

---

## 👥 一、业务员与团队业绩分析

### 1.1 业务员业绩排名（真实数据）

| 排名 | 业务员 | 保单笔数 | 签单保费(元) | 占比 |
|------|--------|---------|------------|------|"""
    
    for i, (_, row) in enumerate(top_salespeople.iterrows(), 1):
        report += f"\n| {i} | {row['业务员']} | {row['保单笔数']} | ¥{row['签单保费']:,.0f} | {row['占比']:.1f}% |"
    
    # 业绩集中度分析
    top_contribution = top_salespeople['签单保费'].sum()
    total_premium = data['total_premium']
    concentration_rate = (top_contribution / total_premium * 100).round(1)
    
    report += f"""

**📊 可视化建议**：横向柱状图（业务员姓名为Y轴，签单保费为X轴）

---

### 1.2 三级机构业绩对比（真实数据）

| 机构 | 保单笔数 | 签单保费(万元) | 占比 |
|------|---------|--------------|------|"""
    
    for _, row in org_performance.iterrows():
        report += f"\n| {row['三级机构']} | {row['保单笔数']} | ¥{row['签单保费']/10000:.1f} | {row['占比']:.1f}% |"
    
    report += f"""

**🥧 可视化建议**：饼图（各机构保费占比）

---

### 1.3 业绩集中度分析

- TOP 业务员贡献占比：**{concentration_rate}%**
- 平均每业务员保费：¥{total_premium/data['salespeople_count']:,.0f}
- 业绩分布：{data['salespeople_count']}名业务员共同承担{data['total_policies']}笔保单

**💡 管理建议**：
- 基于{concentration_rate}%的集中度，需要关注业务员能力均衡发展
- 建议建立业绩分享机制，促进整体团队提升

---

## 🎯 二、产品与险别分析

### 2.1 险种名称分布（真实数据）

| 险种 | 保单笔数 | 签单保费(元) | 占比 |
|------|---------|------------|------|"""
    
    for _, row in insurance_distribution.iterrows():
        report += f"\n| {row['险种名称']} | {row['保单笔数']} | ¥{row['签单保费']:,.0f} | {row['占比']:.1f}% |"
    
    report += f"""

**🥧 可视化建议**：饼图（险种保费占比）

---

## 🚗 三、客户与车辆结构分析

### 3.1 客户类别分布（真实数据）

| 类别 | 保单笔数 | 笔数占比 | 签单保费(万元) | 保费占比 |
|------|---------|---------|--------------|----------|"""
    
    for _, row in customer_distribution.iterrows():
        report += f"\n| {row['客户类别']} | {row['保单笔数']} | {row['笔数占比']:.1f}% | ¥{row['签单保费']/10000:.1f} | {row['保费占比']:.1f}% |"
    
    report += f"""

**🥧 可视化建议**：饼图

---

## ⚠️ 四、特殊车辆标识分析

| 标识 | 笔数 | 占比 |
|------|------|------|"""
    
    for vehicle_type, stats in special_vehicles.items():
        report += f"\n| {vehicle_type} | {stats['count']} | {stats['percentage']:.1f}% |"
    
    if source_distribution is not None:
        report += f"""

---

## 🌐 五、业务来源分析（真实数据）

| 来源 | 保单笔数 | 笔数占比 | 平均保费(元) |
|------|---------|----------|------------|"""
        
        for _, row in source_distribution.iterrows():
            report += f"\n| {row['业务来源']} | {row['保单笔数']} | {row['笔数占比']:.1f}% | ¥{row['平均保费']:.0f} |"
    
    report += f"""

**🥧 可视化建议**：饼图

---

## 📈 六、时间趋势分析（真实数据）

### 6.1 每日业务趋势

| 日期 | 星期 | 保单笔数 | 签单保费(万元) |
|------|------|---------|--------------|"""
    
    for _, row in daily_trends.iterrows():
        weekday = row['日期'].strftime('%A')
        report += f"\n| {row['日期']} | {weekday} | {row['保单笔数']} | ¥{row['签单保费']/10000:.1f} |"
    
    report += f"""

**📈 可视化建议**：折线图（X轴=日期，Y轴=保费）

---

## 🎯 七、基于真实数据的管理建议

### 🔥 立即行动（基于实际数据）
1. **优化业务员资源配置**
   数据支持：{data['salespeople_count']}名业务员处理{data['total_policies']}笔保单
   预期效果：提升人均处理效率，降低运营成本
   行动：分析高绩效业务员工作模式，复制成功经验

2. **强化主力险种销售**
   数据支持：{insurance_distribution.iloc[0]['险种名称']}占比最高({insurance_distribution.iloc[0]['占比']:.1f}%)
   预期效果：巩固优势产品市场地位
   行动：制定专项激励政策，提升主力险种渗透率

### 📌 短期优化
- 关注{customer_distribution.iloc[0]['客户类别']}客户群体的深度开发
- 优化{org_performance.iloc[0]['三级机构']}的成功经验到其他机构
- 加强特殊车辆（新能源车{special_vehicles.get('新能源车', {}).get('percentage', 0):.1f}%）的产品设计

### 💡 长期关注
- 建立基于真实数据的预测模型
- 完善客户画像分析体系
- 优化渠道组合策略

---

## 📎 附录：真实数据说明

- **数据来源**：保批单业务报表-20250321.xlsx
- **数据条数**：{data['total_policies']:,} 条
- **数据字段**：69 个维度
- **业务员数量**：{data['salespeople_count']} 人
- **机构数量**：{data['org_count']} 个
- **险种种类**：{len(data['insurance_types'])} 种
- **客户类别**：{len(data['customer_types'])} 类

---

**报告生成**：AI 数据分析助手（基于真实数据）  
**版本**：v2.0  
**生成时间**：2025-03-31 16:00
"""
    
    return report

def main():
    """主函数 - 基于真实数据"""
    file_path = "/Users/xuechenglong/Downloads/01-公司开发项目/Meta-prompt/output/保批单业务报表-20250321.xlsx"
    
    try:
        print("🚀 开始基于真实数据的深度分析...")
        
        # 1. 基础数据分析
        data = load_real_data_analysis(file_path)
        
        # 2. 业务员业绩分析
        top_salespeople, sales_performance = analyze_real_sales_performance(data['df'])
        
        # 3. 机构业绩分析
        org_performance = analyze_real_organizations(data['df'])
        
        # 4. 险种分析
        insurance_distribution = analyze_real_insurance_products(data['df'])
        
        # 5. 客户结构分析
        customer_distribution = analyze_real_customer_structure(data['df'])
        
        # 6. 渠道分析
        source_distribution = analyze_real_channels(data['df'])
        
        # 7. 时间趋势分析
        daily_trends = analyze_real_time_trends(data['df'])
        
        # 8. 特殊车辆分析
        special_vehicles = analyze_special_vehicles(data['df'])
        
        # 9. 生成真实数据报告
        real_report = generate_real_report(
            data, top_salespeople, org_performance, 
            insurance_distribution, customer_distribution,
            source_distribution, daily_trends, special_vehicles
        )
        
        # 10. 保存报告
        real_report_file = "/Users/xuechenglong/Downloads/01-公司开发项目/Meta-prompt/车险业务分析日报_真实数据_20250321.md"
        with open(real_report_file, 'w', encoding='utf-8') as f:
            f.write(real_report)
        
        print(f"\n✅ 基于真实数据的分析报告生成完成！")
        print(f"📄 报告文件：{real_report_file}")
        print(f"\n📊 真实数据核心指标：")
        print(f"   - 总保单笔数：{data['total_policies']:,} 笔")
        print(f"   - 总签单保费：¥{data['total_premium']:,.0f}")
        print(f"   - 平均单笔保费：¥{data['avg_premium']:.0f}")
        print(f"   - 活跃业务员：{data['salespeople_count']} 人")
        print(f"   - 三级机构：{data['org_count']} 个")
        
    except Exception as e:
        print(f"❌ 真实数据分析过程中出现错误：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()