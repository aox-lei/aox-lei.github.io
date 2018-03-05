title: Mysql 分区介绍(九) —— 分区管理
date: 2017-10-02
slug:mysql/mysql-partition-manage

## 一、分区操作
#### 1. 将没有分区的表改为分区表
```
ALTER TABLE trb3 PARTITION BY KEY(id) PARTITIONS 2;
```

#### 2. 删除分区
```
# 删除所有分区, 同时数据丢失
ALTER TABLE es2 REMOVE PARTITIONING;

# 删除指定分区, 数据丢失
ALTER TABLE tr DROP PARTITION p2;
```

#### 3. SELECT指定分区查询
```
select * from daily_rank_1_1 partition (p2015_04_24) limit 10;
```

#### 4. 添加分区
如果设置了MAXVALUE则无法添加新分区, 会提示 MAXVALUE can only be used in last partition definition, 这时可以使用修改分区来解决
```
ALTER TABLE members ADD PARTITION (PARTITION p3 VALUES LESS THAN (2010));
```

#### 5. 重新划分分区
```
ALTER TABLE table1 REORGANIZE PARTITION 要修改的分区名(可以多个, 逗号分隔) INTO (
    PARTITION 新分区1的名字 VALUES LESS THAN (值),
    PARTITION 新分区2的名字 VALUES LESS THAN (值)
    ...
)
```

修改一个分区成两个分区
```
alter table daily_rank_1_1 reorganize partition p2015_04_28 into(
partition p2015_04_28 values less than (to_days('2015-04-28')),
partition pmax values less than(MAXVALUE)
);
```

重新划分多个分区
```
ALTER TABLE members REORGANIZE PARTITION p0,p1,p2,p3 INTO (
    PARTITION m0 VALUES LESS THAN (1980),
    PARTITION m1 VALUES LESS THAN (2000)
);
```

`分区修改的原则`:<br />
- 1. 不能与原方案有重叠
- 2. 同时对多个分区划分必须是连续的分区
- 3. 分区类型不可以更改, 可以通过ALTER TABLE ... PARTITION BY ...实现

#### 6. 修改分区数量(HASH/Key分区)
```
ALTER TABLE clients COALESCE PARTITION 4;
```

## 二、交换分区和子分区
`支持交换分区的条件`
- 1. 表自身不是分区表
- 2. 不是临时表
- 3. 两个表的结构相同
- 4. 表不包含外键
- 5. 表的数据没有出界

如果要执行操作, 必须具有DROP权限<br />
- 1.  执行 ALTER TABLE ... EXCHANGE PARTITION不会在分区表或交换表上调用任何触发器
- 2. auto_increment会发生重置

具体操作:
pt是分区表, p是分区或子分区

#### 1. 与非分区表交换分区
```
CREATE TABLE e (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30)
)
    PARTITION BY RANGE (id) (
        PARTITION p0 VALUES LESS THAN (50),
        PARTITION p1 VALUES LESS THAN (100),
        PARTITION p2 VALUES LESS THAN (150),
        PARTITION p3 VALUES LESS THAN (MAXVALUE)
);
INSERT INTO e VALUES
    (1669, "Jim", "Smith"),
    (337, "Mary", "Jones"),
    (16, "Frank", "White"),
    (2005, "Linda", "Black");
mysql> CREATE TABLE e2 LIKE e;
Query OK, 0 rows affected (1.34 sec)
mysql> ALTER TABLE e2 REMOVE PARTITIONING;
Query OK, 0 rows affected (0.90 sec)
Records: 0  Duplicates: 0  Warnings: 0
# 将p0分区的数据写入e2
ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2;
```
如果没有匹配到数据, 则提示Found row that does not match the partition
#### 2. 交换一个子分区到一个没有分区的表

```
mysql> CREATE TABLE es (
    ->     id INT NOT NULL,
    ->     fname VARCHAR(30),
    ->     lname VARCHAR(30)
    -> )
    ->     PARTITION BY RANGE (id)
    ->     SUBPARTITION BY KEY (lname)
    ->     SUBPARTITIONS 2 (
    ->         PARTITION p0 VALUES LESS THAN (50),
    ->         PARTITION p1 VALUES LESS THAN (100),
    ->         PARTITION p2 VALUES LESS THAN (150),
    ->         PARTITION p3 VALUES LESS THAN (MAXVALUE)
    ->     );
Query OK, 0 rows affected (2.76 sec)
mysql> INSERT INTO es VALUES
    ->     (1669, "Jim", "Smith"),
    ->     (337, "Mary", "Jones"),
    ->     (16, "Frank", "White"),
    ->     (2005, "Linda", "Black");
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0
mysql> CREATE TABLE es2 LIKE es;
Query OK, 0 rows affected (1.27 sec)
mysql> ALTER TABLE es2 REMOVE PARTITIONING;
Query OK, 0 rows affected (0.70 sec)
Records: 0  Duplicates: 0  Warnings: 0
# 将p3sp0的数据交换到es2表
mysql> ALTER TABLE es EXCHANGE PARTITION p3sp0 WITH TABLE es2;
Query OK, 0 rows affected (0.29 sec)
```

如果一个表拥有子分区, 则不能移动这个父分区到表中
## 三、分区维护
1. 重建分区
删除所有记录存储在分区，然后重新插入它们。整理碎片
```
ALTER TABLE t1 REBUILD PARTITION p0, p1;
```

2. 优化分区
优化分区来回收未使用的空间和整理的分区中的数据文件
```
ALTER TABLE t1 OPTIMIZE PARTITION p0, p1;
```

3. 分析分区

```
ALTER TABLE t1 ANALYZE PARTITION p3;
```

4. 检查分区
```
ALTER TABLE trb3 CHECK PARTITION p1;
```

5. 修复分区
```
ALTER TABLE t1 REPAIR PARTITION p0,p1;
```

6. 获取分区有效信息
```
mysql> SHOW CREATE TABLE trb3\G
*************************** 1. row ***************************
       Table: trb3
Create Table: CREATE TABLE `trb3` (
  `id` int(11) default NULL,
  `name` varchar(50) default NULL,
  `purchased` date default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1
PARTITION BY RANGE (YEAR(purchased)) (
  PARTITION p0 VALUES LESS THAN (1990) ENGINE = MyISAM,
  PARTITION p1 VALUES LESS THAN (1995) ENGINE = MyISAM,
  PARTITION p2 VALUES LESS THAN (2000) ENGINE = MyISAM,
  PARTITION p3 VALUES LESS THAN (2005) ENGINE = MyISAM
)
1 row in set (0.00 sec)
```

```
select *
from INFORMATION_SCHEMA.PARTITIONS
```
## 四、分区修剪
在执行sql时, 优化器会自动根据分区的条件, 进行分区选择来提高性能。

`分区修剪的条件`: <br />
- 1. partition_column = constant
- 2. partition_column IN (constant1, constant2, ..., constantN)
where条件中包含<，>，< =，> =，和< > 等之间范围查询的时候, 就可以使用分区修剪
SELECT、UPDATE和DELETE都可以修剪分区, 但是INSERT无法修剪分区

## 五、分区选择
在执行操作的时候优化器会根据语句自动进行修剪, 但是在有些时候是不同的:
1. 要检查的分区由语句的发布者指定，与分区剪枝不同，它是自动的。
2. 而分区修剪仅适用于查询，分区明确的选择是查询和多个DML语句支持。
支持的语句: SELECT、DELETE、INSERT、REPLACE、UPDATE、LOAD DATA.、LOAD XML.

具体的语句:
```
      PARTITION (partition_names)

      partition_names:
          partition_name, ...
```

```
SELECT * FROM employees PARTITION (p1);

mysql> SELECT * FROM employees PARTITION (p0, p2)
    ->     WHERE lname LIKE 'S%';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
|  4 | Jim   | Smith |        2 |             4 |
| 11 | Jill  | Stone |        1 |             4 |
+----+-------+-------+----------+---------------+
2 rows in set (0.00 sec)

mysql> SELECT id, CONCAT(fname, ' ', lname) AS name
    ->     FROM employees PARTITION (p0) ORDER BY lname;
+----+----------------+
| id | name           |
+----+----------------+
|  3 | Ellen Johnson  |
|  4 | Jim Smith      |
|  1 | Bob Taylor     |
|  2 | Frank Williams |
+----+----------------+
4 rows in set (0.06 sec)

mysql> SELECT store_id, COUNT(department_id) AS c
    ->     FROM employees PARTITION (p1,p2,p3)
    ->     GROUP BY store_id HAVING c > 4;
+---+----------+
| c | store_id |
+---+----------+
| 5 |        2 |
| 5 |        3 |
+---+----------+
2 rows in set (0.00 sec)
```

你也可以使用PARTITION 在INSERT...SELECT语句上
```
mysql> CREATE TABLE employees_copy LIKE employees;
Query OK, 0 rows affected (0.28 sec)

mysql> INSERT INTO employees_copy
    ->     SELECT * FROM employees PARTITION (p2);
Query OK, 5 rows affected (0.04 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM employees_copy;
+----+--------+----------+----------+---------------+
| id | fname  | lname    | store_id | department_id |
+----+--------+----------+----------+---------------+
| 10 | Lou    | Waters   |        2 |             4 |
| 11 | Jill   | Stone    |        1 |             4 |
| 12 | Roger  | White    |        3 |             2 |
| 13 | Howard | Andrews  |        1 |             2 |
| 14 | Fred   | Goldberg |        3 |             3 |
+----+--------+----------+----------+---------------+
5 rows in set (0.00 sec)
```

也可以在联表中使用
```
CREATE TABLE stores (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(30) NOT NULL
)
    PARTITION BY HASH(id)
    PARTITIONS 2;

INSERT INTO stores VALUES
    ('', 'Nambucca'), ('', 'Uranga'),
    ('', 'Bellingen'), ('', 'Grafton');

CREATE TABLE departments  (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL
)
    PARTITION BY KEY(id)
    PARTITIONS 2;

INSERT INTO departments VALUES
    ('', 'Sales'), ('', 'Customer Service'),
    ('', 'Delivery'), ('', 'Accounting');

mysql> SELECT
    ->     e.id AS 'Employee ID', CONCAT(e.fname, ' ', e.lname) AS Name,
    ->     s.city AS City, d.name AS department
    -> FROM employees AS e
    ->     JOIN stores PARTITION (p1) AS s ON e.store_id=s.id
    ->     JOIN departments PARTITION (p0) AS d ON e.department_id=d.id
    -> ORDER BY e.lname;
+-------------+---------------+-----------+------------+
| Employee ID | Name          | City      | department |
+-------------+---------------+-----------+------------+
|          14 | Fred Goldberg | Bellingen | Delivery   |
|           5 | Mary Jones    | Nambucca  | Sales      |
|          17 | Mark Morgan   | Bellingen | Delivery   |
|           9 | Andy Smith    | Nambucca  | Delivery   |
|           8 | June Wilson   | Bellingen | Sales      |
+-------------+---------------+-----------+------------+
5 rows in set (0.00 sec)
```

删除中使用分区选择
```
mysql> SELECT * FROM employees WHERE fname LIKE 'j%';
+----+-------+--------+----------+---------------+
| id | fname | lname  | store_id | department_id |
+----+-------+--------+----------+---------------+
|  4 | Jim   | Smith  |        2 |             4 |
|  8 | June  | Wilson |        3 |             1 |
| 11 | Jill  | Stone  |        1 |             4 |
+----+-------+--------+----------+---------------+
3 rows in set (0.00 sec)

mysql> DELETE FROM employees PARTITION (p0, p1)
    ->     WHERE fname LIKE 'j%';
Query OK, 2 rows affected (0.09 sec)

mysql> SELECT * FROM employees WHERE fname LIKE 'j%';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill  | Stone |        1 |             4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)
```

更新中使用分区选择
```
mysql> UPDATE employees PARTITION (p0)
    ->     SET store_id = 2 WHERE fname = 'Jill';
Query OK, 0 rows affected (0.00 sec)
Rows matched: 0  Changed: 0  Warnings: 0

mysql> SELECT * FROM employees WHERE fname = 'Jill';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill  | Stone |        1 |             4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)

mysql> UPDATE employees PARTITION (p2)
    ->     SET store_id = 2 WHERE fname = 'Jill';
Query OK, 1 row affected (0.09 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT * FROM employees WHERE fname = 'Jill';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill  | Stone |        2 |             4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)
```

INSERT和REPLACE INTO使用分区选择
```
mysql> INSERT INTO employees PARTITION (p2) VALUES (20, 'Jan', 'Jones', 1, 3);
ERROR 1729 (HY000): Found a row not matching the given partition set
mysql> INSERT INTO employees PARTITION (p3) VALUES (20, 'Jan', 'Jones', 1, 3);
Query OK, 1 row affected (0.07 sec)

mysql> REPLACE INTO employees PARTITION (p0) VALUES (20, 'Jan', 'Jones', 3, 2);
ERROR 1729 (HY000): Found a row not matching the given partition set

mysql> REPLACE INTO employees PARTITION (p3) VALUES (20, 'Jan', 'Jones', 3, 2);
Query OK, 2 rows affected (0.09 sec)
```

## 六、分区的限制
- 1. 无法使用存储过程、存储功能、UDF和插件
- 2. 无法用户变量或声明变量
- 3. 不允许位操作

## 七、性能影响
- 1. 分区的创建、修改、删除取决于文件系统。应该确保large_files_support启用，open_files_limit设置正确
- 2. 在执行分区操作时需要上写锁, 但是不影响查询, 分区操作完成后会立即执行插入和更新操作
- 3. 分区操作， 查询、更新往往是MYISAM比INNODB更快
- 4. 使用索引可以在非分区表提高性能, 使用分区修剪也可以显著的提高性能
- 5. 加载数据使用缓冲来提高性能。您应该知道缓冲区每分区使用130KB内存来实现这一点。
- 6. Mysql5.6.7之前, 分区最大数为1024个, 从5.6.7开始, 分区表的数最多是8192个, 包括子分区
- 7. 分区表不支持查询缓存
