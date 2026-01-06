import os
import json

from render_engine import (
    Page,
    Site,
    Collection,
)
from render_engine.blog import Blog as _Blog

from render_engine_microblog import MicroBlog
from render_engine_markdown import MarkdownPageParser
from render_engine_aggregators.feed import AggregateFeed
from render_engine_lunr import LunrTheme

from render_engine_theme_kjaymiller import kjaymiller
from render_engine_fontawesome.fontawesome import fontawesome
from render_engine_json import JSONPageParser


app = Site()
with open("settings.json") as json_file:
    settings = json.loads(json_file.read())
app.site_vars.update(**settings)
app.register_themes(kjaymiller, fontawesome, LunrTheme)
app.plugin_manager.plugin_settings["LunrPlugin"].update(
    {"collections": ["pages", "blog"]}
)

app.site_vars.update({"SITE_URL": os.getenv("RE_SITE_URL", "http://localhost:8000")})
app.site_vars.update(head=["_head.html"])
app.render_html_site_map = True

markdown_extras = [
    "admonitions",
    "footnotes",
    "fenced-code-blocks",
    "header-ids",
    "mermaid",
    "tables",
]

# Note: _404 and GuestAppearances pages removed to avoid TUI conflicts
# These are static site pages, not meant for TUI editing


@app.collection
class Notes(_Blog):
    routes = ["notes"]
    title = "Notes to Self"
    template = "blog.html"
    Parser = MarkdownPageParser
    content_path = "content/notes"
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 20
    parser_extras = {"markdown_extras": markdown_extras}


@app.collection
class Pages(Collection):
    Parser = MarkdownPageParser
    parser_extras = {"markdown_extras": markdown_extras}
    content_path = "content/pages"
    template = "page.html"


@app.collection
class Blog(_Blog):
    routes = ["blog"]
    template = "blog.html"
    Parser = MarkdownPageParser
    content_path = "content"
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 20
    parser_extras = {"markdown_extras": markdown_extras}


@app.collection
class MicroBlog(MicroBlog):
    Parser = MarkdownPageParser
    template_vars = {"microblog_entry": "custom_microblog_post.html"}
    content_path = "content/microblog"
    template = "microblog_post.html"
    routes = ["microblog"]
    parser_extra = {"markdown_extras": markdown_extras}
    items_per_page = 20
    skip_site_map = True


@app.page
class AllPosts(AggregateFeed):
    collections = [MicroBlog]


@app.page
class Index(Page):
    template = "index.html"


if __name__ == "__main__":
    app.render()
