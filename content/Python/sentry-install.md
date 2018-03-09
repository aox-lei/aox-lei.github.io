title: 安装sentry
date:2017-12-01
slug:python/sentry-install
Tags: sentry, 日志收集系统, log, python 日志搜集系统, 日志管理系统
Summary: Sentry 是一个开源的实时错误报告工具，支持 web 前后端、移动应用以及游戏，支持 Python、OC、Java、Go、Node、Django、RoR 等主流编程语言和框架 ，还提供了 GitHub、Slack、Trello 等常见开发工具的集成。

Sentry 是一个开源的实时错误报告工具，支持 web 前后端、移动应用以及游戏，支持 Python、OC、Java、Go、Node、Django、RoR 等主流编程语言和框架 ，还提供了 GitHub、Slack、Trello 等常见开发工具的集成。

[github地址](https://github.com/getsentry/sentry)

## 一、环境准备
| 环境 | 说明 |
| - | - |
| ubuntu16.04 | ip: 10.211.55.14 |

## 二、安装必备组件
### 1. 安装PostgreSQL
#### 1. apt 安装
```
sudo apt-get -y install postgresql postgresql-contrib
```

#### 2. 修改Postgres角色的密码
```
> sudo su
> su - postgres
> psql
```

输入:
```
postgres =# \password #修改当前用户密码
Enter new password:
Enter it again:
postgres =# \q # 退出
```

运行exit离开postgres用户

### 2. 安装redis
#### 1. 安装
```
> sudo wget http://download.redis.io/releases/redis-3.2.6.tar.gz
> sudo tar -zxvf redis-3.2.6.tar.gz
> sudo cp -rf redis-3.2.6 /usr/local/redis
> cd /usr/local/redis
> sudo apt install gcc
> sudo make
> sudo make install
```

如果提示make test, 则输入make test

#### 2. 启动
运行redis-server 启动redis

### 3. 安装python, pip, 以及其他环境
#### 1. 安装系统组件
```
sudo apt install python-setuptools python-dev libxslt1-dev gcc libffi-dev libjpeg-dev libxml2-dev libxslt-dev libyaml-dev libpq-dev
```

#### 2. 安装pip
下载get-pip.py
```
> wget "https://bootstrap.pypa.io/get-pip.py"
> sudo python get-pip.py
```

#### 3. 安装python库
```
> pip install -U virtualenv
```

## 三、安装sentry
### 1. 创建虚拟环境
```
> sudo mkdir /var/www
> sudo chmod -R 777 /var/www
> cd /var/www/
> mkdir sentry
> cd sentry
> virtualenv venv
```

### 2. 安装sentry
```
> source venv/bin/activate
> pip install -U sentry
> sentry
Usage: sentry [OPTIONS] COMMAND [ARGS]...

  Sentry is cross-platform crash reporting built with love.

  The configuration file is looked up in the `~/.sentry` config directory but this can
  be overridden with the `SENTRY_CONF` environment variable or be explicitly provided
  through the `--config` parameter.

Options:
  --config PATH  Path to configuration files.
  --version      Show the version and exit.
  --help         Show this message and exit.

Commands:
  celery      DEPRECATED see `sentry run` instead.
  cleanup     Delete a portion of trailing data based on...
  config      Manage runtime config options.
  createuser  Create a new user.
  devserver   Starts a lightweight web server for...
  django      Execute Django subcommands.
  dsym        Manage system symbols in Sentry.
  export      Exports core metadata for the Sentry...
  files       Manage files from filestore.
  help        Show this message and exit.
  import      Imports data from a Sentry export.
  init        Initialize new configuration directory.
  plugins     Manage Sentry plugins.
  queues      Manage Sentry queues.
  repair      Attempt to repair any invalid data.
  run         Run a service.
  shell       Run a Python interactive interpreter.
  start       DEPRECATED see `sentry run` instead.
  tsdb        Tools for interacting with the time series...
  upgrade     Perform any pending database migrations and...
```

## 四、配置sentry
### 1. 初始化
sentry init 配置文件路径
```
> sentry init /var/www/sentry/conf
```

### 2. 修改postgreSQL的连接账号密码
打开/var/www/sentry/conf/sentry.conf.py

修改下面这段
```
DATABASES = {
    'default': {
        'ENGINE': 'sentry.db.postgres',
        'NAME': 'sentry',
        'USER': 'postgres',
        'PASSWORD': '123123', # 刚才安装完postgreSQL 后你设置的密码
        'HOST': '',
        'PORT': '',
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': False,
    }
}
```

### 3. 初始化数据并且创建用户
```
> createdb -E utf-8 sentry
```

如果提示`createdb: could not connect to database template1: FATAL:  role "lin" does not exist`

则切换到postgre用户执行

执行
```
SENTRY_CONF=/var/www/sentry/conf/ sentry upgrade
```

如果提示`OperationalError: FATAL:  Peer authentication failed for user "postgres"`

解决方案:
1. sudo vim /etc/postgresql/9.5/main/pg_hba.conf
2. 修改
```
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
```

为
```
local   all             postgres                                md5

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
```
3. 重启postgresql
```
sudo service postgresql restart
```

再次执行
```
SENTRY_CONF=/var/www/sentry/conf/ sentry upgrade
```

如果提示`sentry.exceptions.InvalidConfiguration: MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk. Commands that may modify the data set are disabled. Please check Redis logs for details about the error.`

解决方案:
1. 进入redis redis-cli
2. 执行
```
config set stop-writes-on-bgsave-error no
```

再次执行
```
再次执行 SENTRY_CONF=/var/www/sentry/conf/ sentry upgrade
```

在这一步执行完成后可能提示你是否要创建用户,则按照要求创建用户即可, 没有提示的话执行以下语句创建
```
SENTRY_CONF=/var/www/sentry/conf/ sentry createuser
```

## 五、运行服务
```
> SENTRY_CONF=/var/www/sentry/conf/ sentry run web # 运行web服务
> SENTRY_CONF=/var/www/sentry/conf/ sentry run worker # 运行日志搜集进程
```

## 六、配置项目
1. 浏览器打开sentry的web管理, http://ip:9000
2. 输入刚才设置的账号密码
3. 点击New Project创建一个项目
4. 平台选择php, 输入项目的名称, 点击创建
5. 跳转的页面会显示连接的代码
6. 测试错误
```
<?php
require_once 'vendor/autoload.php';
Raven_Autoloader::register();

# 这里替换成你自己的项目id, 在显示连接帮助的页面
$client = new Raven_Client('http://f2c047b856bb41fcbf486f467b7fcf5b:aa2a33c7176d4c1fb86a3aa8cb4728aa@10.211.55.14:9000/1');


$error_handler = new Raven_ErrorHandler($client);
$error_handler->registerExceptionHandler();
$error_handler->registerErrorHandler();
$error_handler->registerShutdownFunction();

set_error_handler(array($error_handler, 'handleError'));
set_exception_handler(array($error_handler, 'handleException'));


$client->captureMessage("这里发生了一个错误");

$i = 1 / 0;
```
运行以后, 查看web端, 就会看到传输回来的错误了。
