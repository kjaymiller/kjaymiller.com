import upload_social_card
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

# Add blog to the site - route_list
mysite.collection(Blog)

for blog_post in Blog():
    if not upload_social_card.check_for_image(
        check_tag="used_for",
        tags= {"used_for": "social_cards"},
        slug=blog_post._slug,
        extension=".jpg",
    ):

        image = upload_social_card.overlay_text(
            text=blog_post.title,
            image_path="static/images/social_card_base.jpg",
        )

        upload_social_card.upload_blob_stream(
            container="media",
            extension=".jpg",
            image=image,
            tags={"used_for": "social_cards"},
            slug=blog_post._slug,
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
