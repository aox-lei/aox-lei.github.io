title: dnspod动态域名提交, 类似花生壳实现的功能
date: 2017-11-10
slug: python/dnspod-dynamic
Tags: dnspod, dnspod 动态域名, dynamic domain, 局域网搭建外部服务器
Summary: 通过dnspod的api接口, 可以把局域网内的ip解析到公网地址, 并且自动检测、自动绑定


Powered by Lei

## 1. dnspod动态提交域名解析记录
经常想把家里的电脑作为服务器绑定到外网使用, 但是ip是动态的, 这个脚本就是借助dnspod的解析api, 自动把域名解析到家里电脑的公网ip
然后从路由器开启dmz主机, 就可以在外网用域名访问家里的电脑了

## 一、dnspod动态提交域名解析记录
经常想把家里的电脑作为服务器绑定到外网使用, 但是ip是动态的, 这个脚本就是借助dnspod的解析api, 自动把域名解析到家里电脑的公网ip
然后从路由器开启dmz主机, 就可以在外网用域名访问家里的电脑了

程序每15分钟会检测一次ip变化, 发生变化则提交到dnspod
### 1. 安装
```
pip install requests apscheduler argparse
```
 [如何获取自己的api_token](https://support.dnspod.cn/Kb/showarticle/tsid/227/)
```
修改文件, 打开dnspod.py,
修改 API_TOKEN = '登录的token' 为你的API_TOKEN, 方法是id, api_token
```

### 2. 使用
1. 获取你的域名列表
```
python dnspod.py -d
```
2. 获取指定域名的记录信息
```
python dnspod.py -r 123 # 从第一步查出来的域名的domain_id
```
3. 填写要修改的记录id
```
# 打开dnspod.py 找到:
RECORD_IDS = [ # 记录id
    1,
    2,
]
改为要修改的记录id
```

4. 运行
```
python dnspod.py -s 开始运行
```

有问题可以提交到这里: [ISSUE](https://github.com/mm333444/python_script/issues/new)
qq群:252799167
