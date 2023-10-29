from dataclasses import dataclass
import os
import json
import pathlib

from render_engine import Page
from render_engine.site import Site
from render_engine.blog import Blog as Blog 
from render_engine_microblog import MicroBlog
from render_engine.collection import Collection
from render_engine.parsers.markdown import MarkdownPageParser
from render_engine_aggregators.feed import AggregateFeed

from render_engine.plugins.site_map import SiteMap
from render_engine_youtube_embed import YouTubeEmbed
from render_engine_theme_kjaymiller import kjaymiller
from render_engine_fontawesome.fontawesome import fontawesome


app = Site()
with open("settings.json") as json_file:
    settings = json.loads(json_file.read())
app.site_vars.update(**settings)
app.register_plugins(SiteMap, YouTubeEmbed) 
app.register_themes(kjaymiller, fontawesome)

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
    items_per_page = 20


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
    template = "blog.html"
    content_path = "content/microblog"
    routes = ["microblog"]
    parser_extras = {"markdown_extras": markdown_extras}
    items_per_page = 20

@app.page
class AllPosts(AggregateFeed):
    collections = [Blog, MicroBlog]

latest_episodes = {
    "hero": {
        "target": list(app.route_list['microblog'].archives)[0].url_for(),
        "title": MicroBlog.title,
        "content": app.route_list['microblog'].latest()[0].content,
        },
    "secondary": {
        "target": list(app.route_list['blog'].archives)[0].url_for(),
        "title": Blog.title,
        "from_template": "secondary_blog.html",
    },
    "blog": app.route_list['blog'].latest(5),
}

@app.page
class Index(Page):
    template = "index.html"
    template_vars = latest_episodes
