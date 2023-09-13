import os

from render_engine import Page
from render_engine.blog import Blog as Blog 
from render_engine_microblog import MicroBlog
from render_engine.collection import Collection
from render_engine.parsers.markdown import MarkdownPageParser
from render_engine_aggregators.feed import AggregateFeed
from render_engine_rss.collection import RSSCollection
from render_engine_rss.parsers import PodcastPageParser

from mysite import app


markdown_extras = [
            "admonitions",
            "footnotes",
            "fenced-code-blocks",
            "header-ids",
            "mermaid",
]

@app.page
class Contact(Page):
    template = "contact.html"

@app.collection
class Pages(Collection):
    PageParser = MarkdownPageParser
    content_path = "content/pages"
    template = "page.html"


@app.collection
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

@app.collection
class Conduit(RSSCollection):
    PageParser = PodcastPageParser
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['conduit']
    content_path = "https://www.relay.fm/conduit/feed"

@app.collection
class PythonCommunityNews(RSSCollection):
    title = "Python Community News"
    PageParser = PodcastPageParser
    template = "blog.html"
    archive_template = "blog_list.html"
    routes = ['pcn']
    content_path = "https://www.youtube.com/feeds/videos.xml?channel_id=UCA8N-T_aEhHLzwwn47K-UFw"

blog = app.route_list['blog']

if os.environ.get("prod", False):
    import upload_social_card

    for post in collection:
        if not upload_social_card.check_for_image(
            check_tag="used_for",
            tags= {"used_for": "social_cards"},
            slug=post._slug,
            extension=".jpg",
        ):
            image = upload_social_card.overlay_text(
                text=post.title,
                image_path="static/images/social_card_base.jpg",
            )

            upload_social_card.upload_blob_stream(
                container="media",
                extension=".jpg",
                image=image,
                tags={"used_for": "social_cards"},
                slug=post._slug,
            )

@app.collection
class MicroBlog(MicroBlog):
    archive_template = "microblog_archive.html"
    template = "blog.html"
    content_path = "content/microblog"
    routes = ["microblog"]
    parser_extras = {"markdown_extras": markdown_extras}
    items_per_page = 50

@app.page
class AllPosts(AggregateFeed):
    collections = [Blog, MicroBlog]

latest_episodes = {
    "blog": app.route_list['blog'].latest(),
    "microblog": app.route_list['microblog'].latest(),
    "conduit": app.route_list['conduit'].latest(),
    "pcn": app.route_list['python-community-news'].latest(),
}

@app.page
class Index(Page):
    template = "index.html"
    template_vars = latest_episodes
