# day4-02MySQL事务

# 第一章 事务操作

```
tom 欠 jack 1000
设计一个页面,输入三个值,一个是付款人,一个是收款人,一个是转账的金额,不能出现付款人的钱被扣而收款人没收到钱的情况发生.而且要使用三层设计思想.
tom账户: 扣款 - 1000
jack账户: 收款 + 1000
```

**事务概述**

- 事务指的是逻辑上的一组操作,组成这组操作的各个单元要么全都成功,要么全都失败.
- 事务作用：保证在一个事务中多次SQL(增删改)操作要么全都成功,要么全都失败.

## 1.1 mysql事务操作

| sql语句           | 描述     |
| ----------------- | -------- |
| start transaction | 开启事务 |
| commit            | 提交事务 |
| rollback          | 回滚事务 |

- 准备数据

```mysql
# 创建一个表：账户表.
drop database if exists db04;
create database if not exists db04;
# 使用数据库
use db04;
# 创建账号表
drop table if exists account;
create table if not exists account (
	id int primary key auto_increment,
	name varchar(20),
	money double
);
# 初始化数据
insert into account values (null,'tom',10000);
insert into account values (null,'jack',10000);
```

- 操作
  - MYSQL中可以有两种方式进行事务的管理：
    - 自动提交：MySql默认自动提交。及执行一条sql语句提交一次事务。
    - 手动提交：先开启，再提交
- 方式1：手动提交

```mysql
start transaction;
update account set money=money-1000 where name='jack';
update account set money=money+1000 where name='tom';
commit;
#或者
rollback;
```

- 方式2：自动提交，通过修改mysql全局变量“autocommit”进行控制

```mysql
show variables like '%commit%';
* 设置自动提交的参数为OFF:
set autocommit = 0;  -- 0:OFF  1:ON
```

**演示**

```java
#查询所有记录
SELECT * FROM account;
#把字段money的值设置成10000
UPDATE account SET money=10000;
/*
	mysql默认事务管理机制:
	一条sql一个事务
	比如,执行tom-1000的update语句时,内部会自动开启事务,
	sql语句执行完毕,自动提交事务	
	但是: 以下两条sql,应该看成一个整体,要么全部执行,要么全都不执行,
		mysql默认事务管理机制就不合适了,需要手动进行事务管理		
		1.开启事务: begin  或者 start transaction
		2.提交事务: commit  把数据持久化到数据库
		3.回滚事务: rollback 把数据回退到开启事务之前的状态		
*/
#tom欠jerry1000元

#1.开启事务
BEGIN;

#tom-1000
UPDATE account SET money = money - 1000 WHERE NAME='tom';

#jerry+1000
UPDATE account SET money = money + 1000 WHERE NAME='jack';

#2.提交事务
COMMIT;

#3.回滚事务
ROLLBACK;
```


