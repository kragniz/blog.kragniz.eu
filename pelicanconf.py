#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Louis Taylor'
SITENAME = u'blog.kragniz.eu'
SITEURL = ''

PATH = 'content'

DEFAULT_LANG = u'en'

THEME='pelican-svbhack-hack'

ARTICLE_URL = "{slug}"
ARTICLE_SAVE_AS = "{slug}/index.html"
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'

DEFAULT_PAGINATION = None
SUMMARY_MAX_LENGTH = None

SITEURL = 'http://blog.kragniz.eu'
RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
USER_LOGO_URL = SITEURL + "/images/lpt_gliph.svg"
TAGLINE='ミ๏ｖ๏彡'

# Blogroll
LINKS = (('Github', 'http://github.com/kragniz'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/kragniz'),)

GOOGLE_ANALYTICS = "UA-59782204-1"

#DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
