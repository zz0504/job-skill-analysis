import uuid
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.job import JobRaw, JobClean
from app.models.user import BatchRecord, User
from app.core.logger import logger
from app.core.auth import get_password_hash

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

JOB_CATEGORIES = {
    '开发': ['开发', '工程师', '程序员', '架构师', '开发工程师', '后端', '前端', '全栈'],
    '运维': ['运维', 'DevOps', 'SRE', '系统管理员', '网络工程师'],
    '测试': ['测试', 'QA', '测试工程师', '自动化测试'],
    '产品': ['产品', 'PM', '产品经理', '产品助理'],
    '设计': ['设计', 'UI', 'UX', '视觉设计', '交互设计'],
    '数据': ['数据', '数据分析', '数据挖掘', '算法', 'AI', '机器学习'],
    '运营': ['运营', '市场', '推广', '增长'],
    '管理': ['经理', '总监', '主管', '负责人', 'Lead']
}


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


def classify_job(job_title: str) -> str:
    if not job_title:
        return '其他'
    
    job_title_lower = job_title.lower()
    
    for category, keywords in JOB_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in job_title_lower:
                return category
    
    return '其他'


def init_test_data(db: Session, num_records: int = 100) -> bool:
    try:
        test_user = db.query(User).filter(User.username == 'test').first()
        if not test_user:
            test_user = User(
                username='test',
                password=get_password_hash('123456'),
                email='test@example.com',
                is_active=1
            )
            db.add(test_user)
            db.commit()
            logger.info("测试用户创建成功: test / 123456")
        
        existing_test = db.query(BatchRecord).filter(
            BatchRecord.file_name == 'test_data_init.csv'
        ).first()
        
        if existing_test:
            logger.info("测试数据已存在，跳过初始化")
            return False
        
        batch_id = str(uuid.uuid4())
        logger.info(f"开始初始化测试数据，batch_id: {batch_id}")
        
        raw_records = []
        base_date = datetime.now() - timedelta(days=365)
        
        for i in range(num_records):
            template = random.choice(JOB_TEMPLATES)
            
            days_ago = random.randint(0, 365)
            publish_date = base_date + timedelta(days=days_ago)
            
            company = random.choice(COMPANIES)
            
            description = generate_job_description(template['skills'])
            
            raw_record = JobRaw(
                batch_id=batch_id,
                job_title=template['title'],
                company=company,
                publish_date=publish_date,
                description=description,
                source_file='test_data_init.csv'
            )
            raw_records.append(raw_record)
        
        db.bulk_save_objects(raw_records)
        
        batch_record = BatchRecord(
            batch_id=batch_id,
            file_name='test_data_init.csv',
            total_count=num_records,
            status='uploaded'
        )
        db.add(batch_record)
        db.commit()
        
        logger.info(f"原始数据导入成功: {num_records} 条")
        
        clean_records = []
        seen = set()
        
        for job in raw_records:
            key = (job.job_title, job.company, job.publish_date)
            
            if key in seen:
                continue
            
            seen.add(key)
            
            job_category = classify_job(job.job_title)
            
            clean_record = JobClean(
                batch_id=batch_id,
                job_title=job.job_title,
                company=job.company,
                publish_date=job.publish_date,
                description_clean=job.description,
                job_category=job_category
            )
            clean_records.append(clean_record)
        
        db.bulk_save_objects(clean_records)
        
        batch_record.clean_count = len(clean_records)
        batch_record.status = 'completed'
        db.commit()
        
        logger.info(f"测试数据初始化完成: 原始数据 {num_records} 条, 清洗后 {len(clean_records)} 条")
        
        return True
        
    except Exception as e:
        db.rollback()
        logger.error(f"测试数据初始化失败: {str(e)}", exc_info=True)
        return False
