from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.job import KeywordStat
from typing import List, Dict


def get_job_skill_matrix(
    batch_id: str,
    top_n: int = 10,
    db: Session = None
) -> List[Dict]:
    results = db.query(KeywordStat).filter(
        KeywordStat.batch_id == batch_id,
        KeywordStat.job_category != None,
        KeywordStat.time_period == None
    ).order_by(
        KeywordStat.job_category,
        KeywordStat.frequency.desc()
    ).all()
    
    category_keywords = {}
    for stat in results:
        category = stat.job_category
        keyword = stat.keyword
        
        if category not in category_keywords:
            category_keywords[category] = {}
        
        if len(category_keywords[category]) < top_n:
            category_keywords[category][keyword] = stat.frequency
    
    matrix_data = []
    for category, keywords in category_keywords.items():
        for keyword, frequency in keywords.items():
            matrix_data.append({
                'job': category,
                'skill': keyword,
                'count': frequency
            })
    
    return matrix_data


def get_matrix_table(
    batch_id: str,
    top_n: int = 10,
    db: Session = None
) -> Dict:
    matrix_data = get_job_skill_matrix(batch_id, top_n, db)
    
    all_skills = set()
    all_jobs = set()
    
    for item in matrix_data:
        all_skills.add(item['skill'])
        all_jobs.add(item['job'])
    
    skills = sorted(list(all_skills))
    jobs = sorted(list(all_jobs))
    
    table = []
    for job in jobs:
        row = {'岗位类别': job}
        for skill in skills:
            item = next(
                (m for m in matrix_data if m['job'] == job and m['skill'] == skill),
                None
            )
            row[skill] = item['count'] if item else 0
        table.append(row)
    
    return {
        'columns': ['岗位类别'] + skills,
        'data': table
    }
