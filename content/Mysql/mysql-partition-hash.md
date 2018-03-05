title: Mysql 分区介绍(六) —— HASH分区
date: 2017-10-02
slug:mysql/mysql-partition-hash

hash分区是使用主键去确保数据均匀分布在一个预先确定数字的分区上. 在range 或list分区中. 你必须显式的指定给出的数据写入哪个分区或设置一个列值去保存; 在hash分区中. Mysql已经为你准备的. 你只需要指定一个列的值或表达式基于列值去hash和分区的数字在哪个分区表中.

```
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)
PARTITION BY HASH(store_id)
PARTITIONS 4;
```

如果不包含PARTITIONS, 那么默认为1个分区

`使用日期分区`

```
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)
PARTITION BY HASH( YEAR(hired) )
PARTITIONS 4;
```

expr 必须是非恒量的数, 非随机的数, 就是数字是不同的, 但是是可以确定的。

如何确定一条数据的分区呢?先创建一个表
```
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

如果你插入一条记录到T1的col3值为“2005-09-15 '，然后分配其存储决定如下：

```
MOD(YEAR('2005-09-01'),4)
=  MOD(2005,4)
=  1
```

## 1. 线性hash分区
线性hash分区使用一个线性的2的幂运算法则
```
REATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)
PARTITION BY LINEAR HASH( YEAR(hired) )
PARTITIONS 4;
```

给定的一个表达式expr，分区中的记录存储在线性散列使用分区数n在Num的分区，其中n是根据下面的算法推导：
1. 发现大于2的数我们称这种价值V下的力量；它可以计算为：
```
V = POWER(2, CEILING(LOG(2, num)))
```
（假设数字为13）。然后LOG（2,13）是3.7004397181411。CEILING（3.7004397181411）是4，和V =功率（2,4），这是16。）

2. N = F(column_list) & (V - 1).
3. N >= num:

1. Set V = V / 2
2. Set N = N & (V - 1)

在线性哈希分区的好处是增加，下降，合并，拆分分区可以更快，有利于在处理含有非常大量的数据表（百万兆字节）。缺点是，与常规哈希分区获得的分布相比，分区之间不太可能均匀分布数据.
