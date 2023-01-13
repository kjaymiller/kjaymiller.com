from dateutil import parser
import datetime
from render_engine import Page
from render_engine.blog import Blog, BlogPost
from render_engine.collection import Collection
from render_engine.parsers.markdown import MarkdownPageParser
from render_engine_rss import RSSCollection
from render_engine_rss.parsers import PodcastPageParser

from mysite import MySite

mysite = MySite()

markdown_extras = [
            "footnotes",
            "fenced-code-blocks",
            "header-ids",
            "mermaid",
]


def get_latest(collection, site):
    _collection = site.collection(collection)
    return _collection.sorted_pages[0]

@mysite.collection
class Pages(Collection):
    PageParser = MarkdownPageParser
    content_path = "content/pages"
    template = "page.html"


class Blog(Blog):
    PageParser = MarkdownPageParser
    parser_extras = {"markdown_extras": markdown_extras}
    template = "blog.html"
    routes = ["blog"]
    content_path = "content"
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 50

class Conduit(RSSCollection):
    PageParser = PodcastPageParser
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['conduit']
    content_path = "https://www.relay.fm/conduit/feed"

class PythonCommunityNews(RSSCollection):
    PageParser = PodcastPageParser
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['pcn']
    content_path = "https://feeds.transistor.fm/python-community-podcast"


class MicroBlogPost(BlogPost):
    @property
    def _slug(self):
        base_date = parser.parse(self.date)
        return base_date.strftime("%Y%m%d%H%M")

    @property    
    def _title(self):
        return ""

class MicroBlog(Blog):
    archive_template = "microblog_archive.html"
    template = "blog.html"
    PageParser = MarkdownPageParser
    content_type = MicroBlogPost
    content_path = "content/microblog"
    routes = ["microblog"]
    parser_extras = {"markdown_extras": markdown_extras}
    items_per_page = 50

class Youtube(RSSCollection):
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['youtube']
    content_path = "https://www.youtube.com/feeds/videos.xml?channel_id=UCjoJU65IbXkKXsNqydro05Q"

collections = [Youtube, Blog, MicroBlog, Conduit, PythonCommunityNews]

@mysite.page
class Index(Page):
    template = "index.html"
    template_vars = {
        collection.__name__.lower(): get_latest(collection, mysite) \
        for collection in collections
    }