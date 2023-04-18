mysql 是日常开发中比较常用的一种`关系型数据库`

以企业数据库表结构为例，讲解常用的查询语句；

- [建表 sql 下载](https://muyids.oss-cn-beijing.aliyuncs.com/blog/company.sql)
- [讲义下载](https://muyids.oss-cn-beijing.aliyuncs.com/blog/mysql%E9%9D%A2%E8%AF%95%E9%A2%98%E8%AE%B2%E4%B9%89.docx)

## 基本 SQL 操作

DDL\DML\DQL\TCL

## db

### 查看所有 db

show databases;

### 创建 db

create database company;

### 使用 db

use company;

### 查看库中表

show tables;

## table

### 建表

员工表

```sql
CREATE TABLE EMP
(
	EMPNO int(4) not null,
	ENAME VARCHAR(10),
	JOB VARCHAR(9),
	MGR INT(4) COMMENT "主管上级",
	HIREDATE DATE  DEFAULT NULL,
	SAL DOUBLE(7,2),
	COMM DOUBLE(7,2) COMMENT "补助",
	primary key (EMPNO),
	DEPTNO INT(2)
);
```

### 查看表结构

```sql
desc emp;
```

获取表字段信息：

```sql
select column_name from information_schema.COLUMNS where table_name='表名'
```

### 插入数据

```sql
INSERT INTO EMP (EMPNO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO )
VALUES ( 7369, 'SMITH', 'CLERK', 7902,  '1980-12-17', 800, NULL, 20);
```

### 查询语句

查询一个字段

```sql
select ename from emp;
```

查询多个字段

```sql
select e.empno, e.ename
from emp e;
```

查询所有字段

```sql
select * from emp;
```

计算

计算员工的年薪；列出员工的编号，姓名和年薪

```sql
select empno, ename, sal*12 as yearsal
from emp;
```

计算部门平均薪水；列出部门编号，部门名和平均薪水

```sql
select t.deptno,dept.dname, t.avgsal
from (select deptno, avg(sal) as avgsal
from emp
group by deptno) as t
join dept
on dept.deptno = t.deptno;
```

计算部门人数；列出部门编号，部门名和人数

```sql
select d.deptno, d.dname, t.pc
from (select deptno, count(distinct empno) as pc
from emp
group by deptno) as t
join dept as d
on t.deptno = d.deptno;
```

查找每个部门前三个工资最高的员工；列出部门编号，员工的编号，姓名和薪水 TODO

```sql
select e.deptno, e.empno, e.sal
from emp e
where (select count(*) from emp t where t.deptno=e.deptno and e.sal<t.sal) <3
order by e.deptno,e.sal desc;
```

条件查询

查询薪水大于 2000 的员工；列出员工编号，员工名，薪水

```sql
select empno,ename, sal
from emp
where sal > 2000;
```

查询薪水为 1600 和 3000 的员工；列出员工编号，员工名，薪水

```sql
select empno,ename,sal
from emp
where sal in(1600, 3000);
```

查询所有名字以 M 开头的员工；列出员工名

```sql
select ename
from emp
where ename like "M%";
```

查询姓名中第二个字符为 A 的所有员工；列出员工名

```sql
select ename
from emp
where ename like "_A%";
```

排序

按工资从高到低排序,相同工资按入职时间先后排序；列出员工编号，员工名，薪水,入职时间

```sql
select empno,ename,sal,hiredate
from emp
order by sal desc, hiredate asc;
```

### 聚合函数

查找工资总和，平均工资，工资最大值，工资最小值，员工总数

```sql
select sum(sal),avg(sal),max(sal),min(sal),count(distinct empno)
from emp;
```

查找所有工资高于平均工资的员工；列出员工名，薪水

```sql
select t.avgsal,e.ename,e.sal
from emp e
join (select avg(sal) as avgsal
from emp) t
where e.sal>t.avgsal;
```

分组查询`group by`

查找每个部门里所有工资高于部门平均工资的员工；列出部门编号，部门平均工资，员工名，薪水

```sql
select e.deptno,t.avgsal,e.ename,e.sal
from emp e
join (select deptno,avg(sal) as avgsal
from emp
group by deptno) t
on e.deptno=t.deptno
where e.sal>t.avgsal;
```

计算不同部门的最高薪水；列出部门编号，最高薪水

```sql
select deptno, max(sal) as maxsal
from emp
group by deptno;
```

计算不同部门不同岗位的最高薪水；列出部门编号，岗位，最高薪水

```sql
select deptno, job, max(sal) as maxsal
from emp
group by deptno, job;
```

计算不同部门不同岗位除 manager 岗的最高薪水；列出部门编号，岗位，最高薪水

```sql
select deptno, job, max(sal) as maxsal
from emp
where job <>"manager"
group by deptno, job;
```

分组条件查询`group by + having`

- where 是在 group by 之前完成过滤
- having 是在 group by 之后完成过滤
  计算平均工资高于 2000 的岗位;列出岗位名，平均工资

```sql
select job, avg(sal) as avgsal
from emp
group by job
having avgsal>2000;
```

### 多表查询

笛卡尔积

含义：若两张表进行连接查询的时候没有任何条件限制，最终的查询结果总数是两张表记录的乘积，该现在称为笛卡尔积现象。

当多张表进行连接查询时，若没有任何条件限制，会发生什么现象？

左连接：保留左边全部行
右连接：保留右边全部行
全连接：左右两边都保留

查询员工所在部门名称；列出员工名，部门名

```sql
select ename,dname
from emp,dept
where emp.deptno=dept.deptno;
```

使用`join on`,join tableName on 限制条件，inner 关键字省略，默认 join 都是内连接

```sql
select ename,dname
from emp join dept on emp.deptno=dept.deptno;
```

查询员工的工资等级，按工资等级由高到低排序；列出员工名，工资等级

```sql
select e.ename, s.grade
from emp e join salgrade s on e.sal >= s.losal and e.sal <=s.hisal
order by s.grade desc;
```

查询员工的上级领导；列出员工名，领导名

```sql
select e.ename, m.ename
from emp e left join emp m on e.mgr=m.empno;
```

找出每一个员工对应的部门名称，以及该员工对应的工资等级;要求显示员工姓名、部门名、工资等级

```sql
select e.ename, d.dname, g.grade
from emp e
  join dept d on e.deptno=d.deptno
  join salgrade g on e.sal>=g.losal and e.sal<=g.hisal;
```

### 子查询

select 语句嵌套 select 语句被称为子查询；

select 子句可出现在 select、from、where 关键字后面，如下：

- select … (select)…
- from …(select)…
- where …(select)…

where 语句后的子查询

找出比平均工资高的员工；

```sql
select ename
from emp
where sal > (select avg(sal) from emp);
```

from 语句后的子查询

找出每个部门的平均薪水，并且要求显示平均薪水的薪水等级；

```sql
select deptno, avgsal, grade
from (
  select deptno, avg(sal) as avgsal
  from emp
  group by deptno
  ) a join salgrade g on a.avgsal>=g.losal and a.avgsal<=g.hisal;
order by deptno asc;
```

limit 关键字

找出工资前五的员工；

```sql
select ename
from emp
order by sal desc
limit 5;
```

找出工资排名在 2-9 的员工

```sql
select ename
from emp
order by sal desc
limit 2,7;
```
