import inspect
from render_engine import Page
from render_engine.blog import Blog
from render_engine.collection import Collection, SubCollection
from render_engine.parsers.markdown import MarkdownPageParser

from mysite import MySite

mysite = MySite()

@mysite.collection
class Pages(Collection):
    PageParser = MarkdownPageParser
    content_path = "content/pages"
    template = "page.html"


markdown_extras = [
            "footnotes",
            "fenced-code-blocks",
            "header-ids",
            "mermaid",
]
class Blog(Blog):
    PageParser = MarkdownPageParser
    parser_extras = {"markdown_extras": markdown_extras}
    template = "blog.html"
    routes = ["blog"]
    content_path = "content"
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 50

# Running render separately to save pages to variable for Index's Featured Post
blog = mysite.collection(Blog)

@mysite.page
class Index(Page):
    template = "index.html"
    template_vars = {
            "featured_post": blog.sorted_pages[0],
        }

if __name__ == "__main__":
    mysite.render()
