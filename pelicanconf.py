#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Lei'
SITENAME = "Lei's Blog"
SITEURL = 'http://www.phpue.com'
# SITEURL = 'http://127.0.0.1:8000'
THEME = 'bootstrap2'
PATH = 'content'

TIMEZONE = 'PRC'

DEFAULT_LANG = 'zh'
DISPLAY_PAGES_ON_MENU = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
MENUITEMS = (
    ('首页', SITEURL),
    ('关于我', SITEURL+'/pages/about-me.html')
)

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'))

# Social widget
SOCIAL = (('我的笔记', '#'),
          ('我的博客', '#'))

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["sitemap"]
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.7,
        "indexes": 0.5,
        "pages": 0.3,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}
