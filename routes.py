from dateutil import parser
import datetime
from render_engine import Page
from render_engine.blog import Blog, BlogPost
from render_engine.collection import Collection, SubCollection
from render_engine.parsers.markdown import MarkdownPageParser
from render_engine_rss import RSSCollection
from render_engine_rss.parsers import PodcastPageParser

from mysite import MySite

mysite = MySite()

@mysite.collection
class Pages(Collection):
    PageParser = MarkdownPageParser
    content_path = "content/pages"
    template = "page.html"


markdown_extras = [
            "footnotes",
            "fenced-code-blocks",
            "header-ids",
            "mermaid",
]


class Blog(Blog):
    PageParser = MarkdownPageParser
    parser_extras = {"markdown_extras": markdown_extras}
    template = "blog.html"
    routes = ["blog"]
    content_path = "content"
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 50

# Running render separately to save pages to variable for Index's Featured Post
blog = mysite.collection(Blog)

@mysite.collection
class Conduit(RSSCollection):
    PageParser = PodcastPageParser
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['conduit']
    content_path = "https://www.relay.fm/conduit/feed"

@mysite.collection
class PythonCommunityNews(RSSCollection):
    PageParser = PodcastPageParser
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['pcn']
    content_path = "https://feeds.transistor.fm/python-community-podcast"

@mysite.page
class Index(Page):
    template = "index.html"
    template_vars = {
            "featured_post": blog.sorted_pages[0],
        }

class MicroBlogPost(BlogPost):
    @property
    def _slug(self):
        base_date = parser.parse(self.date)
        return base_date.strftime("%Y%m%d%H%M")

    @property    
    def _title(self):
        return ""

@mysite.collection
class MicroBlogPost(Blog):
    title = "MicroBlog"
    archive_template = "microblog_archive.html"
    template = "blog.html"
    PageParser = MarkdownPageParser
    content_type = MicroBlogPost
    content_path = "content/microblog"
    routes = ["microblog"]
    parser_extras = {"markdown_extras": markdown_extras}
    items_per_page = 50

