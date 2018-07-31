title:zookeeper 安装使用教程
date:2018-04-11
Tags: zookeeper, 分布式集群, 分布式应用协调
slug:linux/zookeeper-install
Summary: Zookeeper是一个高性能的分布式系统的协调服务。它在一个简单的接口里暴露公共服务：像命名、配置管理、同步、和群组服务，所以你没有必要从头开始实现它们。你可以使用现成的Zookeeper去实现共识、群组管理、领导人选举和业务协议。并且你可以在它的基础之上建立自己特定的需求。

Zookeeper是一个高性能的分布式系统的协调服务。它在一个简单的接口里暴露公共服务：像命名、配置管理、同步、和群组服务，所以你没有必要从头开始实现它们。你可以使用现成的Zookeeper去实现共识、群组管理、领导人选举和业务协议。并且你可以在它的基础之上建立自己特定的需求。

Zookeeper实现的方式为建立一个集群服务器, 并且集群服务器会自动选择leader, 当leader挂掉以后再重新选举。在zookeeper中可以创建节点, 通过监听节点数据变化, 来达到客户端执行指定操作。

## 一、安装
### 一、安装jdk
```
$ java -version
```
![java-version]({filename}/upload/zookeeper-install/java-version.png)

如果你的机器上安装了java, 则直接跳过此步骤

#### 1. 通过访问链接下载最新版本的JDK，并下载最新版本的[JAVA](http://www.oracle.com/technetwork/java/javase/downloads/index.html)。

#### 2. 安装
```
$ cd ~/Downloads
$ tar -zxf jdk-8u60-linux-x64.gz # 解压文件
$ mkdir /opt/jdk
$ mv jdk-1.8.0_60 /opt/jdk/
```

#### 3. 设置路径
要设置路径和JAVA_HOME变量，请将以下命令添加到〜/.bashrc文件中。
```
export JAVA_HOME = /usr/jdk/jdk-1.8.0_60
export PATH=$PATH:$JAVA_HOME/bin
```

运行更改以生效
```
$ source ~/.bashrc
```

### 二、安装zooker
#### 1. 下载
要在你的计算机上安装ZooKeeper框架，请访问以下链接并下载最新版本的ZooKeeper。http://zookeeper.apache.org/releases.html

#### 2. 创建配置文件
使用命令 vi conf/zoo.cfg 和所有以下参数设置为起点，打开名为 conf/zoo.cfg 的配置文件.

```
$ vi conf/zoo.cfg

tickTime = 2000
dataDir = /path/to/zookeeper/data
clientPort = 2181
initLimit = 5
syncLimit = 2
```

#### 3. 启动ZooKeeper服务器
执行以下命令
```
$ bin/zkServer.sh start
```

```
$ JMX enabled by default
$ Using config: /Users/../zookeeper-3.4.6/bin/../conf/zoo.cfg
$ Starting zookeeper ... STARTED
```

## 二、使用CLI客户端
### 1. 启动
```
$ bin/zkCli.sh
```

成功以后会返回以下信息
```
Connecting to localhost:2181
................
................
................
Welcome to ZooKeeper!
................
................
WATCHER::
WatchedEvent state:SyncConnected type: None path:null
[zk: localhost:2181(CONNECTED) 0]
```

## 三、ZooKeeper服务
|操作|说明|
| - | - |
| start | 启动 |
| start-foreground | 查看启动不成功的原因 |
| stop | 停止 |
| restart | 重启 |
| status| 查看服务状态 |
| upgrade | 升级 |
| print-cmd | 打印命令 |

## 四、配置文件说明
| 配置项 | 默认值 | 说明 |
| - | - | - |
| clientPort | 2181 | 客户端连接 |
| dataDir | zookeeper安装目录/data | 存储快照文件snapshot的目录。默认情况下，事务日志也会存储在这里。建议同时配置参数dataLogDir, 事务日志的写性能直接影响zk性能。|
| tickTime | 2000 | ZK中的一个时间单元。ZK中所有时间都是以这个时间单元为基础，进行整数倍配置的。例如，session的最小超时时间是2*tickTime。|
| dataLogDir | |事务日志输出目录。尽量给事务日志的输出配置单独的磁盘或是挂载点，这将极大的提升ZK性能。  |
| globalOutstandingLimit | | 最大请求堆积数。默认是1000。ZK运行的时候， 尽管server已经没有空闲来处理更多的客户端请求了，但是还是允许客户端将请求提交到服务器上来，以提高吞吐性能。当然，为了防止Server内存溢出，这个请求堆积数还是需要限制下的 |
| preAllocSize | | 预先开辟磁盘空间，用于后续写入事务日志。默认是64M，每个事务日志大小就是64M。如果ZK的快照频率较大的话，建议适当减小这个参数。|
| snapCount | | 每进行snapCount次事务日志输出后，触发一次快照(snapshot), 此时，ZK会生成一个snapshot.*文件，同时创建一个新的事务日志文件log.*。默认是100000.（真正的代码实现中，会进行一定的随机数处理，以避免所有服务器在同一时间进行快照而影响性能）|
| traceFile | | 用于记录所有请求的log，一般调试过程中可以使用，但是生产环境不建议使用，会严重影响性能 |
| maxClientCnxns | 60 | 单个客户端与单台服务器之间的连接数的限制，是ip级别的，如果设置为0，那么表明不作任何限制。请注意这个限制的使用范围，仅仅是单台客户端机器与单台ZK服务器之间的连接数限制，不是针对指定客户端IP，也不是ZK集群的连接数限制，也不是单台ZK对所有客户端的连接数限制。 |
| clientPortAddress | | 对于多网卡的机器，可以为每个IP指定不同的监听端口。默认情况是所有IP都监听 clientPort 指定的端口 |
| minSessionTimeoutmaxSessionTimeout | 2 *  tickTime ~ 20 * tickTime  | Session超时时间限制，如果客户端设置的超时时间不在这个范围，那么会被强制设置为最大或最小时间。 |
| fsync.warningthresholdms | 1000ms |事务日志输出时，如果调用fsync方法超过指定的超时时间，那么会在日志中输出警告信息。|
| autopurge.purgeInterval | 0 | 在上文中已经提到，3.4.0及之后版本，ZK提供了自动清理事务日志和快照文件的功能，这个参数指定了清理频率，单位是小时，需要配置一个1或更大的整数，默认是0，表示不开启自动清理功能。|
| autopurge.snapRetainCount | 3 | 这个参数和上面的参数搭配使用，这个参数指定了需要保留的文件数目。 |
| initLimit | 10 | Follower在启动过程中，会从Leader同步所有最新数据，然后确定自己能够对外服务的起始状态。Leader允许F在 initLimit 时间内完成这个工作。通常情况下，我们不用太在意这个参数的设置。如果ZK集群的数据量确实很大了，F在启动的时候，从Leader上同步数据的时间也会相应变长，因此在这种情况下，有必要适当调大这个参数了。|
| syncLimit | 5 | 在运行过程中，Leader负责与ZK集群中所有机器进行通信，例如通过一些心跳检测机制，来检测机器的存活状态。如果L发出心跳包在syncLimit之后，还没有从F那里收到响应，那么就认为这个F已经不在线了。注意：不要把这个参数设置得过大，否则可能会掩盖一些问题。 |
| leaderServes | | 默认情况下，Leader是会接受客户端连接，并提供正常的读写服务。但是，如果你想让Leader专注于集群中机器的协调，那么可以将这个参数设置为no，这样一来，会大大提高写操作的性能。 |
| server.x=[hostname]:nnnnn[:nnnnn] | | 这里的x是一个数字，与myid文件中的id是一致的。右边可以配置两个端口，第一个端口用于F和L之间的数据同步和其它通信，第二个端口用于Leader选举过程中投票通信。 |
| group.x=nnnnn[:nnnnn]weight.x=nnnnn | | 对机器分组和权重设置, http://zookeeper.apache.org/doc/r3.4.3/zookeeperHierarchicalQuorums.html |
| cnxTimeout | 5s | Leader选举过程中，打开一次连接的超时时间|
| zookeeper.DigestAuthenticationProvider.superDigest | | http://blog.51cto.com/nileader/930635 |
| skipACL | | 对所有客户端请求都不作ACL检查。如果之前节点上设置有权限限制，一旦服务器上打开这个开头，那么也将失效。|
| forceSync | | 这个参数确定了是否需要在事务日志提交的时候调用 FileChannel .force来保证数据完全同步到磁盘。|
| jute.maxbuffer | 1M | 每个节点最大数据量，是默认是1M。这个限制必须在server和client端都进行设置才会生效。|

我的博客即将搬运同步至腾讯云+社区，邀请大家一同入驻：https://cloud.tencent.com/developer/support-plan?invite_code=2n310aji3veo4
