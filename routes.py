import tempfile
import pdb
import os
import json

from render_engine_pg import (
    get_db_connection,
    PostgresContentManager,
    PGMarkdownCollectionParser,
    PGPageParser,
    PostgresQuery,
)

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

# Initialize database connection early for collections
conn = get_db_connection(os.getenv("CONNECTION_STRING"))


@app.page
class _404(Page):
    skip_site_map = True
    no_prerender = True
    template = "404.html"
    path_name = "_404.html"


@app.page
class Conferences(Page):
    template = "conferences_map.html"
    parser_extras = {"markdown_extras": markdown_extras}
    content_path = PostgresQuery(connection=conn, collection_name="conferences")
    Parser = PGPageParser


@app.page
class GuestAppearances(Page):
    Parser = JSONPageParser
    content_path = "data/guest_appearances.json"
    template = "guest_appearances.html"
    parser_extras = {"markdown_extras": markdown_extras}


@app.collection
class Notes(_Blog):
    routes = ["notes"]
    title = "Notes to Self"
    template = "blog.html"
    Parser = PGMarkdownCollectionParser
    ContentManager = PostgresContentManager
    content_path = tempfile.gettempdir()
    content_manager_extras = {"connection": conn}
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 20
    parser_extras = {"markdown_extras": markdown_extras}

    @staticmethod
    def _metadata_attrs() -> dict[str, str]:
        return {
            "connection": conn,
            "table": "notes",
        }


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
    Parser = PGMarkdownCollectionParser
    ContentManager = PostgresContentManager
    content_path = tempfile.gettempdir()
    content_manager_extras = {"connection": conn}
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 20
    parser_extras = {"markdown_extras": markdown_extras}

    @staticmethod
    def _metadata_attrs() -> dict[str, str]:
        return {
            "connection": conn,
            "table": "blog",
        }


@app.collection
class MicroBlog(MicroBlog):
    Parser = PGMarkdownCollectionParser
    ContentManager = PostgresContentManager
    template_vars = {"microblog_entry": "custom_microblog_post.html"}
    content_path = tempfile.gettempdir()
    content_manager_extras = {"connection": conn}
    template = "microblog_post.html"
    routes = ["microblog"]
    parser_extra = {"markdown_extras": markdown_extras}
    items_per_page = 20
    skip_site_map = True

    @staticmethod
    def _metadata_attrs() -> dict[str, str]:
        return {
            "connection": conn,
            "table": "microblog",
        }


@app.page
class AllPosts(AggregateFeed):
    collections = [MicroBlog]


@app.page
class Index(Page):
    template = "custom_index.html"
    template_vars = {
        "hero": {
            "from_template": "index_hero.html",
        },
    }


if __name__ == "__main__":
    app.render()
