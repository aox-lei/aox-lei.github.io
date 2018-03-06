title: 微信公众号信息抓取方法(三)——增加微信抓取稳定性
date: 2017-11-10
slug: wechat/wechat-account4
Tags: 微信公众号, 微信数据抓取, 微信文章抓取, 微信点赞数抓取, 微信评论抓取
Summary: 在客户端访问公众号时, 会附加访问很多url, 图片, 视频或者其他检测类url的请求, 这些请求会造成一些开销, 且容易让客户端卡死、闪退等问题, 所以在rule.py中只要指定某些访问的url, 直接返回数据, 不发生实际的请求, 即可提高抓取效率

在客户端访问公众号时, 会附加访问很多url, 图片, 视频或者其他检测类url的请求, 这些请求会造成一些开销, 且容易让客户端卡死、闪退等问题, 所以在rule.py中只要指定某些访问的url, 直接返回数据, 不发生实际的请求, 即可提高抓取效率

```python
def request(self, flow):
    not_allow_domain = [
        r'mmbiz\.qpic\.cn',
        r'wx\.qlogo\.cn',
        r'short\.weixin\.qq\.com',
        r'minorshort\.weixin\.qq\.com',
        r'www\.microvirt\.com'
    ]
    ''' 请求 '''
    _url = flow.request.pretty_url
    for i in not_allow_domain:
        if re.compile(i, re.I).findall(_url):
            flow.response = http.HTTPResponse.make(
                200, b'hello world', {'Content-Type': 'text/html'}
            )
        break
```

在执行过程中, 有可能会内存太多造成服务器卡死, 或者服务异常退出, 这时可以借助python进程管理的神器,发生意外退出并且监控内存使用 [supervisor 使用教程](http://www.phpue.com/python/3.html)
