-- ============================================
-- 招聘岗位技能关键词分析系统 - 数据库快速配置
-- ============================================

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS job_skill_analysis 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. 使用数据库
USE job_skill_analysis;

-- 3. 显示创建结果
SELECT '数据库创建成功！' AS message;
SELECT DATABASE() AS current_database;

-- ============================================
-- 核心表结构
-- ============================================

-- 原始数据表
DROP TABLE IF EXISTS jobs_raw;
CREATE TABLE jobs_raw (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    batch_id VARCHAR(64) NOT NULL COMMENT '批次ID',
    job_title VARCHAR(255) NOT NULL COMMENT '岗位名称',
    company VARCHAR(255) NOT NULL COMMENT '公司名称',
    publish_date DATETIME COMMENT '发布日期',
    description TEXT COMMENT '技能描述',
    source_file VARCHAR(255) COMMENT '来源文件',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原始数据表';

-- 清洗后数据表
DROP TABLE IF EXISTS jobs_clean;
CREATE TABLE jobs_clean (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    batch_id VARCHAR(64) NOT NULL COMMENT '批次ID',
    job_title VARCHAR(255) NOT NULL COMMENT '岗位名称',
    company VARCHAR(255) NOT NULL COMMENT '公司名称',
    publish_date DATETIME NOT NULL COMMENT '发布日期',
    description_clean TEXT COMMENT '清洗后描述',
    job_category VARCHAR(64) COMMENT '岗位类别',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_batch_date (batch_id, publish_date),
    INDEX idx_category (job_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='清洗后数据表';

-- 关键词统计表
DROP TABLE IF EXISTS keywords_stat;
CREATE TABLE keywords_stat (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    batch_id VARCHAR(64) NOT NULL COMMENT '批次ID',
    keyword VARCHAR(128) NOT NULL COMMENT '关键词',
    frequency INT NOT NULL DEFAULT 0 COMMENT '频次',
    job_category VARCHAR(64) COMMENT '岗位类别',
    time_period VARCHAR(20) COMMENT '时间段(月/季度)',
    time_dim VARCHAR(10) COMMENT '时间维度(month/quarter)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE INDEX uk_batch_skill_time (batch_id, keyword, job_category, time_period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='关键词统计表';

-- 批次记录表
DROP TABLE IF EXISTS batch_records;
CREATE TABLE batch_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    batch_id VARCHAR(64) NOT NULL UNIQUE COMMENT '批次ID',
    file_name VARCHAR(255) COMMENT '文件名',
    total_count INT DEFAULT 0 COMMENT '总记录数',
    clean_count INT DEFAULT 0 COMMENT '清洗后记录数',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='批次记录表';

-- 用户表（可选）
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    username VARCHAR(64) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码哈希',
    email VARCHAR(128) COMMENT '邮箱',
    is_active TINYINT DEFAULT 1 COMMENT '是否激活',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ============================================
-- 验证
-- ============================================

-- 显示所有表
SHOW TABLES;

-- 显示表结构统计
SELECT 
    TABLE_NAME AS '表名',
    TABLE_COMMENT AS '说明',
    TABLE_ROWS AS '记录数',
    ROUND(DATA_LENGTH/1024/1024, 2) AS '数据大小(MB)'
FROM 
    information_schema.TABLES 
WHERE 
    TABLE_SCHEMA = 'job_skill_analysis'
ORDER BY 
    TABLE_NAME;

SELECT '数据库初始化完成！' AS message;
