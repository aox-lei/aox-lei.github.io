title: mycat教程(一) —— 安装
date: 2017-12-01
slug: mysql/mycat-1
Tags: mycat, mycat教程, 数据库中间件

Mycat 是什么？从定义和分类来看，它是一个开源的分布式数据库系统，是一个实现了 MySQL 协议的的 Server，前端用户可以把它看作是一个数据库代理，用 MySQL 客户端工具和命令行访问，而其后端可以用 MySQL 原生（Native）协议与多个 MySQL 服务器通信，也可以用 JDBC 协议与大多数主流数据库服务器通信， 其核心功能是分表分库，即将一个大表水平分割为 N 个小表，存储在后端 MySQL 服务器里或者其他数据库里。

## 一. 安装jdk
下载地址:http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html

1. 解压
```
tar -zxvf jdk-8u161-linux-x64.tar.gz
```
2. 创建java目录
```
sudo mkdir /java
```

3. 移动文件到/java下
```
sudo mv jdk1.8.0_161 /java
```

4. 配置环境变量
```
sudo vim /etc/environment
```
末尾加入以下配置（JAVA_HOME 后的路径就是jdk的文件位置)
```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:$JAVA_HOME/bin"
export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
export JAVA_HOME=/java/jdk1.8.0_161
```
修改完成之后保存关闭，并输入以下命令使环境变量立即生效
```
source /etc/environment
```

5. 检查是否安装成功
```
> java -version
java version "1.8.0_161"
Java(TM) SE Runtime Environment (build 1.8.0_161-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.161-b12, mixed mode)
```

6. 配置重启后的环境变量
```
sudo gedit /etc/profile
```
在文件的最后添加以下内容：
```
#set Java environment
export JAVA_HOME=/dengyang/jdk1.8.0_161
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
```
使环境变量生效
```
source /etc/profile
```

## 2. 安装mycat
下载地址: http://dl.mycat.io/1.6-RELEASE/

1. 解压
```
tar -zxvf Mycat-server-xxxxx.linux.tar.gz
```

2. 移动到/usr/local/目录
```
sudo mv mycat /usr/local
```

3. 创建用户
```
useradd mycat
```

4. 修改权限
```
chown -R mycat mycat /usr/local/mycat
```

5. 查看目录
| - bin ----------- 执行文件目录<br/>
| - conf ---------- 配置文件目录<br/>
| - doc ----------- 文档目录<br/>
| - lib ----------- 目录下主要存放 mycat 依赖的一些 jar 文件<br/>
| - logs ---------- 日志目录。日志的配置是在 conf/log4j.xml 中
