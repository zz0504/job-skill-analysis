from datetime import datetime
from typing import Dict, List


def generate_report_data(
    keywords: List[Dict],
    trend_data: Dict,
    matrix_data: List[Dict],
    batch_info: Dict
) -> Dict:
    report = {
        "title": "招聘岗位技能关键词分析报告",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "batch_info": batch_info,
        "summary": {
            "total_keywords": len(keywords),
            "top_keywords": keywords[:10],
            "categories": len(set([m['job'] for m in matrix_data]))
        },
        "keywords": keywords,
        "trend": trend_data,
        "matrix": matrix_data,
        "conclusions": generate_conclusions(keywords, trend_data, matrix_data)
    }
    
    return report


def generate_conclusions(
    keywords: List[Dict],
    trend_data: Dict,
    matrix_data: List[Dict]
) -> List[str]:
    conclusions = []
    
    if keywords:
        top_keyword = keywords[0]
        conclusions.append(
            f"最热门技能为【{top_keyword['name']}】，出现频次达{top_keyword['value']}次"
        )
    
    if len(keywords) >= 3:
        top3 = [kw['name'] for kw in keywords[:3]]
        conclusions.append(
            f"排名前三的技能为：{', '.join(top3)}，是当前市场最紧缺的技能"
        )
    
    categories = {}
    for item in matrix_data:
        cat = item['job']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += item['count']
    
    if categories:
        sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        if sorted_cats:
            conclusions.append(
                f"技能需求最旺盛的岗位类别是【{sorted_cats[0][0]}】，共计{sorted_cats[0][1]}次技能提及"
            )
    
    return conclusions
