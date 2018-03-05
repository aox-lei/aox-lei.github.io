title: 微信公众号信息抓取方法(一)——抓取公众号历史消息列表数据
date: 2017-11-10
slug: wechat/wechat-account2

马上双十一了, 凑个热闹, 发布一篇重量级的文章。如何抓取微信公众号的文章

## 一、介绍
研究微信抓取之前, 看过知乎有大神写的比较完善的例子, 受到启发, 才完成了整个微信公众号的抓取。
[微信公众号内容的批量采集与应用](https://zhuanlan.zhihu.com/c_65943221)
微信抓取的难点:
1. 无法获取到微信公众号的信息(微信并没有提供列表)
2. 无法脱离客户端获取微信公众号历史消息页面
3. 可以获取到文章内容页但是脱离客户端后无法获取到点赞、阅读数据

所以, 流程中的一部分是依赖于手机客户端的, 如果要大量抓取微信公众号信息,就必须依靠大量客户端抓取(自己准备手机、微信号、电费、和人工)

基本使用的方式是和知乎大神说的一样的, 都是中间人代理攻击的方式。

## 一、抓取要使用的工具
知乎大神用的是nodejs, post给php处理, 并且github上有的大部分也是用这个方式, 或者纯nodejs的方式, 个人觉得受限太大, 最主要的原因是我不会nodejs, 简单学过一些, 不过使用的anyproxy, 还是会出现一些无法解决的问题, 无法适用于长期采集

1. python3.5+
2. mitmproxy
3. 其他用到的包插件

## 二、微信抓取基本的应用规则
1. 单个客户端公众号历史消息列表页, 一天访问次数不可以超过1300次, 保险点, 最好别超过1000次, 访问太多, 会提示页面无法打开或者操作频繁, 24小时以后自动解封
2. 千万不要用客户端大量访问文章内容页, 会直接造成封号, 知乎大神的方式里, 是必须访问文章内容页的. 这个是大忌
3. 单个客户端抓取多篇文章的阅读点赞的时间间隔必须超过2秒, 不然会返回unknow error的错误
4. 单个客户端抓取阅读点赞一天不能超过6000, 要不然也会返回错误

## 三、抓取的基本逻辑
获取到公众号——访问公众号历史列表页面——抓取到第一页的文章列表数据以及cookie信息——其他脚本抓取点赞、阅读、评论和小程序信息

## 四、教程开始
### 1. 安装必备包
假设项目目录在/var/www/project 下

1. 安装python3、virtualenv、pip 工具
自己百度

2. 创建python虚拟环境
```
virtualenv -p python路径 --no-site-packages venv
source venv/bin/activate
```

3. 安装必备包
```
pip install mitmproxy
pip install requests
其他mysql、redis或队列的包, 自己根据需要安装即可
```

### 2. 抓取历史详情页数据
```
# rule.py
import re
from mitmproxy import http
from content import content

content_list_url_redirect = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=%s#wechat_redirect'

def response(flow):
    req_url = flow.request.pretty_url
    res_headers = flow.response.headers
    req_headers = flow.request.headers
    body = flow.response.text
    status_code = flow.response.status_code

    if status_code == 200:
        if re.compile('r'mp\.weixin\.qq\.com\/mp\/profile_ext\?action=home', re.I).findall(self.req_url):
            '''启动一个线程去抓取到的页面中获取到文章列表的处理'''
            _thread.append(threading.Thread(target=content().run, args=(body)))
            body = get_next_body()

            flow.response = http.HTTPResponse.make(
                200, bytes(body, encoding='utf-8'),
                {'Content-Type': 'text/html', 'Cache-Control': 'no-cache, must-revalidate'}
            )

def get_next_body(content_body):
    if body != '':
        wechat_account_name = parse_wechat_account_name(content_body)
        if wechat_account_name:
            _body = '<p>当前抓取公众号: %s</p>' % (wechat_account_name)
    else:
        _body = ''

    body = '''<meta http-equiv="content-type" content="text/html;charset=utf8">
        <meta id="viewport" name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0" />
        <style>p {font-size:1.25em;}</style>
        %s
        <script>setTimeout(function(){window.location.href="%s";},%s);</script> %s''' %\
        (_body, get_next_url(), str(80*1000), content_body)

    return body

def parse_wechat_account_name(body):
    ''' 从内容中解析公众号名称 '''
    _regular = r'<strong\s+class="profile_nickname"\s+id="nickname">\s+(.*?)\s+</strong>'
    data = re.compile(_regular, re.I).findall(body)

    if data:
        return data[0]

    return False

def get_next_url():
    '''这部分写要跳转到下一页的url'''
```

```
# content.py
分析内容中的文章列表并保存
以及将cookie保存起来, 假设保存到redis中
```
