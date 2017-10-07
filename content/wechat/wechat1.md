title:微信公众号历史记录以及文章内容接口数据分析
date:2017-09-09
slug:wechat/wechat1

## 一: 查看历史消息
### 1. 请求转发到实际的页面
**URL**
https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI2NjA3NTc4Ng==&devicetype=iOS10.3.2&version=16050c20&lang=zh_CN&nettype=WIFI&ascene=3&fontScale=100&pass_ticket=M9BUVH%2BJ9ju9HPQnUHJOghEPjTseQIWuGhGhdg6wE2FaaMeWfW3NZR1bAv8VKX2t&wx_header=1
**作用**
猜测是为了设置cookie等一些信息, 不经过则cookie无效
**请求方式**: GET
**请求参数**

|参数名|参数值|说明|
|-|-|-|
|__biz|MzI2NjA3NTc4Ng==|公众号标识,每个公众号值不变,base64加密,解密后是数字|
|devicetype|iOS10.3.2|设备型号|
|version|16050c20|版本(不知道是啥)|
|lang|zh_CN|微信语言|
|ascene|3|(不确定作用)|
|fontScale|100|字体规模(不清楚作用)|
|pass_ticket||验证ticket|
|wx_header|1|固定值(不清楚作用)|

**Header**

|参数名|参数值|说明|
|-|-|-|
|X-WECHAT-KEY||验证的key,每次访问都会变, 有效期大约2小时,原来的key不会失效|
|X-WECHAT-UIN|MjY2NDk1NTMyMA%3D%3D|客户端的uin,每个客户端是固定的，不会变|
|User-Agent|Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.12 NetType/WIFI Language/zh_CN|

**Cookie**

|参数名|参数值|说明|
|-|-|-|
|pass_ticket|||
|wap_sid2||猜测应该是根据key,uin等计算后得到的验证值,保存在Cookie直接验证, 有效期和key有关,每次请求都会变,原来的不失效|
|wxuin|2664955320|客户端id|
|wxtokenkey|ce2fb7cff8175db8bbe1284d8ea309c974a4d393f3c0e7ddcf0f3e1925aa6d83|微信请求的一个key|
|pgv_pvid|2885910680|(不清楚)|
|eas_sid|5144i9T9L8n345w5i2L2G5A3E8|(不清楚)|
|pgv_pvi|5673884672|(不清楚)|
|g_ut|2|(不清楚)|
|news_commid|oDOGxv8dGvIVz2BAUA4ANY_SQh3I|(不清楚)|
|sd_cookie_crttime|1498009878512|cookie创建的毫秒数(猜测)|
|sd_userid|70901498009878512|(不清楚)|

## 2. 历史消息第一页
**URL**
https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI2NjA3NTc4Ng==&scene=124&devicetype=iOS10.3.2&version=16050c20&lang=zh_CN&nettype=WIFI&a8scene=3&fontScale=100&pass_ticket=M9BUVH%2BJ9ju9HPQnUHJOghEPjTseQIWuGhGhdg6wE2FaaMeWfW3NZR1bAv8VKX2t&wx_header=1

**Method** GET/POST
**模拟请求的参数**
```
# 可直接返回结果
url:https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI2NjA3NTc4Ng==
headers:
'User-Agent'=>'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 MicroMessenger/6.0.1 NetType/WIFI',
'Cookie'=>'pass_ticket=M9BUVH+J9ju9HPQnUHJOghEPjTseQIWuGhGhdg6wE2FaaMeWfW3NZR1bAv8VKX2t; wap_sid2=CLj73/YJEnA4VnFXMkc2RGZxYlNxTy1XZS1US1pubDFsY1o0OF8yUC1kR2ZrdWw3RE9fYlppUDBwblFKUTI5b2FSZVZVWnFnT25fRE5heTVSeXhlRWVMTXh3RFRjWHQyTEpfYTlSdG9lMmxPakIzRVpXdVNBd0FBMNDGwMsFOA1AlU4=; wxuin=2664955320; wxtokenkey=ce2fb7cff8175db8bbe1284d8ea309c974a4d393f3c0e7ddcf0f3e1925aa6d83; pgv_pvid=2885910680; eas_sid=5144i9T9L8n345w5i2L2G5A3E8; pgv_pvi=5673884672; g_ut=2; news_commid=oDOGxv8dGvIVz2BAUA4ANY_SQh3I; sd_cookie_crttime=1498009878512; sd_userid=70901498009878512',
```

## 3. 获取历史消息第二页
**URL**
https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzI2NjA3NTc4Ng==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=M9BUVH%2BJ9ju9HPQnUHJOghEPjTseQIWuGhGhdg6wE2FaaMeWfW3NZR1bAv8VKX2t&wxtoken=&x5=0&f=json

**METHOD** GET/POST
**模拟请求的参数**
```
# offset=0则可以获取到第一页的数据, 则没必要用获取首页页面数据分析
# 访问别的公众号, 不影响当前公众号接口请求
# 但是当前cookie不能用于别的公众号, 必须通过历史消息第一页拿到cookie
url:https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzI2NjA3NTc4Ng==&f=json&offset=10&count=10

headers:
'User-Agent'=>'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 MicroMessenger/6.0.1 NetType/WIFI',
        'Cookie'=>'pass_ticket=M9BUVH+J9ju9HPQnUHJOghEPjTseQIWuGhGhdg6wE2FaaMeWfW3NZR1bAv8VKX2t; wap_sid2=CLj73/YJEnA4VnFXMkc2RGZxYlNxTy1XZS1US1pubDFsY1o0OF8yUC1kR2ZrdWw3RE9fYlppUDBwblFKUTI5b2FSZVZVWnFnT25fRE5heTVSeXhlRWVMTXh3RFRjWHQyTEpfYTlSdG9lMmxPakIzRVpXdVNBd0FBMNDGwMsFOA1AlU4=; wxuin=2664955320; wxtokenkey=ce2fb7cff8175db8bbe1284d8ea309c974a4d393f3c0e7ddcf0f3e1925aa6d83; pgv_pvid=2885910680; eas_sid=5144i9T9L8n345w5i2L2G5A3E8; pgv_pvi=5673884672; g_ut=2; news_commid=oDOGxv8dGvIVz2BAUA4ANY_SQh3I; sd_cookie_crttime=1498009878512; sd_userid=70901498009878512',
```

## 二、获取点赞数和阅读数
**URL**:
https://mp.weixin.qq.com/mp/getappmsgext?__biz=MjM5Nzg0MTQ3OQ==&appmsg_type=9&mid=2660617942&sn=ec05841f9675c74a5f630f5993d25cc2&idx=1&is_need_ad=0

- sn: 可能是文章的唯一编码
**模拟请求的参数**
```
'headers'=>[
        'User-Agent'=>'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 MicroMessenger/6.0.1 NetType/WIFI',
        'Cookie'=>'pass_ticket=M9BUVH+J9ju9HPQnUHJOghEPjTseQIWuGhGhdg6wE2FaaMeWfW3NZR1bAv8VKX2t; wap_sid2=CLj73/YJEnA4VnFXMkc2RGZxYlNxTy1XZS1US1pnd3phR1FLN0VPQjBHOFR4SkRYLTZKTWdHWUs1OVZ1Ykwxa2M0UmFURzdFV0NTLVRYaUEyVG5VOUtRMVRZXzIxYW5vTDBJVlFXWG0xVUhpMWpGQXF5NlNBd0FBMLvWwMsFOAxAlE4=; wxuin=2664955320; wxtokenkey=48b756518ff8c26ff9600411ab07e3da21930909adb6a449a70282559e0c21b0; pgv_pvid=2885910680; eas_sid=5144i9T9L8n345w5i2L2G5A3E8; pgv_pvi=5673884672; g_ut=2; news_commid=oDOGxv8dGvIVz2BAUA4ANY_SQh3I; sd_cookie_crttime=1498009878512; sd_userid=70901498009878512',
    ],
    'form_params'=>[
        'is_only_read'=>1,
    ],
```

## 三、获取评论数据
**url**:
https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&__biz=MjM5Nzg0MTQ3OQ==&appmsgid=2660617942&idx=1&comment_id=4070344972&offset=0&limit=100
**请求方式**
get
**模拟数据**
```
'headers'=>[
        'User-Agent'=>'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 MicroMessenger/6.0.1 NetType/WIFI',
        'Cookie'=>'pass_ticket=M9BUVH+J9ju9HPQnUHJOghEPjTseQIWuGhGhdg6wE2FaaMeWfW3NZR1bAv8VKX2t; wap_sid2=CLj73/YJEnA4VnFXMkc2RGZxYlNxTy1XZS1US1pnd3phR1FLN0VPQjBHOFR4SkRYLTZMRm1aTnRzZDhmY1cwNHVXaHRyOC1EaDdtbjdhUldxV0tLQ1VOWllVT2N1NmY3LTlWTjFpNmFDNTBTUXV6SllkT1NBd0FBMKHYwMsFOA1AAQ==; wxtokenkey=33c19f4f0ced3c0f2ae0c96b7a5a794920998c44247b642c5f3b665840ad8272; wxuin=2664955320; pgv_pvid=2885910680; eas_sid=5144i9T9L8n345w5i2L2G5A3E8; pgv_pvi=5673884672; g_ut=2; news_commid=oDOGxv8dGvIVz2BAUA4ANY_SQh3I; sd_cookie_crttime=1498009878512; sd_userid=70901498009878512',
    ],

```

# 四、获取主体信息
**url**
https://mp.weixin.qq.com/mp/getverifyinfo?__biz=MjM5MDI5MjAyMA==&type=reg_info
**模拟请求数据**
```
'headers'=>[
        'User-Agent'=>'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 MicroMessenger/6.0.1 NetType/WIFI',
        'Cookie'=>'pass_ticket=M9BUVH+J9ju9HPQnUHJOghEPjTseQIWuGhGhdg6wE2FaaMeWfW3NZR1bAv8VKX2t; wap_sid2=CLj73/YJEnA4VnFXMkc2RGZxYlNxTy1XZS1US1pnd3phR1FLN0VPQjBHOFR4SkRYLTZMRm1aTnRzZDhmY1cwNHVXaHRyOC1EaDdtbjdhUldxV0tLQ1VOWllVT2N1NmY3LTlWTjFpNmFDNTBTUXV6SllkT1NBd0FBMKHYwMsFOA1AAQ==; wxtokenkey=33c19f4f0ced3c0f2ae0c96b7a5a794920998c44247b642c5f3b665840ad8272; wxuin=2664955320; pgv_pvid=2885910680; eas_sid=5144i9T9L8n345w5i2L2G5A3E8; pgv_pvi=5673884672; g_ut=2; news_commid=oDOGxv8dGvIVz2BAUA4ANY_SQh3I; sd_cookie_crttime=1498009878512; sd_userid=70901498009878512',
    ],
```
# cookie可以通用
## 备注
cookie每个公众号不通用(部分公众号是通用的,规律暂时未找到)
cookie中的有效期待定
