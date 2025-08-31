#!/usr/bin/env python3
"""
健康保险成本效益分析计算器
日期: 2025年8月31日
"""

import json
from datetime import datetime, timedelta

def calculate_insurance_costs():
    """计算不同保险方案的成本"""
    
    # 基础参数
    school_insurance = {
        "name": "学校保险",
        "cost_3_months": 1000,
        "payment": "一次性",
        "copay_emergency": 300,
        "copay_urgent": 75,
        "copay_specialist": 50,
        "deductible": 350,
        "out_of_network_coverage": 0.6,  # 60%覆盖
    }
    
    kimber_insurance = {
        "name": "Kimber旅行保险",
        "monthly_cost": 125,  # 取中间值
        "payment": "按月",
        "copay_emergency": 0,
        "copay_urgent": 0,
        "copay_specialist": 0,
        "deductible": 100,
        "max_coverage": 1000000,
    }
    
    # 时间范围
    periods = [3, 6, 12]  # 月数
    
    results = {
        "comparison_date": datetime.now().strftime("%Y-%m-%d"),
        "periods": {}
    }
    
    for months in periods:
        school_cost = (months // 3) * school_insurance["cost_3_months"]
        kimber_cost = months * kimber_insurance["monthly_cost"]
        savings = school_cost - kimber_cost
        
        results["periods"][f"{months}_months"] = {
            "school_insurance": school_cost,
            "kimber_insurance": kimber_cost,
            "savings_with_kimber": savings,
            "savings_percentage": round((savings / school_cost) * 100, 1)
        }
    
    # 不同医疗场景分析
    scenarios = {
        "no_medical_needs": {
            "description": "无医疗需求",
            "school_cost": 1000,
            "kimber_cost": 375  # 3个月
        },
        "one_emergency": {
            "description": "一次急诊",
            "school_cost": 1000 + 300,  # 保费 + 共付
            "kimber_cost": 375  # 全额覆盖
        },
        "monthly_checkup": {
            "description": "每月体检",
            "school_cost": 1000,  # 预防性护理覆盖
            "kimber_cost": 375 + 300  # 保费 + 自付
        },
        "out_of_state_emergency": {
            "description": "州外急诊",
            "school_cost": 1000 + 500 + 2000 * 0.4,  # 保费 + 免赔额 + 40%自付
            "kimber_cost": 375 + 100  # 保费 + 免赔额
        }
    }
    
    results["scenarios"] = scenarios
    
    # 风险调整后的期望成本
    # 假设概率：80%无需求，15%需要紧急护理，5%需要急诊
    expected_school = 0.8 * 1000 + 0.15 * (1000 + 75) + 0.05 * (1000 + 300)
    expected_kimber = 0.8 * 375 + 0.15 * 375 + 0.05 * 375
    
    results["risk_adjusted"] = {
        "expected_cost_school": round(expected_school, 2),
        "expected_cost_kimber": round(expected_kimber, 2),
        "expected_savings": round(expected_school - expected_kimber, 2)
    }
    
    return results

def generate_recommendation(analysis):
    """基于分析生成建议"""
    savings_3m = analysis["periods"]["3_months"]["savings_with_kimber"]
    
    if savings_3m > 500:
        return {
            "recommendation": "强烈推荐Kimber旅行保险",
            "confidence": "高",
            "primary_reasons": [
                f"3个月节省${savings_3m}",
                "完美匹配跨州需求",
                "支付灵活性高"
            ]
        }
    else:
        return {
            "recommendation": "建议详细比较后决定",
            "confidence": "中",
            "primary_reasons": [
                "成本差异不够显著",
                "需要评估具体医疗需求",
                "考虑覆盖范围差异"
            ]
        }

def main():
    print("=" * 60)
    print("健康保险成本效益分析")
    print("分析日期: 2025年8月31日")
    print("=" * 60)
    
    # 执行分析
    analysis = calculate_insurance_costs()
    recommendation = generate_recommendation(analysis)
    
    # 输出结果
    print("\n📊 成本对比:")
    print("-" * 40)
    for period, data in analysis["periods"].items():
        months = period.replace("_months", "个月")
        print(f"\n{months}:")
        print(f"  学校保险: ${data['school_insurance']:,}")
        print(f"  Kimber保险: ${data['kimber_insurance']:,}")
        print(f"  节省金额: ${data['savings_with_kimber']:,} ({data['savings_percentage']}%)")
    
    print("\n📈 场景分析:")
    print("-" * 40)
    for scenario_id, scenario in analysis["scenarios"].items():
        print(f"\n{scenario['description']}:")
        print(f"  学校保险总成本: ${scenario['school_cost']:,}")
        print(f"  Kimber保险总成本: ${scenario['kimber_cost']:,}")
        print(f"  Kimber节省: ${scenario['school_cost'] - scenario['kimber_cost']:,}")
    
    print("\n🎯 风险调整后期望成本 (3个月):")
    print("-" * 40)
    print(f"学校保险: ${analysis['risk_adjusted']['expected_cost_school']:,}")
    print(f"Kimber保险: ${analysis['risk_adjusted']['expected_cost_kimber']:,}")
    print(f"期望节省: ${analysis['risk_adjusted']['expected_savings']:,}")
    
    print("\n💡 最终建议:")
    print("-" * 40)
    print(f"建议: {recommendation['recommendation']}")
    print(f"信心度: {recommendation['confidence']}")
    print("主要理由:")
    for reason in recommendation['primary_reasons']:
        print(f"  • {reason}")
    
    # 保存结果到JSON
    with open('cost_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            "analysis": analysis,
            "recommendation": recommendation
        }, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 分析结果已保存到 cost_analysis_results.json")
    
    return analysis, recommendation

if __name__ == "__main__":
    main()