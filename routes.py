import slugify
from upload_social_card import overlay_text
from render_engine import Page
from render_engine.blog import Blog as Blog 
from render_engine_microblog import MicroBlog
from render_engine.collection import Collection
from render_engine.parsers.markdown import MarkdownPageParser
from render_engine_aggregators.feed import AggregateFeed
from render_engine_rss import RSSCollection
from render_engine_rss.parsers import PodcastPageParser

from mysite import MySite

mysite = MySite()

markdown_extras = [
            "admonitions",
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

mysite.collection(Blog)

if not pathlib.Path("static/images/social_cards").exists():
    mkdir("static/images/social_cards")

for blog_post in Blog():
    overlay_text(
        text=blog_post.title,
        image_path="static/images/social_card_base.jpg",
        output_path=f"static/images/social_cards/{slugify.slugify(blog_post.title)}.jpg",
    )


class MicroBlog(MicroBlog):
    archive_template = "microblog_archive.html"
    template = "blog.html"
    content_path = "content/microblog"
    routes = ["microblog"]
    parser_extras = {"markdown_extras": markdown_extras}
    items_per_page = 50

mysite.collection(MicroBlog)

@mysite.collection
class Youtube(RSSCollection):
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['youtube']
    content_path = "https://www.youtube.com/feeds/videos.xml?channel_id=UCjoJU65IbXkKXsNqydro05Q"


latest_episodes = dict()
for entry, col in mysite._route_list.items():
    if isinstance(col, Collection) and col.has_archive:
        latest_episodes[entry] = {
            "title": col.title,
            "latest": col.sorted_pages[0],
            "archive": list(col.archives)[0],
        }

mysite.engine.globals['latest_episodes'] = latest_episodes


@mysite.page
class AllPosts(AggregateFeed):
    collections = [Blog, MicroBlog]


@mysite.page
class Index(Page):
    template = "index.html"
