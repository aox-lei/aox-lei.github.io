title: Mysql 分区介绍(一) ——概述
date: 2017-10-02
slug:mysql/mysql-partition
Tags: mysql分区, mysql partition, mysql list分区, range分区, 子分区, hash分区, key分区
Summary: mysql分区类型介绍

## 一、分区类型
### 1. RANGE类型(范围分区)
> 通过范围的方式进行分区, 为每个分区给出一定的范围, 范围必须是连续的并且不能重复, 使用VALUES LESS THAN操作符

啥意思呢? 就是range类型就是一种范围, 比如, 从1-10, 11-20, 21-30这种的方式分区, 1-10就在一个分区里, 11-20是另外一个分区, 但是看起来他们还是同一个表 <br />

咱们看一个创建的例子
```
CREATE TABLE `t1` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL COMMENT '用户id',
  `score` int(3) NOT NULL DEFAULT '0' COMMENT '分数',
  PRIMARY KEY (`id`,`score`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (score)
(PARTITION p0 VALUES LESS THAN (10) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (20) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (30) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (40) ENGINE = InnoDB)
```

创建了个t1表, 并且t1有四个分区, 第一个分区p0的范围是小于10的, 第二个是小于20的。这就是一个range分区的例子。 <br />
`那为啥主键定义的是双主键呢?` 因为分区键(score) 必须也是主键或者唯一键的一部分。

Range分区的详细介绍请看[Mysql 分区介绍(二) —— RANGE分区](http://www.phpue.com/mysql/mysql-partition-range)

### 2. LIST分区
> LIST不同于RANGE分区, 每个分区必须被显式的定义, 每个分区是根据列值的成员在一组列表中的元素定义的

这说的有点乱, 还是直接看一个创建的例子吧

```
create table t2 (
	id int not null,
	uid int not null comment '用户id',
	score int(3) not null default 0 comment '分数',
	primary key(id, uid)
)
partition by list(uid) (
    partition p0 values in (1,3,5,7,9),
    partition p1 values in (2,4,6,8,10)
)
```

t2的分区键是uid, 有两个分区(这个很明显嘛), 如果uid in (1,3,5,7,9), 那么这条数据就会保存在p0中, 如果是2,4,6,8,10的话, 就会在p1中, 这就是LIST 分区

Range分区的详细介绍请看[Mysql 分区介绍(三) —— LIST分区](http://www.phpue.com/mysql/mysql-partition-list)

### 3. COLUMNS 分区
COLUMNS和以上两种是很不一样的, 这个是可以用多个分区键确定分区的。有两种方式, RANGE COLUMNS 和 LIST COLUMNS

#### 1. RANGE COLUMNS 分区
> 类似RANGE 分区, 但是可以使用一个或多个字段值定义

不太好理解... 还是看例子吧

```
create table t3 (
    a int,
    b int,
    c char(3),
    d int
)
PARTITION BY RANGE COLUMNS(a,d,c) (
PARTITION p0 VALUES LESS THAN (5,10,'ggg'),
PARTITION p1 VALUES LESS THAN (10,20,'mmm'),
PARTITION p2 VALUES LESS THAN (15,30,'sss')
)
```

分区键有多个, 并且都是范围的, 就是RANGE COLUMNS 分区

RANGE COLUMNS分区的详细介绍请看[Mysql 分区介绍(四) —— RANGE COLUMNS分区](http://www.phpue.com/mysql/mysql-partition-range-columns)

#### 2. LIST COLUMNS 分区
> Mysql 5.6开始支持LIST COLUMNS分区, 可以开始使用多个列作为分区的键, 并且列的数据类型除了数字类型可以作为分区列; 你也可以使用字符串类型, DATE和DATETIME

还是看例子吧
```
CREATE TABLE customers_1 (
    first_name VARCHAR(25),
    last_name VARCHAR(25),
    street_1 VARCHAR(30),
    street_2 VARCHAR(30),
    city VARCHAR(15),
    renewal DATE
)
PARTITION BY LIST COLUMNS(city) (
    PARTITION pRegion_1 VALUES IN('Oskarshamn', 'Högsby', 'Mönsterås'),
    PARTITION pRegion_2 VALUES IN('Vimmerby', 'Hultsfred', 'Västervik'),
    PARTITION pRegion_3 VALUES IN('Nässjö', 'Eksjö', 'Vetlanda'),
    PARTITION pRegion_4 VALUES IN('Uppvidinge', 'Alvesta', 'Växjo')
);
```

LIST COLUMNS分区的详细介绍请看[Mysql 分区介绍(五) —— LIST COLUMNS分区](http://www.phpue.com/mysql/mysql-partition-list-columns)

### 3. HASH分区
> 使用分区键去确保数据可以均匀的分布在一个预先确定数字的分区上, 在hash分区中, 无需显式的指定分区


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

HASH分区的详细介绍请看[Mysql 分区介绍(六) —— HASH分区](http://www.phpue.com/mysql/mysql-partition-hash)

### 4. KEY分区
> key分区类似hash分区, 接受0个或多个列名, key分区的哈希函数由MySQL服务器提供。NDB集群使用md5()；使用其他存储引擎的表，服务器采用自己的内部的哈希函数是基于相同的算法password()。

```
CREATE TABLE k1 (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(20)
)
PARTITION BY KEY()
PARTITIONS 2;
```

KEY分区的详细介绍请看[Mysql 分区介绍(七) —— KEY分区](http://www.phpue.com/mysql/mysql-partition-key)

### 5. 子分区
> 子分区也称为复合分区, 在分区的基础上进一步进行分区的方式

```
CREATE TABLE ts (
id INT, purchased DATE
)
PARTITION BY RANGE( YEAR(purchased) )
SUBPARTITION BY HASH( TO_DAYS(purchased) )
SUBPARTITIONS 2 (
    PARTITION p0 VALUES LESS THAN (1990),
    PARTITION p1 VALUES LESS THAN (2000),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);
```

子分区的详细介绍请看[Mysql 分区介绍(八) —— 子分区](http://www.phpue.com/mysql/mysql-partition-subpartition)
