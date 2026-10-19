-- 默认管理员账号
-- 用户名: admin
-- 密码: CHANGE_ME_ADMIN_PWD (加密后的hash值，使用bcrypt生成)

-- 如果用户表不存在则创建
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码哈希',
    email VARCHAR(128) COMMENT '邮箱',
    is_active INT DEFAULT 1 COMMENT '是否激活',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
);

-- 插入默认管理员账号
-- 密码 CHANGE_ME_ADMIN_PWD 的bcrypt hash值
INSERT INTO users (username, password, email, is_active) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHA8CO5jYwQZ9dqXvK9Z8YqN5xJmZ8YqN5xJm', 'admin@example.com', 1)
ON DUPLICATE KEY UPDATE username=username;

-- 创建测试账号
-- 用户名: test, 密码: CHANGE_ME_TEST_PWD
INSERT INTO users (username, password, email, is_active) 
VALUES ('test', '$2b$12$LQv3c1yqBWVHxkd0LHA8CO5jYwQZ9dqXvK9Z8YqN5xJmZ8YqN5xJm', 'test@example.com', 1)
ON DUPLICATE KEY UPDATE username=username;
