title: Mycat基本使用教程
date: 2017-12-02
slug: mysql/mycat-2
Tags: mycat, mycat教程, 数据库中间件
Summary: 在完成mycat安装后, 我们开始一个示例来尽快熟悉mycat

在完成mycat安装后, 开始一个示例来尽快熟悉mycat

## 一、环境说明
### 1. 服务器说明
|服务器名称|地址|说明|
| - | - | - |
| mycat服务器 | 10.211.55.13 | mycat中间件服务器 |
| mysql服务器 | 10.211.55.9 | mysql服务器 |


### 2. mysql 库和表说明
|库名称|说明|
| - | - |
| db01 | 只有一个user表 |
| db02 | item表 |
| db03 | item表 |

db02,db03上的item表根据id%2取模保存数据, 也就是进行了数据分片

1. db01 创建表语句
```
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `indate` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8
```

2. db02,db03 创建表语句
```
CREATE TABLE `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` int(11) NOT NULL DEFAULT '0',
  `indate` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8
```

### 3. mycat服务器说明
**mycat目录**: /usr/local/mycat

至此, 我们的环境就配置好了

## 二、配置mycat服务
### 1. server.xml配置
路径在 `/usr/local/mycat/conf/server.xml`
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mycat:server SYSTEM "server.dtd">
<mycat:server xmlns:mycat="http://io.mycat/">
        <system>
        <property name="useSqlStat">0</property>  <!-- 1为开启实时统计、0为关闭 -->
        <property name="useGlobleTableCheck">0</property>  <!-- 1为开启全加班一致性检测、0为关闭 -->
                <property name="sequnceHandlerType">1</property>
                <property name="processorBufferPoolType">0</property>
                        <!-- 8066 为连接mycat的端口-->
                        <property name="serverPort">8066</property>
                        <!-- 9066 为连接mycat管理地址的端口-->
                        <property name="managerPort">9066</property>
                        <property name="idleTimeout">300000</property> <property name="bindIp">0.0.0.0</property>
                        <property name="frontWriteQueueSize">4096</property> <property name="processors">32</property>
                <property name="handleDistributedTransactions">0</property>
                <property name="useOffHeapForMerge">1</property>
                <property name="memoryPageSize">1m</property>
                <property name="spillsFileBufferSize">1k</property>
                <property name="useStreamOutput">0</property>
                <property name="systemReserveMemorySize">384m</property>
                <property name="useZKSwitch">true</property>
        </system>
        <!-- 配置连接mycat的账号密码, 和逻辑库名称, 可以设置多个-->
        <user name="root">
                <property name="password">123456</property>
                <property name="schemas">TESTDB</property>
        </user>
        <user name="user">
                <property name="password">user</property>
                <property name="schemas">TESTDB</property>
                <property name="readOnly">true</property>
        </user>
</mycat:server>
```

### 2. 配置rule.xml
路径在: `/usr/local/mycat/conf/rule.xml`
`function必须在tableRule的下面, 否则会报错找不到`
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mycat:rule SYSTEM "rule.dtd">
<mycat:rule xmlns:mycat="http://io.mycat/">
        <!-- 指定表规则的名称, 以及分片的function-->
        <tableRule name="role1">
                <rule>
                        <columns>id</columns>
                        <algorithm>mod-long</algorithm>
                </rule>
        </tableRule>
        <!-- 分片名称为mod-long, 为tableRule标签提供-->
        <function name="mod-long" class="io.mycat.route.function.PartitionByMod">
                <!-- 指定有几个节点,咱们有两个db02和db03,所以写2, 取模就是id%2 -->
                <property name="count">2</property>
                <property name="virtualBucketTimes">160</property>
        </function>
</mycat:rule>
```

### 3. 配置schema.xml
路径在: `/usr/local/mycat/conf/schema.xml`
声明也必须按照顺序, 最不需要调用的, 放在最后。
```
<?xml version="1.0"?>
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">
<mycat:schema xmlns:mycat="http://io.mycat/">
        <!-- 声明一个逻辑表, 表名为TESTDB, 和server.xml中的对应 -->
        <schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100">
                <!-- 指定实际表名为users, 是在node_db01节点上-->
                <table name="users" primaryKey="id" autoIncrement="true" dataNode="node_db01" />
                <!-- 实际表名为item, 在node_db02和node_db03节点上-->
                <table name="item" primaryKey="id" autoIncrement="true"  dataNode="node_db02,node_db03" rule="role1" />
        </schema>

        <dataNode name="node_db01" dataHost="dataHost01" database="db01" />
        <dataNode name="node_db02" dataHost="dataHost01" database="db02" />
        <dataNode name="node_db03" dataHost="dataHost01" database="db03" />

        <!-- 声明数据库的连接地址, 名称为dataHost01, 为dataNode节点提供-->
        <dataHost name="dataHost01" maxCon="1000" minCon="10" balance="0" writeType="0" dbType="mysql" dbDriver="native">
                <heartbeat>select user()</heartbeat>
                <!-- 数据库的连接地址，账号和密码-->
                <writeHost host="server1" url="10.211.55.9:3306" user="root" password="123123" />
        </dataHost>
</mycat:schema>
```

### 4. 启动mycat
```
> cd /usr/local/mycat/bin
> ./mycat start
```

如果发生错误可以查看/usr/local/mycat/logs/wrapper.log日志

## 三、验证

### 1. 验证user表的查询写入
账号和密码都是server.xml声明的
```
> /usr/local/mysql/bin/mysql -h10.211.55.13 -uroot -P8066 -p123456
```

#### 2. 查看库
```
mysql> show databases;
+----------+
| DATABASE |
+----------+
| TESTDB   |
+----------+
1 row in set (0.00 sec)
```

发现有TESTDB库

#### 3. 查看表
```
mysql> use TESTDB;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+------------------+
| Tables in TESTDB |
+------------------+
| item             |
| users            |
+------------------+
2 rows in set (0.00 sec)
```

看到了item和users表, 这就是我们在schema.xml中声明的逻辑表, 实际对应的是mysql服务器上的表

#### 4. 验证user的写入
```
mysql> insert into users (`id`, `name`, `indate`)values(1, 'test_name', '2017-01-01');
Query OK, 1 row affected (0.08 sec)

mysql>
```

去实际的users表中看, 数据也存在。

#### 5. 验证查询
```
mysql> select * from users;
+----+-----------+---------------------+
| id | name      | indate              |
+----+-----------+---------------------+
|  1 | test_name | 2017-01-01 00:00:00 |
+----+-----------+---------------------+
1 row in set (0.06 sec)
```

也可以查到, 说明执行成功了

### 2. 验证item表
#### 1. 验证写入
因为id分布式的话,id无法自增判断, 所以必须指定id, 否则提示错误。这个在稍后会介绍如何解决
```
mysql> insert into item(`id`, `value`, `indate`)values(1, 1, '2017-01-01');
Query OK, 1 row affected (0.01 sec)
```

查看实际的库, 发现写在了db03库中,

再写入一条
```
mysql> insert into item(`id`, `value`, `indate`)values(2, 2, '2017-01-01');
Query OK, 1 row affected (0.01 sec)
```
发现写在了db02库中, 所以分片的方式也成功了

#### 2. 验证查询
```
+----+-------+---------------------+
| id | value | indate              |
+----+-------+---------------------+
|  2 |     2 | 2017-01-01 00:00:00 |
|  1 |     1 | 2017-01-01 00:00:00 |
+----+-------+---------------------+
2 rows in set (0.03 sec)
```
也有了两条记录
