import os
import json
from jinja2.environment import Environment as Environment

from lunr import lunr
from render_engine import Page
from render_engine.site import Site
from render_engine.blog import Blog as Blog
from render_engine_microblog import MicroBlog
from render_engine.collection import Collection
from render_engine.parsers.markdown import MarkdownPageParser
from render_engine_aggregators.feed import AggregateFeed

from render_engine.extras.site_map import SiteMap
from render_engine_youtube_embed import YouTubeEmbed
from render_engine_theme_kjaymiller import kjaymiller
from render_engine_fontawesome.fontawesome import fontawesome
from render_engine_json import JSONPageParser


app = Site()
with open("settings.json") as json_file:
    settings = json.loads(json_file.read())
app.site_vars.update(**settings)
app.register_plugins(SiteMap, YouTubeEmbed)
app.register_themes(kjaymiller, fontawesome)

if os.environ.get("prod", False):
    app.site_vars.update({"SITE_URL": "https://kjaymiller.com"})
else:
    app.site_vars.update({"SITE_URL": "http://localhost:8000"})

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
    Parser = JSONPageParser
    content_path = "conferences.json"


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


@app.collection
class MicroBlog(MicroBlog):
    template = "blog.html"
    archive_template = "microblog_post.html"
    template_vars = {
            "markdown_post": "markdown_post.html",
            }
    content_path = "content/microblog"
    routes = ["microblog"]
    parser_extras = {"markdown_extras": markdown_extras}
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
    template = "index.html"
    template_vars = latest_episodes

@app.page
class Corpus(Page):
    """The Corpus page is a list of all blog posts and their contents."""
    extension = ".json"
    pages = app.route_list["blog"]

    @property
    def _content(self):
        corpus = []
        for _id, page in enumerate(self.pages):
            entry = {
                **{
                "id": _id,
                "title": page.title,
                "url": page.url_for(),
                "content": page.content,
                }
            }
            corpus.append(entry)
        return corpus

    def _render_content(self, *args, **kwargs) -> str:
        lunr_index = lunr(ref="id", fields=["title", "url", "content"], documents=self._content)
        return json.dumps(lunr_index.serialize())

@app.page
class SearchPage(Page):
    extension = ".json"

    def _render_content(self, *args, **kwargs) -> str:
        return json.dumps(app.route_list["corpus"]._content)
    

if __name__ == "__main__":
    app.render()
