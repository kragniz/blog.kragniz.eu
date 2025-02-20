AUTHOR = 'Louis Taylor'
SITENAME = 'blog.kgz.sh'
SITEURL = "https://blog.kgz.sh"

PATH = "content"

TIMEZONE = 'Europe/London'
DEFAULT_DATE_FORMAT = '%d %B %Y'

DEFAULT_LANG = 'en'

CATEGORY_FEED_ATOM = None

# Blogroll
LINKS = (
    ('GitHub', 'https://github.com/kragniz'),
)

# Social widget
SOCIAL = (
    ('fedi', 'https://chaos.social/@kgz'),
)

THEME='pelican-svbhack-hack'

ARTICLE_URL = "{slug}"
ARTICLE_SAVE_AS = "{slug}/index.html"
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'

DEFAULT_PAGINATION = 4
SUMMARY_MAX_LENGTH = None

RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
USER_LOGO_URL = "/images/me2.png"
TAGLINE='ミ๏ｖ๏彡'
