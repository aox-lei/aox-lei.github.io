title: 微信公众号信息抓取方法(二)——抓取文章点赞、阅读、评论、小程序信息
date: 2017-11-10
slug: wechat/wechat-account3

上一篇文章文章将cookie信息保存到redis中, 则这一节主要是取出cookie, 并且构造方法去获取文章的点赞、阅读、评论、小程序信息, 而且不会访问文章内容页, 防止被微信认为是刷阅读数而封号, cookie的有效期保险一些为2个小时。所以在2个小时内一定要处理完数据

```python
# crawl_like.py
# -*- coding:utf-8 -*-
''' 抓取文章点赞和评论'''

import json
import re
import time
import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from app.config import redis_key
from app import logger, _, __
from app.model.Article import Article
from app.model.ContentLikeRead import ContentLikeRead
from app.model.Comment import Comment
from app.model.WechatAccountMain import WechatAccountMain
from app.model.Weapp import Weapp
from app.lib.function import emjoyEncode, now
from hot_redis import List
from app.lib.function import parse_url

logger.name = __name__

class like(object):
    ''' 抓取文章点赞和评论 '''
    LIKE_URL = 'https://mp.weixin.qq.com/mp/getappmsgext?__biz=%s&appmsg_type=9&mid=%s&sn=%s&idx=%s&appmsg_token=%s&is_need_ad=0'
    COMMENT_URL = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&__biz=%s&appmsgid=%s&idx=%d&comment_id=%s&offset=%d&limit=100'
    BODY_URL = 'https://mp.weixin.qq.com/mp/getverifyinfo?__biz=%s&type=reg_info#wechat_redirect'
    WEAPP_URL = 'https://mp.weixin.qq.com/mp/appmsg_weapp?action=batch_get_weapp&__biz=%s&mid=%s&idx=%d&weapp_num=1&weapp_appid_0=%s&weapp_sn_0=%s&appmsg_token=%s&x5=0&f=json'
    ARTICLE_URL = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=%s&f=json&offset=%d&count=10&is_ok=1&scene=124&appmsg_token=%s&uin=777&key=777&&x5=0&f=json'


    def run(self, uin):
        ''' 脚本执行入口 '''
        while True:
            # _task = List(key=redis_key.get('LIKE_HEADERS_PREFIX_KEY') + str(uin)).pop()
            _task = self.get_task() # 获取任务列表, 也就是获取cookie,biz等信息
            if not _task:
                time.sleep(10)
                continue

            _task = json.loads(_task, strict=False)

            _headers = _task.get('headers')
            _biz = _task.get('biz')
            _appmsg_token = _task.get('appmsg_token')

            wechatInfo = self.getBizInfo(_biz) # 获取公众号信息

            if wechatInfo is False:
                continue

            _threads = []

            contentList = Article().lists(wechatInfo.id) # 获取要抓取点赞的文章

            if contentList is False:
                continue

            for _content in contentList:
                _threads = []
                _content_body = self._get_content(_content.content_url)
                _comment_id = self._getCommentId(_content_body)
                _weapp_list = self.get_weapp_list(_content_body)

                _threads.append(threading.Thread(
                    target=self.crawl_like,
                    args=(_content.id, _headers, _biz, _content.mid,
                          _content.sn, _content.idx, _appmsg_token)))

                if int(_comment_id):
                    _threads.append(threading.Thread(
                        target=self.crawl_comment,
                        args=(_content.id, _headers, _biz, _content.mid,
                              _content.idx, _comment_id, 0)))

                if _weapp_list is not False:
                    for _weapp_value in _weapp_list:
                        _threads.append(threading.Thread(
                            target=self.crawl_weapp,
                            args=(wechatInfo.id, _content.id, {
                                'biz': _biz, 'mid': _content.mid,
                                'idx': _content.idx,
                                'appid': _weapp_value.get('appid'),
                                'sn': _weapp_value.get('sn'),
                                'appmsg_token': _appmsg_token
                            })))

                for _t in _threads:
                    _t.start()

                for _t in _threads:
                    _t.join()

                time.sleep(2)


            print('[%s] [账号:%s]%s --------------抓取成功' % (now(), str(uin), _biz))

    def crawl_weapp(self, wechat_account_id, content_id, url_info):
        '''
        抓取文章中的小程序
        '''
        _url = self.WEAPP_URL % (
            url_info.get('biz'), str(url_info.get('mid')),
            url_info.get('idx'), url_info.get('appid'),
            url_info.get('sn'), url_info.get('appmsg_token'))

        try:
            _requests = requests.get(_url, timeout=10)
            body = _requests.text
        except:
            logger.error(__('抓取小程序信息失败', {'url': _url}))
            return False

        data = json.loads(body, strict=False)

        if 'weapp_info' not in data:
            logger.warning(_('未获取到小程序信息数据', {'url': _url, 'body': body}))
            return False

        weapp_info = data.get('weapp_info')[0]
        if Weapp().info_by_appid(weapp_info.get('weapp_appid')) is False:
            Weapp().add({
                'wechat_account_id': wechat_account_id,
                'content_id': content_id,
                'name': weapp_info.get('nickname'),
                'homepage_url': weapp_info.get('homepage_url'),
                'logo_url': weapp_info.get('logo_url'),
                'weapp_appid': weapp_info.get('weapp_appid'),
                'weapp_username': weapp_info.get('weapp_username'),
                'app_version': weapp_info.get('app_version')
            })


    def crawl_like(self, content_id, headers, biz, mid, sn, idx, appmsg_token):
        ''' 抓取文章点赞数和阅读数 '''
        _url = self.LIKE_URL % (biz, mid, sn, str(idx), appmsg_token)
        _params = {'is_only_read': 1}
        body = ''
        try:
            body = requests.post(_url, headers=headers, data=_params, timeout=10)
            body = body.text
        except:
            logger.error(__('抓取点赞数失败', {'url': _url}))
            return False

        if body == '':
            return False

        body = json.loads(body, strict=False)

        if 'appmsgstat' not in body:
            logger.warning(_('未获取到点赞数据', {'url': _url, 'body': body}))
            return False

        _appmsgstat = body.get('appmsgstat')

        _like_num = _appmsgstat.get('like_num') if 'like_num' in _appmsgstat else 0
        _read_num = _appmsgstat.get('read_num') if 'read_num' in _appmsgstat else 0

        ContentLikeRead().add(
            content_id=content_id,
            like_num=_like_num,
            read_num=_read_num,
        )

    def crawl_comment(self, content_id, headers, biz, mid, idx, comment_id, offset=0):
        ''' 抓取文章评论 '''
        _url = self.COMMENT_URL % (biz, mid, idx, str(comment_id), offset)

        try:
            body = requests.get(_url, headers=headers, timeout=10)
            if re.compile(r'请在微信客户端打开链接', re.I).findall(body.text):
                return False
        except:
            logger.error(__('抓取评论失败:', {'url':_url, 'data':body.text}))
            return False

        body = json.loads(body.text, strict=False)
        _list = body.get('elected_comment')


        _data = []
        _reply_data = []
        for _value in _list:
            _tmp_data = {
                'content_id': content_id,
                'wx_content_id': _value.get('content_id'),
                'nick_name': emjoyEncode(_value.get('nick_name')),
                'content': emjoyEncode(_value.get('content')),
                'like_num': _value.get('like_num'),
                'is_top': _value.get('is_top'),
                'publish_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_value.get('create_time')))
            }
            _data.append(_tmp_data)
            if 'reply' in _value and 'reply_list' in _value.get('reply') and len(_value.get('reply').get('reply_list')) > 0:
                _reply_list = _value.get('reply').get('reply_list')
                for _reply_value in _reply_list:
                    _tmp_data = {
                        'wx_content_id': _value.get('content_id'),
                        'uin': _reply_value.get('uin'),
                        'publish_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_reply_value.get('create_time'))),
                        'to_uin': _reply_value.get('to_uin'),
                        'content': emjoyEncode(_reply_value.get('content')),
                        'like_num': _reply_value.get('like_num') if 'like_num' in _reply_value else 0
                    }
                    _reply_data.append(_tmp_data)

        _r = Comment().addAll(_data, _reply_data)
        return _r

    def _get_content(self, content_url):
        _headers = {
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 MicroMessenger/6.0.1 NetType/WIFI'
        }
        try:
            body = requests.get(content_url, headers=_headers, timeout=10)
            return body.text
        except:
            logger.error(__('抓取comment_id失败', {'url': content_url}))
            return False

    @classmethod
    def _getCommentId(self, body):
        try:
            _match = re.compile(r'var\s+comment_id\s+=\s+"(\d+)"\s+\*\s+\d;', re.I).findall(body)
        except:
            return False

        if _match:
            return _match[0]
        return False

    def get_weapp_list(self, body):
        '''
        从文章中获取weapp需要的信息
        '''
        try:
            _match = re.compile(r'var\s+weapp_sn_arr_json\s+=\s+"(.*?)";', re.I).findall(body)
        except:
            return False

        if not _match:
            return False

        _match = _match[0].replace('" || "', '').replace('\\x22', '"')
        if _match == '':
            return False
        data = json.loads(_match, strict=False)

        if not isinstance(data, (dict)):
            return False
        weapp_card_list = data.get('weapp_card_list')

        return weapp_card_list

    def getBizInfo(self, biz):
        info = WechatAccountMain().getInfoByBiz(biz)
        if info is False:
            return False
        if info.status != 1:
            return False

        return info

```
