title:php curl时遇到Can't load the certificate "..." and its private key: OSStatus -25299的问题
date:2017-11-22
slug:php/curl-osstatus-25299
Tags: curl-osstatus, 25299, curl错误
Summary: php在执行curl 使用私钥访问https网站时, 提示Can't load the certificate "..." and its private key: OSStatus -25299, 在此之前还有提示其他类似的错误, 应该都是因为php中curl的SSL Version中不是OpenSSL的问题

php在执行curl 使用私钥访问https网站时, 提示Can't load the certificate "..." and its private key: OSStatus -25299, 在此之前还有提示其他类似的错误, 应该都是因为php中curl的SSL Version中不是OpenSSL的问题

基本环境:
MAC OS X、php5.6

phpinfo()查看curl信息, 显示的SSL Version 不是OpenSSL(在linux可能也显示别的)

一、先查看系统的curl支持的协议

```
>>> curl -V
curl 7.56.1 (x86_64-apple-darwin15.3.0) libcurl/7.56.1 OpenSSL/1.0.2m zlib/1.2.5
Release-Date: 2017-10-23
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp
Features: AsynchDNS IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP UnixSockets HTTPS-proxy
```
如果返回的信息里没有OpenSSL, 则需要重新安装一个新的curl, 查看第二步, 如果有OpenSSL, 则直接看第三步

二、重新安装curl
```
>>> brew uninstall curl
>>> brew install curl --with-openssl
>>> brew link curl --force
>>> curl --version
```

三、重新安装php
```
>>> brew uninstall php56
>>> brew install --with-homebrew-curl php56
```

四、重启服务, 查看phpinfo中的SSL VERSION 是否是OpenSSL
