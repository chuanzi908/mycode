-- ============================================================
-- 实验二 EMP 员工管理 MIS 数据库初始化脚本
-- 用法：mysql -u root -p < sql/init.sql   （或在工作台整段执行）
-- 说明：
--   emp_id    自增主键
--   emp_name  姓名，建立普通索引，支持按姓名模糊查询
--   gender    性别，取值 男 / 女
--   dept      部门，分页接口的筛选条件之一
--   post      职位
--   salary    薪资，DECIMAL(10,2) 保留两位小数
--   hire_date 入职日期
--   status    1 在职 / 0 离职
-- 初始数据 5 条，覆盖研发、测试、人事三个部门
-- ============================================================
-- 实验二：EMP 员工管理 MIS 数据库初始化脚本
CREATE DATABASE IF NOT EXISTS ssm_emp DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;
USE ssm_emp;

DROP TABLE IF EXISTS emp;
CREATE TABLE emp (
    emp_id    INT PRIMARY KEY AUTO_INCREMENT COMMENT '员工编号',
    emp_name  VARCHAR(50)  NOT NULL COMMENT '姓名',
    gender    CHAR(1)      DEFAULT '男' COMMENT '性别',
    dept      VARCHAR(30)  COMMENT '部门',
    post      VARCHAR(30)  COMMENT '职位',
    salary    DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '薪资',
    hire_date DATE         COMMENT '入职日期',
    status    TINYINT      DEFAULT 1 COMMENT '1在职 0离职',
    KEY idx_emp_name (emp_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工表';

INSERT INTO emp (emp_name, gender, dept, post, salary, hire_date, status) VALUES
('张三', '男', '研发部', '后端工程师', 12000.00, '2023-03-01', 1),
('李四', '女', '研发部', '前端工程师', 11000.00, '2023-07-15', 1),
('王五', '男', '测试部', '测试工程师', 9000.00, '2022-11-20', 1),
('赵六', '女', '人事部', 'HR', 8000.00, '2021-05-10', 1),
('孙七', '男', '研发部', '架构师', 25000.00, '2020-01-06', 1);

