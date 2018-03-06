title: supervisor python的进程管理工具 使用教程 【持续更新】
date: 2017-10-31
slug: python/supervisor
Tags: supervisor, supervisord, python 进程管理
Summary: Supervisor（http://supervisord.org/）是用Python开发的一个client/server服务，是Linux/Unix系统下的一个进程管理工具，不支持Windows系统。它可以很方便的监听、启动、停止、重启一个或多个进程。用Supervisor管理的进程，当一个进程意外被杀死，supervisort监听到进程死后，会自动将它重新拉起，很方便的做到进程自动恢复的功能，不再需要自己写shell脚本来控制。

Supervisor（http://supervisord.org/）是用Python开发的一个client/server服务，是Linux/Unix系统下的一个进程管理工具，不支持Windows系统。它可以很方便的监听、启动、停止、重启一个或多个进程。用Supervisor管理的进程，当一个进程意外被杀死，supervisort监听到进程死后，会自动将它重新拉起，很方便的做到进程自动恢复的功能，不再需要自己写shell脚本来控制。

## 一、安装配置
[文档地址](http://www.supervisord.org/)
### 1. 安装
```
easy_install supervisor
pip install supervisor
```

### 2. 生成配置文件
```
sudo echo_supervisord_conf > /etc/supervisor/supervisord.conf
```

### 3.修改配置项
```python
# 找到
;[include]
;files = relative/directory/*.ini

# 改为
[include]
files = /etc/supervisor/conf.d/*.cnf
```

### 4. 启动
```
supervisord -c /etc/supervisor/supervisord.conf
```

## 二、基本使用
### 1. 创建脚本
```
# vim /etc/supervisor/conf.d/test.cnf

[program:test]
command=/usr/bin/python run.py # 要执行的目录
directroy=/var/www/test # 执行脚本的家目录
autostart=true # 是否自动开始
autorestart=true # 是否自动重启
stdout_logfile=/var/log/supervisor/%(program_name)s_out.log # 输出日志目录
stderr_logfile=/var/log/supervisor/%(program_name)s_err.log # 进程错误日志目录
```

### 2. 进程管理命令 supervisorctl
|选项|说明|
|-|-|
|-c, --configuration | 配置文件路径 |
|-i, --interactive | 在命令运行后启动一个交互shell |
|-s, --serverurl URL | 指定web管理界面的地址, 默认是 http://localhost:9001 |
|-u, --username | 指定运行服务的用户 |
|-p, --password | 指定运行服务的用户的密码 |
|-r, --history-file | 写入历史文件记录 |
|add [name] | 激活配置文件中的一个任务到进程/组 中 |
|remove [name] | 从进程中移除一个任务 |
|update | 更新配置文件, 会重启所有任务进程 |
|clear [name] | 清理指定名称的日志文件 |
|clear all | 清理所有进程的日志文件 |
|fg [name] | 用前台模式连接一个进程, 按Ctrl+c 退出前台模式 |
|pid | 获取supervisord的pid |
|pid [name] | 获取指定任务的pid |
|reread | 重新读取配置文件内容, 不重启任务 |
|restart [name] | 重启指定任务 |
|restart [gname]:* | 重启指定组任务|
|restart all | 重启所有任务 |
|start | 所有start的命令同restart |
|stop | 所有stop的命令同restart |
|status | 所有status的命令同restart |

### 3. 服务命令 supervisord
|命令选项|说明|
|-|-|
|-c config_file | 要加载的配置文件 |
|-n, --nodaemon | 前台运行supervisor |

### 4. web管理界面配置
打开/etc/supervisor/supervisord.conf
```python
# 找到
;[inet_http_server]         ; inet (TCP) server disabled by default
;port=127.0.0.1:9001        ; ip_address:port specifier, *:port for all iface
;username=user              ; default is no username (open server)
;password=123               ; default is no password (open server)
# 改为
[inet_http_server]         ; inet (TCP) server disabled by default
port=127.0.0.1:9001        ; 访问的ip和端口
username=user              ; 认证用户
password=123               ; 认证密码
```

然后打开ip:9001 就可以访问web管理界面了
## 三、高级应用
## 四、配置文件说明
### 1. program:x
|配置项|说明|是否必须|默认值|
|-|-|
|command | 要执行的命令 | Y | No default |
|process_name | 进程名 | N | %(program_name)s |
|autostart | 自动启动 | N | true |
|autorestart | 自动重启 | N | unexpected |

## 五、插件
### 1. superlancede
[点击查看源码](https://github.com/Supervisor/superlance)
[点击查看文档](https://superlance.readthedocs.io/en/latest/index.html)
#### 1. 安装
```python
easy_install superlance
pip install superlance
```
#### 2. 工具集
##### 1. httpok
通过定时对一个HTTP接口进行GET请求，根据请求是否成功来判定一个进程是否处于正常状态，如果不正常则对进程进行重启。

##### 2. crashmail
当一个进程意外退出时，发送邮件告警。

##### 3. memmon
当一个进程的内存占用超过了设定阈值时，发送邮件告警。

###### 1. 基本命令
|命令选项|说明|
|-|-|
|-c, --cumulative | 检测累计RSS, 监控过程中也监听子进程[没明白啥意思, 以后研究] |
|-p [name/size pair], --program=[name/size pair] | 检测指定任务名称的内存大小, 格式为name=size, 支持单位(“KB”, “MB” or “GB”) , 可以同时写多个任务 |
|-g [name/size pair], --groupname=[name/size pair] | 检测指定组任务名称的内存大小, 格式为gname=size, 支持单位((“KB”, “MB” or “GB”)) |
|-a [size], --any=[size] | 检测所有任务的内存大小, 达到任务则自动重启 |
|-s [command], --sendmail=[command] | 如果发生意外则发送邮件通知, 默认是/usr/sbin/sendmail -t -i |
|-m [email address], --email=[email address] | 接收邮件的邮件地址 |
|-u [email uptime limit], --uptime=[email uptime limit] | 只发送一个邮件, 防止任务在重启后, 大量发送邮件, “m” for minutes, “h” for hours or “d” for days |

###### 2. 内存超出预警
以下代码存在内存泄露问题, 内存会越来越大, 要实现的目标为达到指定内存则自动重启
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename : memoryleak.py
import time

class LeakTest(object):
    def __init__(self):
        print 'Object with id %d born here.' % id(self)

    def __del__(self):
        print 'Object with id %d dead here.' % id(self)

def doLeak():
    A = LeakTest()
    B = LeakTest()
    A.b = B
    B.a = A

if __name__ == '__main__':
    while True:
        for i in range(1, 10000):
            doLeak()
        time.sleep(5)
```

##### 4. crashmailbatch
类似于crashmail的告警，但是一段时间内的邮件将会被合成起来发送，以避免邮件轰炸。

##### 5. fatalmailbatch
当一个进程没有成功启动多次后会进入FATAL状态，此时发送邮件告警。与crashmailbatch一样会进行合成报警。

##### 6. crashsms
当一个进程意外退出时发送短信告警，这个短信也是通过email网关来发送的。
