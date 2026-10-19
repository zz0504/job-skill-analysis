import jieba
import jieba.analyse
from collections import Counter
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.job import JobClean, KeywordStat
from app.models.user import BatchRecord


SKILL_KEYWORDS = [
    'Python', 'Java', 'JavaScript', 'TypeScript', 'Go', 'Rust', 'C++', 'C#',
    'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB',
    'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring',
    'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQL Server',
    'Docker', 'Kubernetes', 'Jenkins', 'Git', 'Linux', 'Nginx',
    'TensorFlow', 'PyTorch', 'Keras', 'OpenCV', 'NLP', '深度学习', '机器学习',
    '数据分析', '数据挖掘', '大数据', 'Hadoop', 'Spark', 'Flink', 'Hive',
    'HTML', 'CSS', 'jQuery', 'Bootstrap', 'Element UI', 'Ant Design',
    'RESTful', 'GraphQL', 'Microservices', '微服务', '分布式',
    'Agile', 'Scrum', 'DevOps', 'CI/CD',
    '英语', '沟通', '团队协作', '项目管理', '领导力'
]

for keyword in SKILL_KEYWORDS:
    jieba.add_word(keyword)


STOP_WORDS = set([
    '的', '了', '和', '是', '在', '有', '我', '他', '她', '它',
    '这', '那', '就', '也', '都', '会', '能', '要', '可以', '需要',
    '负责', '完成', '进行', '实现', '开发', '设计', '维护', '优化',
    '熟悉', '精通', '掌握', '了解', '具备', '拥有', '具有',
    '良好', '优秀', '较强', '强烈', '高度', '丰富',
    '工作', '职位', '岗位', '招聘', '公司', '团队', '部门',
    '经验', '学历', '本科', '硕士', '博士', '大专',
    '年以上', '岁以下', '薪资', '待遇', '福利'
])


def extract_keywords(text: str, top_k: int = 20) -> list:
    if not text or len(text.strip()) < 2:
        return []
    
    keywords = jieba.analyse.extract_tags(
        text,
        topK=top_k * 2,
        withWeight=True,
        allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'v', 'vn', 'eng')
    )
    
    result = []
    for word, weight in keywords:
        if word not in STOP_WORDS and len(word) >= 2:
            result.append({'keyword': word, 'weight': weight})
    
    return result[:top_k]


def get_time_period(date: datetime, time_dim: str = 'month') -> str:
    if not date:
        return ''
    
    if time_dim == 'month':
        return date.strftime('%Y-%m')
    elif time_dim == 'quarter':
        quarter = (date.month - 1) // 3 + 1
        return f"{date.year}-Q{quarter}"
    else:
        return date.strftime('%Y-%m')


def calculate_keywords_stats(
    batch_id: str,
    time_dim: str = 'month',
    top_n: int = 50,
    db: Session = None
) -> dict:
    clean_jobs = db.query(JobClean).filter(
        JobClean.batch_id == batch_id
    ).all()
    
    if not clean_jobs:
        return {
            "status": "error",
            "message": "没有找到清洗后的数据"
        }
    
    keyword_counter = Counter()
    time_keyword_counter = {}
    category_keyword_counter = {}
    
    for job in clean_jobs:
        keywords = extract_keywords(job.description_clean, top_k=20)
        
        time_period = get_time_period(job.publish_date, time_dim)
        
        for kw in keywords:
            keyword = kw['keyword']
            keyword_counter[keyword] += 1
            
            if time_period:
                if time_period not in time_keyword_counter:
                    time_keyword_counter[time_period] = Counter()
                time_keyword_counter[time_period][keyword] += 1
            
            if job.job_category:
                if job.job_category not in category_keyword_counter:
                    category_keyword_counter[job.job_category] = Counter()
                category_keyword_counter[job.job_category][keyword] += 1
    
    stats_records = []
    
    top_keywords = keyword_counter.most_common(top_n)
    for keyword, freq in top_keywords:
        stat = KeywordStat(
            batch_id=batch_id,
            keyword=keyword,
            frequency=freq,
            time_dim=time_dim
        )
        stats_records.append(stat)
    
    for time_period, counter in time_keyword_counter.items():
        for keyword, freq in counter.most_common(top_n):
            stat = KeywordStat(
                batch_id=batch_id,
                keyword=keyword,
                frequency=freq,
                time_period=time_period,
                time_dim=time_dim
            )
            stats_records.append(stat)
    
    for category, counter in category_keyword_counter.items():
        for keyword, freq in counter.most_common(top_n):
            stat = KeywordStat(
                batch_id=batch_id,
                keyword=keyword,
                frequency=freq,
                job_category=category,
                time_dim=time_dim
            )
            stats_records.append(stat)
    
    db.bulk_save_objects(stats_records)
    db.commit()
    
    batch = db.query(BatchRecord).filter(BatchRecord.batch_id == batch_id).first()
    if batch:
        batch.status = 'analyzed'
        db.commit()
    
    return {
        "status": "success",
        "batch_id": batch_id,
        "total_keywords": len(keyword_counter),
        "stats_records": len(stats_records)
    }


def get_keywords(
    batch_id: str,
    top_n: int = 20,
    job_category: str = None,
    time_period: str = None,
    db: Session = None
) -> list:
    query = db.query(KeywordStat).filter(
        KeywordStat.batch_id == batch_id
    )
    
    if time_period:
        query = query.filter(KeywordStat.time_period == time_period)
    else:
        query = query.filter(KeywordStat.time_period.is_(None))
    
    if job_category:
        query = query.filter(KeywordStat.job_category == job_category)
    else:
        query = query.filter(KeywordStat.job_category.is_(None))
    
    results = query.order_by(KeywordStat.frequency.desc()).limit(top_n).all()
    
    keywords = []
    for stat in results:
        keywords.append({
            "name": stat.keyword,
            "value": stat.frequency
        })
    
    return keywords


def get_trend_data(
    batch_id: str,
    keywords: list = None,
    time_dim: str = 'month',
    db: Session = None
) -> dict:
    query = db.query(KeywordStat).filter(
        KeywordStat.batch_id == batch_id,
        KeywordStat.time_dim == time_dim,
        KeywordStat.time_period != None
    )
    
    if keywords:
        query = query.filter(KeywordStat.keyword.in_(keywords))
    
    results = query.all()
    
    trend_data = {}
    for stat in results:
        keyword = stat.keyword
        period = stat.time_period
        
        if keyword not in trend_data:
            trend_data[keyword] = {}
        
        trend_data[keyword][period] = stat.frequency
    
    return trend_data
