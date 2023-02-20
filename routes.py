from render_engine import Page
from render_engine.blog import Blog
from render_engine_microblog import MicroBlog
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
@mysite.collection
class Conduit(RSSCollection):
    PageParser = PodcastPageParser
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['conduit']
    content_path = "https://www.relay.fm/conduit/feed"


@mysite.collection
class PythonCommunityNews(RSSCollection):
    title = "Python Community News"
    PageParser = PodcastPageParser
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['pcn']
    content_path = "https://feeds.transistor.fm/python-community-podcast"



@mysite.collection
class Pages(Collection):
    PageParser = MarkdownPageParser
    content_path = "content/pages"
    template = "page.html"


@mysite.collection
class Blog(Blog):
    PageParser = MarkdownPageParser
    parser_extras = {"markdown_extras": markdown_extras}
    subcollections = ["tags"]
    template = "blog.html"
    routes = ["blog"]
    content_path = "content"
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 50


@mysite.collection
class MicroBlog(MicroBlog):
    archive_template = "microblog_archive.html"
    template = "blog.html"
    content_path = "content/microblog"
    routes = ["microblog"]
    parser_extras = {"markdown_extras": markdown_extras}
    items_per_page = 50


@mysite.collection
class Youtube(RSSCollection):
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['youtube']
    content_path = "https://www.youtube.com/feeds/videos.xml?channel_id=UCjoJU65IbXkKXsNqydro05Q"


latest_episodes = dict()
for entry, col in mysite.route_list.items():
    if isinstance(col, Collection) and col.has_archive:
        latest_episodes[entry] = {
            "title": col.title,
            "latest": col.sorted_pages[0],
            "archive": list(col.archives)[0],
        }

mysite.site_vars['latest_episodes'] = latest_episodes

@mysite.page
class Index(Page):
    template = "index.html"
