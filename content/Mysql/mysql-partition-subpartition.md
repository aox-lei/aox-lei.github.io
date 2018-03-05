title: Mysql 分区介绍(八) —— 子分区
date: 2017-10-02
slug:mysql/mysql-partition-subpartition

分区也被称为复合分区在分区表中每个分区的进一步划分。子分区也必须是hash分区/key分区

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

表TS有3个范围分区。这些partitions-p0，P1和P2，进一步划分为2个子。实际上，整个表被划分为3×2＝6个分区。然而，由于分区子句的作用，这些存储的前2个仅在列中的值小于1990的那些记录中存储。

**需要注意的是**:
1. 每个分区必须有相同数量的子分区。
2. 子分区的名称必须在整个表中是唯一的

`为每个分区指定单独的磁盘`
```
CREATE TABLE ts (id INT, purchased DATE)
    ENGINE = MYISAM
    PARTITION BY RANGE(YEAR(purchased))
    SUBPARTITION BY HASH( TO_DAYS(purchased) ) (
        PARTITION p0 VALUES LESS THAN (1990) (
            SUBPARTITION s0a
                DATA DIRECTORY = '/disk0'
                INDEX DIRECTORY = '/disk1',
            SUBPARTITION s0b
                DATA DIRECTORY = '/disk2'
                INDEX DIRECTORY = '/disk3'
        ),
        PARTITION p1 VALUES LESS THAN (2000) (
            SUBPARTITION s1a
                DATA DIRECTORY = '/disk4/data'
                INDEX DIRECTORY = '/disk4/idx',
            SUBPARTITION s1b
                DATA DIRECTORY = '/disk5/data'
                INDEX DIRECTORY = '/disk5/idx'
        ),
        PARTITION p2 VALUES LESS THAN MAXVALUE (
            SUBPARTITION s2a,
            SUBPARTITION s2b
        )
    );
```
