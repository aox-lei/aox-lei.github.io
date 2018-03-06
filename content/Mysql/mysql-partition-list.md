title: Mysql 分区介绍(三) —— LIST分区
date: 2017-10-02
slug:mysql/mysql-partition-list
Tags: mysql分区, List分区, List Columns分区, 列分区, 数据库分区
Summary: LIST不同于RANGE分区, 每个分区必须被显式的定义, 每个分区是根据列值的成员在一组列表中的元素定义的

LIST不同于RANGE分区, 每个分区必须被显式的定义, 每个分区是根据列值的成员在一组列表中的元素定义的

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
PARTITION BY LIST(store_id) (
    PARTITION pNorth VALUES IN (3,5,6,9,17),
    PARTITION pEast VALUES IN (1,2,10,11,19,20),
    PARTITION pWest VALUES IN (4,12,13,14,18),
    PARTITION pCentral VALUES IN (7,8,15,16)
);
```

如果要删除一个分区的所有数据, 可以通过 ALTER TABLE员工表, TRUNCATE PARTITION pWest, 并且效率比DELETE高多了<br />

如果一次性写入多条数据, 在INNODB中, 会将这个认为是单个事务, 如果存在不符合的值, 则不会写入成功, 在MYSIAM中, 因为没有事务处理, 符合条件的值会写入, 不符合的会被抛弃。
