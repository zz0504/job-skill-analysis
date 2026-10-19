import pandas as pd
import random
from datetime import datetime, timedelta
import os

SKILLS = [
    'Python', 'Java', 'JavaScript', 'TypeScript', 'Go', 'React', 'Vue', 'Angular',
    'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes',
    'TensorFlow', 'PyTorch', '数据分析', '机器学习', '深度学习', 'NLP',
    'Spring', 'Django', 'Flask', 'Node.js', 'Linux', 'Git', 'Jenkins',
    'Hadoop', 'Spark', 'Flink', 'Kafka', 'ElasticSearch'
]

COMPANIES = [
    '华为', '阿里巴巴', '腾讯', '字节跳动', '美团', '百度', '京东', '小米',
    '网易', '滴滴出行', '快手', 'B站', '知乎', '携程', '平安科技'
]

JOB_TEMPLATES = [
    {'title': 'Python开发工程师', 'category': '开发', 'skills': ['Python', 'Django', 'MySQL', 'Redis', 'Docker']},
    {'title': 'Java后端工程师', 'category': '开发', 'skills': ['Java', 'Spring', 'MySQL', 'Redis', 'Docker']},
    {'title': '前端开发工程师', 'category': '开发', 'skills': ['JavaScript', 'React', 'Vue', 'TypeScript', 'Node.js']},
    {'title': '大数据工程师', 'category': '数据', 'skills': ['Hadoop', 'Spark', 'Flink', 'Hive', 'Python']},
    {'title': '算法工程师', 'category': '数据', 'skills': ['Python', 'TensorFlow', 'PyTorch', '机器学习', '深度学习']},
    {'title': '数据分析师', 'category': '数据', 'skills': ['Python', '数据分析', 'SQL', 'Excel', 'Tableau']},
    {'title': '运维工程师', 'category': '运维', 'skills': ['Linux', 'Docker', 'Kubernetes', 'Jenkins', 'Git']},
    {'title': '测试工程师', 'category': '测试', 'skills': ['Python', 'Selenium', 'JMeter', 'Git', 'Linux']},
    {'title': '产品经理', 'category': '产品', 'skills': ['数据分析', '需求分析', '原型设计', '项目管理', '沟通']},
]


def generate_job_description(skills, add_random=True):
    base_skills = skills.copy()
    
    if add_random:
        extra_count = random.randint(2, 5)
        extra_skills = [s for s in SKILLS if s not in base_skills]
        if extra_skills:
            base_skills.extend(random.sample(extra_skills, min(extra_count, len(extra_skills))))
    
    random.shuffle(base_skills)
    
    descriptions = [
        f"熟练掌握{base_skills[0]}，有实际项目经验",
        f"熟悉{base_skills[1]}，了解{base_skills[2]}",
        f"具备{base_skills[0]}、{base_skills[1]}开发能力",
        f"精通{base_skills[0]}，熟悉{base_skills[1]}、{base_skills[2]}等技术栈",
    ]
    
    return "；".join(random.sample(descriptions, min(2, len(descriptions))))


def generate_sample_data(num_records=1000, output_file='sample_jobs.csv'):
    records = []
    base_date = datetime.now() - timedelta(days=365)
    
    for i in range(num_records):
        template = random.choice(JOB_TEMPLATES)
        
        days_ago = random.randint(0, 365)
        publish_date = base_date + timedelta(days=days_ago)
        
        company = random.choice(COMPANIES)
        
        description = generate_job_description(template['skills'])
        
        records.append({
            '岗位名称': template['title'],
            '公司': company,
            '发布时间': publish_date.strftime('%Y-%m-%d'),
            '技能描述': description
        })
    
    df = pd.DataFrame(records)
    
    df = df.sort_values('发布时间', ascending=False).reset_index(drop=True)
    
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"已生成 {num_records} 条测试数据，保存至: {output_path}")
    print(f"\n数据统计:")
    print(f"- 岗位类型: {df['岗位名称'].nunique()} 种")
    print(f"- 公司数量: {df['公司'].nunique()} 家")
    print(f"- 时间范围: {df['发布时间'].min()} 至 {df['发布时间'].max()}")
    
    return output_path


if __name__ == '__main__':
    generate_sample_data(1000)
