# day4-03MySQL做作业&刷题

https://leetcode.cn/studyplan/sql-free-50/
（先做作业后刷题）

## 第一套题目：初级（初级：DDL+DML+单表基础查询）
业务场景：开发一个“员工信息管理表”，用于保存公司员工的基础资料，并完成最基本的增删改查操作。

```java
create database company_db;
use company_db;
show databases;
create table emp(
    id int primary key auto_increment,
    name varchar(255) not null,
    gender char(1),
    age int,
    dept varchar(20),
    salary decimal(10,2),
    entry_date date
);

insert into emp(id,name,gender,age,dept,salary,entry_date) values (1,'小李','男',28,'研发部',10000,'2026-10-01');

insert into emp(id,name,gender,age,dept,salary,entry_date) values (2,'小张','男',32,'销售部',7000,'2026-08-01');

insert into emp(id,name,gender,age,dept,salary,entry_date) values (3,'小陈','男',24,'技术部',10000,'2026-07-01');

insert into emp(id,name,gender,age,dept,salary,entry_date) values (4,'小刘','男',38,'研发部',25000,'2026-03-01');

insert into emp(id,name,gender,age,dept,salary,entry_date) values (5,'小花','女',26,'销售部',12000,'2026-10-01');

update emp set dept='研发部' where id=5;
update emp set salary = salary + 1000 where id=5;

delete from emp where id=5;

select * from emp;
select * from emp where dept='研发部';
select * from emp where salary > 8000;
select * from emp where name like '%张%';
select * from emp order by salary DESC;

```

## 第二套题目：中级（高级DQL：排序+聚合+分组+分页）
业务场景：开发一个“订单统计分析功能”，用于查看订单数据的整体情况、分类统计结果以及分页展示效果。

```java
create table orders(
    id int primary key auto_increment,
    customer_name varchar(255) not null,
    category varchar(255),
    amount decimal(10,2),
    status varchar(20),
    create_time datetime  
);

INSERT INTO orders (customer_name, category, amount, status, create_time) VALUES 
('张三', '数码', 5999.00, '已支付', '2026-10-01 10:30:00'),
('李四', '服饰', 299.50, '未支付', '2026-10-02 14:15:00'),
('王五', '食品', 89.90, '已取消', '2026-10-03 09:00:00'),
('赵六', '家居', 1200.00, '已支付', '2026-10-04 18:20:00'),
('孙七', '数码', 129.00, '未支付', '2026-10-05 11:45:00'),
('周八', '服饰', 450.00, '已支付', '2026-10-06 16:10:00'),
('吴九', '食品', 45.00, '已支付', '2026-10-07 08:30:00'),
('郑十', '家居', 3500.00, '已取消', '2026-10-08 20:00:00');

select count(*) from orders;
select sum(amount) from orders where status='已支付';
select category,count(*),sum(amount) from orders group by category;
select category,sum(amount) from orders group by category having sum(amount) > 1000;
select * from orders order by amount DESC limit 3;
//这里主要是这个分页查询的offset关键字不是很熟悉
select * from orders order by id ASC limit 3 offset 3;
```

## 第三套题目：中高级（多表关系 + 多表查询）
业务场景：开发一个“学生选课系统”，学生可以选择多门课程，一门课程也可以被多个学生选择。现在需要完成表设计和多表查询。

```java
-- 1. 学生表
CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT
);

-- 2. 课程表
CREATE TABLE course (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(50) NOT NULL,
    teacher_name VARCHAR(50)
);

-- 3. 选课关系表
CREATE TABLE student_course (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT
);


-- 插入 3 个学生
INSERT INTO student (name, age) VALUES 
('张三', 20), 
('李四', 21), 
('王五', 22);

-- 插入 3 门课程
INSERT INTO course (course_name, teacher_name) VALUES 
('数据库原理', '刘老师'), 
('Java编程', '陈老师'), 
('高等数学', '杨老师');

-- 插入 5 条选课关系 (张三选了2门，李四选了2门，王五选了1门)
INSERT INTO student_course (student_id, course_id) VALUES 
(1, 1), -- 张三 选 数据库原理
(1, 2), -- 张三 选 Java编程
(2, 1), -- 李四 选 数据库原理
(2, 3), -- 李四 选 高等数学
(3, 2); -- 王五 选 Java编程


SELECT s.name AS 学生姓名, c.course_name AS 课程名称
FROM student s
INNER JOIN student_course sc ON s.id = sc.student_id
INNER JOIN course c ON sc.course_id = c.id;

SELECT s.id, s.name AS 学生姓名, s.age, c.course_name AS 课程名称
FROM student s
LEFT JOIN student_course sc ON s.id = sc.student_id
LEFT JOIN course c ON sc.course_id = c.id;

SELECT c.course_name AS 课程名称, COUNT(sc.student_id) AS 选课人数
FROM course c
LEFT JOIN student_course sc ON c.id = sc.course_id
GROUP BY c.id, c.course_name
ORDER BY 选课人数 DESC;

SELECT c.course_name AS 课程名称, c.teacher_name AS 授课教师
FROM student s
INNER JOIN student_course sc ON s.id = sc.student_id
INNER JOIN course c ON sc.course_id = c.id
WHERE s.name = '张三';

SELECT c.course_name AS 课程名称
FROM course c
LEFT JOIN student_course sc ON c.id = sc.course_id
WHERE sc.id IS NULL;
```

