import tempfile
import pdb
import os
import json

from render_engine_pg import (
    get_db_connection,
    PGPageParser,
    PostgresContentManager,
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

from render_engine_json import JSONPageParser

from re_plugin_pack import DateNormalizer, NextPrevPlugin

import markdown2
from render_engine.engine import engine as _jinja_engine


def _md_filter(text):
    if not text:
        return ""
    return markdown2.markdown(text, extras=["fenced-code-blocks", "tables", "footnotes"])


_jinja_engine.filters["md"] = _md_filter


app = Site()
with open("settings.json") as json_file:
    settings = json.loads(json_file.read())
app.site_vars.update(**settings)
app.register_themes(LunrTheme)
app.register_plugins(DateNormalizer)
app.plugin_manager.plugin_settings["LunrPlugin"].update(
    {"collections": ["pages", "blog"]}
)

app.site_vars.update({"SITE_URL": os.getenv("RE_SITE_URL", "")})
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
    Parser = PGPageParser
    template = "conferences_map.html"
    content_path = PostgresQuery(connection=conn, collection_name="conferences")

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
    Parser = MarkdownPageParser
    ContentManager = PostgresContentManager
    content_path = tempfile.gettempdir()
    content_manager_extras = {"connection": conn}
    archive_template = "notes_archive.html"
    has_archive = True
    items_per_page = 20
    parser_extras = {"markdown_extras": markdown_extras}
    plugins = [(NextPrevPlugin, {"reversed": True})]

    @staticmethod
    def _metadata_attrs() -> dict[str, str]:
        return {"connection": conn}


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
    ContentManager = PostgresContentManager
    content_path = tempfile.gettempdir()
    content_manager_extras = {"connection": conn}
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 20
    parser_extras = {"markdown_extras": markdown_extras}
    plugins = [(NextPrevPlugin, {"reversed": True})]

    @staticmethod
    def _metadata_attrs() -> dict[str, str]:
        return {
            "connection": conn,
        }


@app.collection
class MicroBlog(MicroBlog):
    Parser = MarkdownPageParser
    ContentManager = PostgresContentManager
    template_vars = {"microblog_entry": "custom_microblog_post.html"}
    content_path = tempfile.gettempdir()
    content_manager_extras = {"connection": conn}
    template = "microblog_post.html"
    archive_template = "microblog_archive.html"
    routes = ["microblog"]
    parser_extra = {"markdown_extras": markdown_extras}
    items_per_page = 10000
    skip_site_map = True

    @staticmethod
    def _metadata_attrs() -> dict[str, str]:
        return {
            "connection": conn,
        }


@app.page
class AllPosts(AggregateFeed):
    collections = [MicroBlog]


def _fetch_latest_posts(limit=15):
    """Pull recent posts from blog, notes, microblog tables, merged by date desc."""
    query = """
    (SELECT 'blog' AS _type, id, slug, title, content, description,
            external_link, image_url, date,
            mastodon_url, bluesky_url, webmentions_count
       FROM blog ORDER BY date DESC LIMIT %s)
    UNION ALL
    (SELECT 'notes' AS _type, id, slug, title, content, description,
            external_link, image_url, date,
            NULL AS mastodon_url, NULL AS bluesky_url, NULL AS webmentions_count
       FROM notes ORDER BY date DESC LIMIT %s)
    UNION ALL
    (SELECT 'microblog' AS _type, id, slug, NULL AS title, content, NULL AS description,
            external_link, image_url, date,
            mastodon_url, bluesky_url, webmentions_count
       FROM microblog ORDER BY date DESC LIMIT %s)
    ORDER BY date DESC
    LIMIT %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (limit, limit, limit, limit))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


@app.page
class Index(Page):
    template = "custom_index.html"
    template_vars = {
        "latest_posts": _fetch_latest_posts(15),
    }


@app.page
class Links(Page):
    template = "links.html"
    title = "Links"
    slug = "links"
    template_vars = {
        "links": {
            "social": [
                {
                    "text": "LinkedIn",
                    "url": "https://linkedin.com/in/kjaymiller",
                },
                {
                    "text": "Mastodon",
                    "url": "https://mastodon.social/@kjaymiller",
                },
                {
                    "text": "Bluesky",
                    "url": "https://bsky.app/profile/kjaymiller.com",
                },
            ],
            "Org and Work": [
                {
                    "text": "Black Python Devs",
                    "url": "https://blakpythondevs.com",
                },
                {
                    "text": "Aiven Blogposts",
                    "url": "https://aiven.io/blog/author/jay-miller",
                },
            ],
        }
    }


if __name__ == "__main__":
    app.render()
