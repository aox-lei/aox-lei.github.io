title: Mysql主从配置
date: 2017-12-01
slug: mysql/mysql-sync
Tags: mysql主从配置, mysql读写分离
Summary: Mysql主从可以方便的实现数据的自动备份, 实现数据库的扩展, 并且可以使读写分离, 减轻数据库压力。

Mysql主从可以方便的实现数据的自动备份, 实现数据库的扩展, 并且可以使读写分离, 减轻数据库压力。

## 主从复制原理
从库生成两个线程，一个I/O线程，一个SQL线程；

i/o线程去请求主库 的binlog，并将得到的binlog日志写到relay log（中继日志） 文件中；
主库会生成一个 log dump 线程，用来给从库 i/o线程传binlog；

SQL 线程，会读取relay log文件中的日志，并解析成具体操作，来实现主从的操作一致，而最终数据一致；

## 一、准备工作
1. 主从的数据库最好一致
2. 主从的数据库内部数据结构最好一致

主数据库地址: 10.211.55.9
从数据库地址: 10.211.55.10

## 二、主数据库的配置
### 1. 修改mysql配置, 开启binlog
```
[mysqld]
log-bin=mysql-bin #开启二进制日志
server-id=1 #设置server-id
```

`server_id的作用`
1. server_id标识语句是由哪个server产生的
2. 如果两个slave具有相同的server_id, 那么最后一个会被踢掉。如果执行了slave stop, maser上的线程并不会退出, 在执行slave start后, 会直接进行连接。
3. 如果主主同步构成一个环状, 就要保证数据不同不进入死循环, 就需要靠server_id来实现。

### 2. 重启mysql并创建同步账号
```
mysql> CREATE USER 'sync'@'%' IDENTIFIED BY 'slavepass';#创建用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'sync'@'%';#分配权限
mysql>flush privileges;   #刷新权限
```

### 3. 查看master状态并记录binlog文件位置
```
mysql > SHOW MASTER STATUS;
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000001 | 5524     |              |                  |
+------------------+----------+--------------+------------------+
```

## 三、从服务器设置
### 1. 修改配置
经测试, 从服务器不需要开启binlog也可以同步
```
[mysqld]
server-id=2 #设置server-id，必须唯一
```

### 2. 指定主库
```
mysql> CHANGE MASTER TO
    ->     MASTER_HOST='10.211.155.9',
    ->     MASTER_USER='sync',
    ->     MASTER_PASSWORD='123123',
    ->     MASTER_LOG_FILE='mysql-bin.000001',
    ->     MASTER_LOG_POS=5524;
```

### 3. 开始同步
```
start slave;
```

### 4. 查看slave状态
```
***************************[ 1. row ]***************************
Slave_IO_State                | Waiting for master to send event
Master_Host                   | 10.211.55.9
Master_User                   | sync
Master_Port                   | 3306
Connect_Retry                 | 60
Master_Log_File               | mysql-bin.000001
Read_Master_Log_Pos           | 7071
Relay_Log_File                | lin-Parallels-Virtual-Platform-relay-bin.000004
Relay_Log_Pos                 | 588
Relay_Master_Log_File         | mysql-bin.000001
Slave_IO_Running              | Yes
Slave_SQL_Running             | Yes
Replicate_Do_DB               |
Replicate_Ignore_DB           |
Replicate_Do_Table            |
Replicate_Ignore_Table        |
Replicate_Wild_Do_Table       |
Replicate_Wild_Ignore_Table   |
Last_Errno                    | 0
Last_Error                    |
Skip_Counter                  | 0
Exec_Master_Log_Pos           | 7071
Relay_Log_Space               | 786
Until_Condition               | None
Until_Log_File                |
Until_Log_Pos                 | 0
```

Slave_IO_Running和Slave_SQL_Running 是Yes 则代表同步正常
如果发生错误, 可以查看以下参数排查问题。
```
Last_IO_Errno                 | 0
Last_IO_Error                 |
Last_SQL_Errno                | 0
Last_SQL_Error                |
Slave_SQL_Running_State       | Slave has read all relay log; waiting for the slave I/O thread to update it
```

## 四、mysql主从复制方案

### 1. 异步复制（Asynchronous replication）
MySQL默认的复制即是异步的，主库在执行完客户端提交的事务后会立即将结果返给给客户端，并不关心从库是否已经接收并处理，这样就会有一个问题，主如果crash掉了，此时主上已经提交的事务可能并没有传到从上，如果此时，强行将从提升为主，可能导致新主上的数据不完整。

### 2. 全同步复制（Fully synchronous replication）
指当主库执行完一个事务，所有的从库都执行了该事务才返回给客户端。因为需要等待所有从库执行完该事务才能返回，所以全同步复制的性能必然会收到严重的影响。

### 3. 半同步复制（Semisynchronous replication）
介于异步复制和全同步复制之间，主库在执行完客户端提交的事务后不是立刻返回给客户端，而是等待至少一个从库接收到并写到relay log中才返回给客户端。相对于异步复制，半同步复制提高了数据的安全性，同时它也造成了一定程度的延迟，这个延迟最少是一个TCP/IP往返的时间。所以，半同步复制最好在低延时的网络中使用。

**存在的问题**:
1. 事务还没发送到从库上
此时，客户端会收到事务提交失败的信息，客户端会重新提交该事务到新的主上，当宕机的主库重新启动后，以从库的身份重新加入到该主从结构中，会发现，该事务在从库中被提交了两次，一次是之前作为主的时候，一次是被新主同步过来的
2. 事务已经发送到从库上
此时，从库已经收到并应用了该事务，但是客户端仍然会收到事务提交失败的信息，重新提交该事务到新的主上。
