-- 修复数据库字符编码问题
-- 在MySQL命令行中执行此脚本

-- 设置客户端编码
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 显示当前字符集配置
SHOW VARIABLES LIKE 'character%';

-- 显示数据库信息
USE job_skill_analysis;
SHOW TABLE STATUS;

-- 验证表结构（应该正确显示中文）
SHOW CREATE TABLE jobs_raw\G
SHOW CREATE TABLE jobs_clean\G
SHOW CREATE TABLE keywords_stat\G

SELECT '数据库字符编码正常！' AS message;
