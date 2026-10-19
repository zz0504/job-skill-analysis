-- 测试数据初始化脚本
-- 招聘岗位技能关键词分析系统

USE job_skill_analysis;

-- 插入批次记录
INSERT INTO batch_records (batch_id, file_name, total_count, clean_count, status, created_at) VALUES
('batch_test_001', 'test_data_2024.xlsx', 50, 50, 'analyzed', NOW())
ON DUPLICATE KEY UPDATE status='analyzed';

-- 插入原始数据 (jobs_raw)
INSERT INTO jobs_raw (batch_id, job_title, company, publish_date, description, source_file, created_at) VALUES
-- 前端开发岗位
('batch_test_001', '前端开发工程师', '华为技术有限公司', '2024-01-15 10:00:00', '熟练掌握Vue、React等前端框架，熟悉HTML5、CSS3、JavaScript，有良好的编码习惯，熟悉Git版本控制', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '高级前端开发工程师', '阿里巴巴集团', '2024-01-16 09:30:00', '精通Vue3、TypeScript、Webpack/Vite，熟悉Element UI、Ant Design，有大型项目经验，熟练使用Git', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '前端开发工程师', '腾讯科技', '2024-01-17 14:00:00', '熟练使用React、Redux、Axios，熟悉ES6语法，了解Node.js，有移动端开发经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', 'Web前端开发', '字节跳动', '2024-02-01 11:00:00', '精通HTML/CSS/JavaScript，熟悉Vue全家桶，了解小程序开发，有性能优化经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '前端架构师', '京东集团', '2024-02-05 10:30:00', '深入理解前端工程化，熟悉Webpack、Rollup，掌握TypeScript，有微前端架构经验', 'test_data_2024.xlsx', NOW()),
-- 后端开发岗位
('batch_test_001', 'Python后端开发工程师', '美团点评', '2024-01-18 10:00:00', '熟练掌握Python、Django、Flask框架，熟悉MySQL、Redis，了解Docker容器化部署', 'test_data_2024.xlsx', NOW()),
('batch_test_001', 'Java后端开发工程师', '蚂蚁金服', '2024-01-19 09:00:00', '精通Java、Spring Boot、MyBatis，熟悉MySQL、Oracle数据库，有分布式系统开发经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '后端开发工程师', '拼多多', '2024-01-20 15:00:00', '熟练使用Python、FastAPI，熟悉PostgreSQL、MongoDB，了解微服务架构，有高并发经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '高级Java开发', '网易公司', '2024-02-10 11:30:00', '精通Spring Cloud、Dubbo，熟悉Kafka、RabbitMQ，有电商系统开发经验，了解JVM调优', 'test_data_2024.xlsx', NOW()),
('batch_test_001', 'Python开发工程师', '小米科技', '2024-02-15 14:00:00', '熟练掌握Python、SQLAlchemy，熟悉Celery异步任务，有数据分析经验，了解机器学习', 'test_data_2024.xlsx', NOW()),
-- 数据分析岗位
('batch_test_001', '数据分析师', '百度在线', '2024-01-21 10:00:00', '熟练使用Python、Pandas、NumPy，掌握SQL查询，熟悉数据可视化工具，有统计学基础', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '高级数据分析师', '滴滴出行', '2024-01-22 09:30:00', '精通Python数据分析库，熟悉Tableau、PowerBI，有机器学习基础，善于数据建模', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '数据分析师', '快手科技', '2024-02-01 11:00:00', '熟练使用SQL、Excel，了解Python、R语言，熟悉A/B测试，有用户行为分析经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '商业数据分析师', '携程旅行', '2024-02-20 10:00:00', '掌握SQL、Python，熟悉数据挖掘算法，有电商数据分析经验，善于撰写分析报告', 'test_data_2024.xlsx', NOW()),
-- 算法/机器学习岗位
('batch_test_001', '算法工程师', '商汤科技', '2024-01-23 10:00:00', '熟悉机器学习算法，掌握Python、TensorFlow、PyTorch，有深度学习项目经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '机器学习工程师', '旷视科技', '2024-01-24 09:00:00', '精通Python、C++，熟悉CNN、RNN等神经网络，有计算机视觉或NLP项目经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '深度学习工程师', '科大讯飞', '2024-02-05 11:00:00', '熟练使用PyTorch、TensorFlow，熟悉模型优化和部署，有图像识别或语音识别经验', 'test_data_2024.xlsx', NOW()),
-- 测试岗位
('batch_test_001', '软件测试工程师', 'OPPO公司', '2024-01-25 10:30:00', '熟悉软件测试流程，掌握Selenium、JMeter，有自动化测试经验，了解Python', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '测试开发工程师', 'VIVO手机', '2024-01-26 09:00:00', '熟练使用Python、pytest，熟悉接口测试、性能测试，有CI/CD流程经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '自动化测试工程师', '中兴通讯', '2024-02-10 14:00:00', '精通自动化测试框架，熟悉Appium、Robot Framework，有移动端测试经验', 'test_data_2024.xlsx', NOW()),
-- 运维/DevOps岗位
('batch_test_001', '运维工程师', '中国移动', '2024-01-27 10:00:00', '熟悉Linux系统管理，掌握Shell脚本，了解Docker、Kubernetes，有自动化运维经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', 'DevOps工程师', '中国电信', '2024-01-28 09:30:00', '精通CI/CD流程，熟练使用Jenkins、GitLab CI，熟悉云平台AWS/阿里云，有容器化部署经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', 'SRE工程师', '中国联通', '2024-02-15 11:00:00', '熟悉Kubernetes、Prometheus、Grafana，有大规模系统运维经验，了解Go语言', 'test_data_2024.xlsx', NOW()),
-- 产品/设计岗位
('batch_test_001', '产品经理', '哔哩哔哩', '2024-01-29 10:00:00', '熟悉产品规划流程，善于需求分析，有B端或C端产品设计经验，熟练使用Axure、Figma', 'test_data_2024.xlsx', NOW()),
('batch_test_001', 'UI设计师', '知乎社区', '2024-01-30 09:00:00', '精通Photoshop、Sketch，熟悉UI设计规范，有移动端和Web端设计经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '交互设计师', '小红书', '2024-02-01 11:30:00', '熟练使用Figma、Principle，善于用户体验研究，有产品交互设计经验', 'test_data_2024.xlsx', NOW()),
-- 全栈开发
('batch_test_001', '全栈开发工程师', '新浪微博', '2024-02-01 10:00:00', '精通前端Vue/React和后端Node.js/Python，熟悉MySQL、MongoDB，有全栈项目经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '全栈工程师', '贝壳找房', '2024-02-05 09:30:00', '熟练掌握前后端开发，熟悉React、Express、PostgreSQL，有SaaS产品开发经验', 'test_data_2024.xlsx', NOW()),
-- 更多前端岗位
('batch_test_001', '前端开发工程师', '饿了么', '2024-02-10 10:00:00', '熟练使用Vue3、Pinia、Vite，熟悉移动端适配，有H5开发经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '前端开发工程师', '去哪儿网', '2024-02-15 11:00:00', '精通React生态系统，熟悉Next.js，有SSR服务端渲染经验，了解性能优化', 'test_data_2024.xlsx', NOW()),
-- 更多后端岗位
('batch_test_001', 'Go后端开发工程师', '七牛云', '2024-02-20 10:30:00', '熟练掌握Go语言，熟悉Gin框架，了解微服务架构，有高并发服务开发经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', 'Node.js开发工程师', '慕课网', '2024-02-25 09:00:00', '精通Node.js、Express、Koa，熟悉MongoDB、Redis，有实时通信开发经验', 'test_data_2024.xlsx', NOW()),
-- 更多数据岗位
('batch_test_001', '数据工程师', '唯品会', '2024-03-01 10:00:00', '熟悉Hadoop、Spark生态，掌握SQL、Python，有ETL开发经验，了解数仓建设', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '数据科学家', '平安科技', '2024-03-05 11:00:00', '精通统计分析、机器学习，熟练使用Python、R，有金融风控建模经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '大数据开发工程师', '富士康', '2024-03-10 10:00:00', '熟悉Hive、Spark、Flink，有海量数据处理经验，了解数据湖架构', 'test_data_2024.xlsx', NOW()),
-- 安卓/iOS开发
('batch_test_001', 'Android开发工程师', '魅族科技', '2024-03-01 09:30:00', '精通Java、Kotlin，熟悉Android SDK，有App性能优化经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', 'iOS开发工程师', '苹果中国', '2024-03-05 10:00:00', '熟练使用Swift、Objective-C，熟悉iOS开发框架，有App上架经验', 'test_data_2024.xlsx', NOW()),
-- 安全岗位
('batch_test_001', '网络安全工程师', '奇安信', '2024-03-10 09:00:00', '熟悉网络安全攻防技术，掌握渗透测试工具，有安全运维经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '信息安全工程师', '深信服', '2024-03-15 10:30:00', '了解安全合规标准，熟悉加密算法，有安全审计经验，掌握Python', 'test_data_2024.xlsx', NOW()),
-- 区块链
('batch_test_001', '区块链开发工程师', '火币网', '2024-03-01 11:00:00', '熟悉以太坊、智能合约开发，掌握Solidity、Web3.js，有DeFi项目经验', 'test_data_2024.xlsx', NOW()),
-- 云计算
('batch_test_001', '云计算工程师', '华为云', '2024-03-05 10:00:00', '熟悉OpenStack、Kubernetes，了解虚拟化技术，有私有云部署经验', 'test_data_2024.xlsx', NOW()),
-- 嵌入式
('batch_test_001', '嵌入式开发工程师', '大疆创新', '2024-03-10 09:30:00', '精通C/C++，熟悉ARM架构，有RTOS开发经验，了解硬件调试', 'test_data_2024.xlsx', NOW()),
-- 技术支持
('batch_test_001', '技术支持工程师', '海康威视', '2024-03-15 10:00:00', '熟悉Linux、网络协议，有故障排查经验，善于客户沟通', 'test_data_2024.xlsx', NOW()),
-- 项目管理
('batch_test_001', '项目经理', '用友网络', '2024-03-01 11:30:00', '熟悉敏捷开发流程，有PMP证书，善于团队管理，有软件交付经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '技术经理', '金蝶软件', '2024-03-05 10:30:00', '有团队管理经验，熟悉技术架构设计，善于技术选型和团队建设', 'test_data_2024.xlsx', NOW()),
-- 游戏开发
('batch_test_001', '游戏开发工程师', '米哈游', '2024-03-10 09:00:00', '精通C++、Lua，熟悉Unity3D或Unreal引擎，有游戏项目开发经验', 'test_data_2024.xlsx', NOW()),
('batch_test_001', '游戏服务端开发', '莉莉丝游戏', '2024-03-15 11:00:00', '熟练使用Go、C++，熟悉分布式服务器架构，有高并发游戏服务开发经验', 'test_data_2024.xlsx', NOW()),
-- 更多测试岗位
('batch_test_001', '性能测试工程师', '联想集团', '2024-03-01 10:00:00', '精通性能测试工具LoadRunner、JMeter，有系统性能调优经验', 'test_data_2024.xlsx', NOW())
ON DUPLICATE KEY UPDATE job_title=job_title;

-- 插入清洗后数据 (jobs_clean)
INSERT INTO jobs_clean (batch_id, job_title, company, publish_date, description_clean, job_category, created_at) VALUES
-- 前端开发
('batch_test_001', '前端开发工程师', '华为技术有限公司', '2024-01-15 10:00:00', 'Vue React HTML5 CSS3 JavaScript Git', '前端开发', NOW()),
('batch_test_001', '高级前端开发工程师', '阿里巴巴集团', '2024-01-16 09:30:00', 'Vue3 TypeScript Webpack Vite Element UI Ant Design Git', '前端开发', NOW()),
('batch_test_001', '前端开发工程师', '腾讯科技', '2024-01-17 14:00:00', 'React Redux Axios ES6 Node.js 移动端', '前端开发', NOW()),
('batch_test_001', 'Web前端开发', '字节跳动', '2024-02-01 11:00:00', 'HTML CSS JavaScript Vue 小程序 性能优化', '前端开发', NOW()),
('batch_test_001', '前端架构师', '京东集团', '2024-02-05 10:30:00', '前端工程化 Webpack Rollup TypeScript 微前端', '前端开发', NOW()),
('batch_test_001', '前端开发工程师', '饿了么', '2024-02-10 10:00:00', 'Vue3 Pinia Vite H5 移动端', '前端开发', NOW()),
('batch_test_001', '前端开发工程师', '去哪儿网', '2024-02-15 11:00:00', 'React Next.js SSR 性能优化', '前端开发', NOW()),
-- 后端开发
('batch_test_001', 'Python后端开发工程师', '美团点评', '2024-01-18 10:00:00', 'Python Django Flask MySQL Redis Docker', '后端开发', NOW()),
('batch_test_001', 'Java后端开发工程师', '蚂蚁金服', '2024-01-19 09:00:00', 'Java Spring Boot MyBatis MySQL Oracle 分布式', '后端开发', NOW()),
('batch_test_001', '后端开发工程师', '拼多多', '2024-01-20 15:00:00', 'Python FastAPI PostgreSQL MongoDB 微服务 高并发', '后端开发', NOW()),
('batch_test_001', '高级Java开发', '网易公司', '2024-02-10 11:30:00', 'Spring Cloud Dubbo Kafka RabbitMQ 电商 JVM', '后端开发', NOW()),
('batch_test_001', 'Python开发工程师', '小米科技', '2024-02-15 14:00:00', 'Python SQLAlchemy Celery 数据分析 机器学习', '后端开发', NOW()),
('batch_test_001', 'Go后端开发工程师', '七牛云', '2024-02-20 10:30:00', 'Go Gin 微服务 高并发', '后端开发', NOW()),
('batch_test_001', 'Node.js开发工程师', '慕课网', '2024-02-25 09:00:00', 'Node.js Express Koa MongoDB Redis 实时通信', '后端开发', NOW()),
-- 数据分析
('batch_test_001', '数据分析师', '百度在线', '2024-01-21 10:00:00', 'Python Pandas NumPy SQL 数据可视化 统计学', '数据分析', NOW()),
('batch_test_001', '高级数据分析师', '滴滴出行', '2024-01-22 09:30:00', 'Python Tableau PowerBI 机器学习 数据建模', '数据分析', NOW()),
('batch_test_001', '数据分析师', '快手科技', '2024-02-01 11:00:00', 'SQL Excel Python R A/B测试 用户行为分析', '数据分析', NOW()),
('batch_test_001', '商业数据分析师', '携程旅行', '2024-02-20 10:00:00', 'SQL Python 数据挖掘 电商数据 分析报告', '数据分析', NOW()),
-- 算法/机器学习
('batch_test_001', '算法工程师', '商汤科技', '2024-01-23 10:00:00', '机器学习 Python TensorFlow PyTorch 深度学习', '算法工程师', NOW()),
('batch_test_001', '机器学习工程师', '旷视科技', '2024-01-24 09:00:00', 'Python C++ CNN RNN 计算机视觉 NLP', '算法工程师', NOW()),
('batch_test_001', '深度学习工程师', '科大讯飞', '2024-02-05 11:00:00', 'PyTorch TensorFlow 模型优化 图像识别 语音识别', '算法工程师', NOW()),
('batch_test_001', '数据科学家', '平安科技', '2024-03-05 11:00:00', '统计分析 机器学习 Python R 金融风控', '算法工程师', NOW()),
-- 测试
('batch_test_001', '软件测试工程师', 'OPPO公司', '2024-01-25 10:30:00', '软件测试 Selenium JMeter 自动化测试 Python', '测试工程师', NOW()),
('batch_test_001', '测试开发工程师', 'VIVO手机', '2024-01-26 09:00:00', 'Python pytest 接口测试 性能测试 CI/CD', '测试工程师', NOW()),
('batch_test_001', '自动化测试工程师', '中兴通讯', '2024-02-10 14:00:00', '自动化测试框架 Appium Robot Framework 移动端测试', '测试工程师', NOW()),
('batch_test_001', '性能测试工程师', '联想集团', '2024-03-01 10:00:00', 'LoadRunner JMeter 性能调优', '测试工程师', NOW()),
-- 运维/DevOps
('batch_test_001', '运维工程师', '中国移动', '2024-01-27 10:00:00', 'Linux Shell Docker Kubernetes 自动化运维', '运维工程师', NOW()),
('batch_test_001', 'DevOps工程师', '中国电信', '2024-01-28 09:30:00', 'CI/CD Jenkins GitLab CI AWS 阿里云 容器化', '运维工程师', NOW()),
('batch_test_001', 'SRE工程师', '中国联通', '2024-02-15 11:00:00', 'Kubernetes Prometheus Grafana Go', '运维工程师', NOW()),
('batch_test_001', '云计算工程师', '华为云', '2024-03-05 10:00:00', 'OpenStack Kubernetes 虚拟化 私有云', '运维工程师', NOW()),
-- 产品/设计
('batch_test_001', '产品经理', '哔哩哔哩', '2024-01-29 10:00:00', '产品规划 需求分析 B端 C端 Axure Figma', '产品经理', NOW()),
('batch_test_001', 'UI设计师', '知乎社区', '2024-01-30 09:00:00', 'Photoshop Sketch UI设计 移动端 Web端', 'UI设计师', NOW()),
('batch_test_001', '交互设计师', '小红书', '2024-02-01 11:30:00', 'Figma Principle 用户体验 交互设计', 'UI设计师', NOW()),
-- 全栈
('batch_test_001', '全栈开发工程师', '新浪微博', '2024-02-01 10:00:00', 'Vue React Node.js Python MySQL MongoDB', '全栈开发', NOW()),
('batch_test_001', '全栈工程师', '贝壳找房', '2024-02-05 09:30:00', 'React Express PostgreSQL SaaS', '全栈开发', NOW()),
-- 数据工程
('batch_test_001', '数据工程师', '唯品会', '2024-03-01 10:00:00', 'Hadoop Spark SQL Python ETL 数仓', '数据工程师', NOW()),
('batch_test_001', '大数据开发工程师', '富士康', '2024-03-10 10:00:00', 'Hive Spark Flink 海量数据 数据湖', '数据工程师', NOW()),
-- 移动端
('batch_test_001', 'Android开发工程师', '魅族科技', '2024-03-01 09:30:00', 'Java Kotlin Android SDK App优化', '移动端开发', NOW()),
('batch_test_001', 'iOS开发工程师', '苹果中国', '2024-03-05 10:00:00', 'Swift Objective-C iOS App上架', '移动端开发', NOW()),
-- 安全
('batch_test_001', '网络安全工程师', '奇安信', '2024-03-10 09:00:00', '网络安全 渗透测试 安全运维', '安全工程师', NOW()),
('batch_test_001', '信息安全工程师', '深信服', '2024-03-15 10:30:00', '安全合规 加密算法 安全审计 Python', '安全工程师', NOW()),
-- 区块链
('batch_test_001', '区块链开发工程师', '火币网', '2024-03-01 11:00:00', '以太坊 智能合约 Solidity Web3.js DeFi', '区块链开发', NOW()),
-- 嵌入式
('batch_test_001', '嵌入式开发工程师', '大疆创新', '2024-03-10 09:30:00', 'C C++ ARM RTOS 硬件调试', '嵌入式开发', NOW()),
-- 技术支持
('batch_test_001', '技术支持工程师', '海康威视', '2024-03-15 10:00:00', 'Linux 网络协议 故障排查', '技术支持', NOW()),
-- 项目管理
('batch_test_001', '项目经理', '用友网络', '2024-03-01 11:30:00', '敏捷开发 PMP 团队管理', '项目管理', NOW()),
('batch_test_001', '技术经理', '金蝶软件', '2024-03-05 10:30:00', '团队管理 架构设计 技术选型', '项目管理', NOW()),
-- 游戏开发
('batch_test_001', '游戏开发工程师', '米哈游', '2024-03-10 09:00:00', 'C++ Lua Unity3D Unreal', '游戏开发', NOW()),
('batch_test_001', '游戏服务端开发', '莉莉丝游戏', '2024-03-15 11:00:00', 'Go C++ 分布式 高并发', '游戏开发', NOW())
ON DUPLICATE KEY UPDATE job_title=job_title;

-- 插入关键词统计数据 (keywords_stat)
INSERT INTO keywords_stat (batch_id, keyword, frequency, job_category, time_period, time_dim, created_at) VALUES
-- 前端开发关键词
('batch_test_001', 'Vue', 15, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'React', 12, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'JavaScript', 18, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'TypeScript', 8, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'HTML5', 10, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'CSS3', 10, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Webpack', 6, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Vite', 5, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Element UI', 4, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Ant Design', 3, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Git', 8, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', '性能优化', 4, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', '小程序', 3, '前端开发', '2024-01', 'month', NOW()),
('batch_test_001', '移动端', 5, '前端开发', '2024-01', 'month', NOW()),
-- 后端开发关键词
('batch_test_001', 'Python', 20, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Java', 12, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Go', 5, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Node.js', 6, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Spring Boot', 8, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Django', 4, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Flask', 3, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'FastAPI', 4, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'MySQL', 15, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Redis', 10, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'MongoDB', 5, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Docker', 8, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', '微服务', 6, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', '高并发', 5, '后端开发', '2024-01', 'month', NOW()),
('batch_test_001', '分布式', 6, '后端开发', '2024-01', 'month', NOW()),
-- 数据分析关键词
('batch_test_001', 'SQL', 18, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', 'Pandas', 8, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', 'NumPy', 6, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', '数据可视化', 5, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', 'Tableau', 3, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', 'PowerBI', 3, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', 'Excel', 4, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', '统计学', 3, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', 'A/B测试', 2, '数据分析', '2024-01', 'month', NOW()),
('batch_test_001', '数据建模', 4, '数据分析', '2024-01', 'month', NOW()),
-- 算法工程师关键词
('batch_test_001', '机器学习', 10, '算法工程师', '2024-01', 'month', NOW()),
('batch_test_001', '深度学习', 8, '算法工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'TensorFlow', 6, '算法工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'PyTorch', 8, '算法工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'C++', 6, '算法工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'CNN', 3, '算法工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'RNN', 3, '算法工程师', '2024-01', 'month', NOW()),
('batch_test_001', '计算机视觉', 4, '算法工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'NLP', 3, '算法工程师', '2024-01', 'month', NOW()),
-- 测试工程师关键词
('batch_test_001', '自动化测试', 8, '测试工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Selenium', 4, '测试工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'JMeter', 4, '测试工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'pytest', 3, '测试工程师', '2024-01', 'month', NOW()),
('batch_test_001', '接口测试', 3, '测试工程师', '2024-01', 'month', NOW()),
('batch_test_001', '性能测试', 4, '测试工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'LoadRunner', 2, '测试工程师', '2024-01', 'month', NOW()),
-- 运维工程师关键词
('batch_test_001', 'Linux', 12, '运维工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Kubernetes', 8, '运维工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Docker', 10, '运维工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'CI/CD', 6, '运维工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Jenkins', 4, '运维工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Shell', 5, '运维工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Prometheus', 3, '运维工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Grafana', 3, '运维工程师', '2024-01', 'month', NOW()),
-- 产品经理关键词
('batch_test_001', '需求分析', 6, '产品经理', '2024-01', 'month', NOW()),
('batch_test_001', '产品规划', 5, '产品经理', '2024-01', 'month', NOW()),
('batch_test_001', 'Axure', 4, '产品经理', '2024-01', 'month', NOW()),
('batch_test_001', 'Figma', 5, '产品经理', '2024-01', 'month', NOW()),
('batch_test_001', '敏捷开发', 3, '产品经理', '2024-01', 'month', NOW()),
-- 数据工程师关键词
('batch_test_001', 'Hadoop', 5, '数据工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Spark', 6, '数据工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Hive', 4, '数据工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'ETL', 4, '数据工程师', '2024-01', 'month', NOW()),
('batch_test_001', 'Flink', 3, '数据工程师', '2024-01', 'month', NOW()),
-- 安全工程师关键词
('batch_test_001', '网络安全', 4, '安全工程师', '2024-01', 'month', NOW()),
('batch_test_001', '渗透测试', 3, '安全工程师', '2024-01', 'month', NOW()),
('batch_test_001', '安全运维', 3, '安全工程师', '2024-01', 'month', NOW()),
('batch_test_001', '加密算法', 2, '安全工程师', '2024-01', 'month', NOW()),
-- 移动端开发关键词
('batch_test_001', 'Android', 5, '移动端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'iOS', 4, '移动端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Swift', 3, '移动端开发', '2024-01', 'month', NOW()),
('batch_test_001', 'Kotlin', 3, '移动端开发', '2024-01', 'month', NOW()),
-- 其他热门关键词（不限岗位类别）
('batch_test_001', 'Git', 25, NULL, '2024-01', 'month', NOW()),
('batch_test_001', 'Python', 35, NULL, '2024-01', 'month', NOW()),
('batch_test_001', 'MySQL', 22, NULL, '2024-01', 'month', NOW()),
('batch_test_001', 'Docker', 18, NULL, '2024-01', 'month', NOW()),
('batch_test_001', 'Linux', 20, NULL, '2024-01', 'month', NOW()),
('batch_test_001', 'JavaScript', 25, NULL, '2024-01', 'month', NOW()),
-- 季度数据
('batch_test_001', 'Python', 35, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'Java', 20, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'JavaScript', 28, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'Go', 8, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'Vue', 18, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'React', 15, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'MySQL', 25, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'Redis', 15, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'Docker', 20, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', 'Kubernetes', 12, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', '机器学习', 12, NULL, '2024-Q1', 'quarter', NOW()),
('batch_test_001', '深度学习', 10, NULL, '2024-Q1', 'quarter', NOW())
ON DUPLICATE KEY UPDATE frequency=frequency;

-- 完成提示
SELECT '测试数据插入完成！' AS message;
SELECT COUNT(*) AS jobs_raw_count FROM jobs_raw WHERE batch_id='batch_test_001';
SELECT COUNT(*) AS jobs_clean_count FROM jobs_clean WHERE batch_id='batch_test_001';
SELECT COUNT(*) AS keywords_stat_count FROM keywords_stat WHERE batch_id='batch_test_001';
