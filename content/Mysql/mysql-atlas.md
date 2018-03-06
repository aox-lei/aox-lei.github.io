title: Mysql中间件——Atlas
date: 2017-12-01
slug: mysql/mysql-atlas
Tas: mysql中间件, altas教程, altas
Summary: Atlas是由 Qihoo 360公司Web平台部基础架构团队开发维护的一个基于MySQL协议的数据中间层项目。它在MySQL官方推出的MySQL-Proxy 0.8.2版本的基础上，修改了大量bug，添加了很多功能特性。目前该项目在360公司内部得到了广泛应用，很多MySQL业务已经接入了Atlas平台，每天承载的读写请求数达几十亿条。同时，有超过50家公司在生产环境中部署了Atlas，超过800人已加入了我们的开发者交流群，并且这些数字还在不断增加。

Atlas是由 Qihoo 360公司Web平台部基础架构团队开发维护的一个基于MySQL协议的数据中间层项目。它在MySQL官方推出的MySQL-Proxy 0.8.2版本的基础上，修改了大量bug，添加了很多功能特性。目前该项目在360公司内部得到了广泛应用，很多MySQL业务已经接入了Atlas平台，每天承载的读写请求数达几十亿条。同时，有超过50家公司在生产环境中部署了Atlas，超过800人已加入了我们的开发者交流群，并且这些数字还在不断增加。

[github地址](https://github.com/Qihoo360/Atlas/)
[介绍](https://github.com/Qihoo360/Atlas/blob/master/README_ZH.md)


## 一、安装
[安装](https://github.com/Qihoo360/Atlas/wiki/Atlas%E7%9A%84%E5%AE%89%E8%A3%85)

在安装之前, 服务器上必须要装有mysql, altas会用到mysql的组件。

在启动时, 可能提示faild start altas of test之类的信息, 解决方法如下
```
echo '/usr/local/mysql/lib/' >> /etc/ld.so.conf
ldconfig
```

## 二、配置说明

```
[mysql-proxy]

(必备，默认值即可)管理接口的用户名
admin-username = user

(必备，默认值即可)管理接口的密码
admin-password = pwd

(必备，根据实际情况配置)主库的IP和端口
proxy-backend-addresses = 192.168.0.12:3306

(非必备，根据实际情况配置)从库的IP和端口，@后面的数字代表权重，用来作负载均衡，若省略则默认为1，可设置多项，用逗号分隔。如果想让主库也能分担读请求的话，只需要将主库信息加入到下面的配置项中。
proxy-read-only-backend-addresses = 192.168.0.13:3306,192.168.0.14:3306

(必备，根据实际情况配置)用户名与其对应的加密过的MySQL密码，密码使用PREFIX/bin目录下的加密程序encrypt加密，用户名与密码之间用冒号分隔。主从数据库上需要先创建该用户并设置密码（用户名和密码在主从数据库上要一致）。比如用户名为myuser，密码为mypwd，执行./encrypt mypwd结果为HJBoxfRsjeI=。如果有多个用户用逗号分隔即可。则设置如下行所示：
pwds = myuser: HJBoxfRsjeI=,myuser2:HJBoxfRsjeI=

（必备，默认值即可)Atlas的运行方式，设为true时为守护进程方式，设为false时为前台方式，一般开发调试时设为false，线上运行时设为true
daemon = true

(必备，默认值即可)设置Atlas的运行方式，设为true时Atlas会启动两个进程，一个为monitor，一个为worker，monitor在worker意外退出后会自动将其重启，设为false时只有worker，没有monitor，一般开发调试时设为false，线上运行时设为true
keepalive = true

(必备，根据实际情况配置)工作线程数，推荐设置成系统的CPU核数的2至4倍
event-threads = 4

(必备，默认值即可)日志级别，分为message、warning、critical、error、debug五个级别
log-level = message

(必备，默认值即可)日志存放的路径
log-path = /usr/local/mysql-proxy/log

(必备，根据实际情况配置)SQL日志的开关，可设置为OFF、ON、REALTIME，OFF代表不记录SQL日志，ON代表记录SQL日志，该模式下日志刷新是基于缓冲区的，当日志填满缓冲区后，才将日志信息刷到磁盘。REALTIME用于调试，代表记录SQL日志且实时写入磁盘，默认为OFF
sql-log = OFF

(可选项，可不设置）慢日志输出设置。当设置了该参数时，则日志只输出执行时间超过sql-log-slow（单位：ms)的日志记录。不设置该参数则输出全部日志。
sql-log-slow = 10

(可选项，可不设置）关闭不活跃的客户端连接设置。当设置了该参数时，Atlas会主动关闭经过'wait-timeout'时间后一直未活跃的连接。单位：秒
wait-timeout = 10

(必备，默认值即可)Atlas监听的工作接口IP和端口, 连接altas的地址
proxy-address = 0.0.0.0:1234

(必备，默认值即可)Atlas监听的管理接口IP和端口 admin-address = 0.0.0.0:2345, 连接altas管理服务的地址

(可选项，可不设置)分表设置，此例中person为库名，mt为表名，id为分表字段，3为子表数量，可设置多项，以逗号分隔，若不分表则不需要设置该项，子表需要事先建好，子表名称为表名_数字，数字范围为[0,子表数-1]，如本例里，子表名称为mt_0、mt_1、mt_2
tables = person.mt.id.3

(可选项，可不设置)默认字符集，若不设置该项，则默认字符集为latin1
charset = utf8

(可选项，可不设置)允许连接Atlas的客户端的IP，可以是精确IP，也可以是IP段，以逗号分隔，若不设置该项则允许所有IP连接，否则只允许列表中的IP连接
client-ips = 127.0.0.1, 192.168.1

(可选项，极少需要)Atlas前面挂接的LVS的物理网卡的IP(注意不是虚IP)，若有LVS且设置了client-ips则此项必须设置，否则可以不设置
lvs-ips = 192.168.1.1
```

## 三、Altas管理
执行mysql -h127.0.0.1 -uuser -ppwd -P2345进行连接, 进入altas管理

### 1. 查询帮助
```
select * from help;

+----------------------------+---------------------------------------------------------+
| command                    | description                                             |
+----------------------------+---------------------------------------------------------+
| SELECT * FROM help         | 显示帮助                                        |
| SELECT * FROM backends     | 查看后端服务器状态                 |
| SET OFFLINE $backend_id    | 下线后端服务器, $backend_id is backend_ndx's id |
| SET ONLINE $backend_id     | 上线后端服务器, ...                              |
| ADD MASTER $backend        | 添加主服务器, example: "add master 127.0.0.1:3306", ...               |
| ADD SLAVE $backend         | 添加从服务器, example: "add slave 127.0.0.1:3306", ...                |
| REMOVE BACKEND $backend_id | 移除后端服务器example: "remove backend 1", ...                        |
| ADD CLIENT $client         | 添加客户端 example: "add client 192.168.1.2", ...                  |
| REMOVE CLIENT $client      | 移除客户端example: "remove client 192.168.1.2", ...               |
| SAVE CONFIG                | 保存配置到文件                         |
+----------------------------+---------------------------------------------------------+
```

### 2. 查看后端mysql状态信息
```
mysql> select * from backends
    -> ;
+-------------+-------------------+-------+------+
| backend_ndx | address           | state | type |
+-------------+-------------------+-------+------+
|           1 | 10.211.55.9:3306  | up    | rw   |
|           2 | 10.211.55.10:3306 | up    | ro   |
+-------------+-------------------+-------+------+
2 rows in set (0.00 sec)
```

### 3. 下线mysql服务器
```
mysql> set offline 2
    -> ;
+-------------+-------------------+---------+------+
| backend_ndx | address           | state   | type |
+-------------+-------------------+---------+------+
|           2 | 10.211.55.10:3306 | offline | ro   |
+-------------+-------------------+---------+------+
1 row in set (0.00 sec)
```

### 4. 上线mysql服务器
```
mysql> set online 2;
+-------------+-------------------+---------+------+
| backend_ndx | address           | state   | type |
+-------------+-------------------+---------+------+
|           2 | 10.211.55.10:3306 | unknown | ro   |
+-------------+-------------------+---------+------+
1 row in set (0.00 sec)
```
