from render_engine import Page
from render_engine.blog import Blog
from render_engine.collection import Collection, SubCollection

from mysite import MySite

mysite = MySite(static="static")


@mysite.render_collection
class Pages(Collection):
    content_path = "content/pages"
    template = "page.html"
    output_path = "./"


class Blog(Blog):
    template = "blog.html"
    output_path = "blog"
    content_path = "content"
    archive_template = "blog_list.html"
    has_archive = True
    items_per_page = 20
    subcollections = (
        SubCollection("category", "Uncategorized"),
        SubCollection("tags", "untagged"),
    )


# Running render separately to save pages to variable for Index's Featured Post
blog = mysite.render_collection(Blog)


@mysite.render_page
class Index(Page):
    template = "index.html"
    featured_post = blog.sorted_pages[0]
