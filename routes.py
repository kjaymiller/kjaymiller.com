import os
import json
from jinja2.environment import Environment as Environment


from render_engine import (
    Page,
    Site,
    Collection,
)
from render_engine.blog import Blog as _Blog

from render_engine_microblog import MicroBlog
from render_engine_markdown import MarkdownPageParser
from render_engine_aggregators.feed import AggregateFeed

from render_engine.extras import SiteMap
from render_engine_youtube_embed import YouTubeEmbed
from render_engine_theme_kjaymiller import kjaymiller
from render_engine_fontawesome.fontawesome import fontawesome
from render_engine_json import JSONPageParser
from render_engine_lunr import LunrTheme


app = Site()
with open("settings.json") as json_file:
    settings = json.loads(json_file.read())
app.site_vars.update(**settings)
app.register_plugins(SiteMap, YouTubeEmbed)
app.register_themes(kjaymiller, fontawesome, LunrTheme)
app.plugin_manager.plugin_settings["LunrPlugin"].update(
    {"collections": ["blog", "pages"]}
)

if os.environ.get("prod", False):
    app.site_vars.update({"SITE_URL": "https://kjaymiller.com"})
else:
    app.site_vars.update({"SITE_URL": ""})

markdown_extras = [
    "admonitions",
    "footnotes",
    "fenced-code-blocks",
    "header-ids",
    "mermaid",
]


@app.page
class Conferences(Page):
    template = "conferences.html"
    parser_extras = {"markdown_extras": markdown_extras}
    Parser = JSONPageParser
    content_path = "conferences.json"


@app.page
class GuestAppearances(Page):
    Parser = JSONPageParser
    content_path = "guest_appearances.json"
    template = "guest_appearances.html"
    parser_extras = {"markdown_extras": markdown_extras}


@app.collection
class Pages(Collection):
    Parser = MarkdownPageParser
    parser_extras = {"markdown_extras": markdown_extras}
    content_path = "content/pages"
    template = "page.html"


@app.collection
class Blog(_Blog):
    Parser = MarkdownPageParser
    parser_extras = {"markdown_extras": markdown_extras}
    subcollections = ["tags"]
    template = "blog.html"
    routes = ["blog"]
    content_path = "content"
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 20


@app.collection
class MicroBlog(MicroBlog):
    Parser = MarkdownPageParser
    template_vars = {"microblog_entry": "custom_microblog_post.html"}
    content_path = "content/microblog"
    template = "microblog_post.html"
    routes = ["microblog"]
    parser_extra = {"markdown_extras": markdown_extras}
    items_per_page = 20


@app.page
class AllPosts(AggregateFeed):
    collections = [Blog, MicroBlog]


latest_episodes = {
    "hero": {
        "from_template": "index_hero.html",
    },
    "secondary": {
        "target": list(app.route_list["blog"].archives)[0].url_for(),
        "title": Blog.title,
        "from_template": "secondary_blog.html",
    },
    "blog": app.route_list["blog"].latest(3),
}


@app.page
class Index(Page):
    template = "custom_index.html"
    template_vars = latest_episodes


if __name__ == "__main__":
    app.render()
