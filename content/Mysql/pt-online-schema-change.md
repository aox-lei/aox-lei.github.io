title: pt-online-schema-change 在线修改表结构
date: 2017-11-01
slug: mysql/pt-online-schema-change
Tags: pt-online-schema-change, percona-toolkit, mysql在线修改表结构操作
Summary: pt-online-schema-change可以在不影响正常业务的情况下, 对数据库表结构进行修改, 修改的速度根据数据量大小决定。是一个很值得学习的工具

## 1. 参数
|参数|默认值|说明|
|-|-|-|
|--host=xxx --user=xxx --password=xxx | | 连接实例信息，缩写-h xxx -u xxx -p xxx，密码可以使用参数--ask-pass 手动输入。|
|--alter| | 结构变更语句，不需要 ALTER TABLE关键字。与原始ddl一样可以指定多个更改，用逗号分隔。|
|D=db_name,t=table_name||指定要ddl的数据库名和表名|
|--max-load||默认为Threads_running=25。每个chunk拷贝完后，会检查 SHOW GLOBAL STATUS 的内容，检查指标是否超过了指定的阈值。如果超过，则先暂停。这里可以用逗号分隔，指定多个条件，每个条件格式： status指标=MAX_VALUE或者status指标:MAX_VALUE。如果不指定MAX_VALUE，那么工具会这只其为当前值的120%。|
|--max-lag | | 默认1s。每个chunk拷贝完成后，会查看所有复制Slave的延迟情况（Seconds_Behind_Master）。要是延迟大于该值，则暂停复制数据，直到所有从的滞后小于这个值。--check-interval配合使用，指定出现从库滞后超过 max-lag，则该工具将睡眠多长时间，默认1s，再检查。如--max-lag=5 --check-interval=2。|
|--chunk-time | | 默认0.5s，即拷贝数据行的时候，为了尽量保证0.5s内拷完一个chunk，动态调整chunk-size的大小，以适应服务器性能的变化。|
|--set-vars | | 使用pt-osc进行ddl要开一个session去操作，set-vars可以在执行alter之前设定这些变量，比如默认会设置--set-vars "wait_timeout=10000,innodb_lock_wait_timeout=1,lock_wait_timeout=60"。|
|--dry-run | | 创建和修改新表，但不会创建触发器、复制数据、和替换原表。并不真正执行，可以看到生成的执行语句，了解其执行步骤与细节，和--print配合最佳。。|
| --execute | |确定修改表，则指定该参数。真正执行alter。–dry-run与–execute必须指定一个，二者相互排斥|

### 1. --alter说明
1.绝大部分情况下表上需要有主键或唯一索引，因为工具在运行当中为了保证新表也是最新的，需要旧表上创建 DELETE和UPDATE 触发器，同步到新表的时候有主键会更快。个别情况是，当alter操作就是在c1列上建立主键时，DELETE触发器将基于c1列。
2. 子句不支持 rename 去给表重命名。
3. alter命令原表就不支持给索引重命名，需要先drop再add，在pt-osc也一样。(mysql 5.7 支持 RENAME INDEX old_index_name TO new_index_name)。但给字段重命名，千万不要drop-add，整列数据会丢失，使用change col1 col1_new type constraint（保持类型和约束一致，否则相当于修改 column type，不能online）
4. 子句如果是add column并且定义了not null，那么必须指定default值，否则会失败。
5. 如果要删除外键（名 fk_foo），使用工具的时候外键名要加下划线，比如--alter "DROP FOREIGN KEY _fk_foo"

## 2. 使用限制
1. 原表上不能有触发器存在
2. 在使用之前需要对磁盘容量进行评估。因为数据量会多一倍

## 3. 使用示例
### 1. 添加字段
```
pt-online-schema-change --user=user --password=password --host=10.0.201.34  --alter "ADD COLUMN f_id int default 0" D=confluence,t=sbtest3 --print --execute
```
