title: Mysql 分区介绍(七) —— KEY分区
date: 2017-10-02
slug:mysql/mysql-partition-key

Key分区和HASH分区非常类似。它们主要的区别在于:

1. Key分区默认使用主键作为分区键
2. key分区只接受一个列表的零个或多个列名。任何用作分区键的列都必须包含表主键的一部分或全部，如果表有一个。如果没有指定列名为分区键，则使用表主键。

```
CREATE TABLE k1 (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(20)
)
PARTITION BY KEY()
PARTITIONS 2;
```
