import json

from render_engine.links import Link
from render_engine.site import Site
from render_engine.plugins import CleanOutput, SiteMap
from render_engine_tailwindcss import TailwindCSS
from render_engine_youtube_embed import YouTubeEmbed


def load_json(filename):
    with open(filename) as j:
        return json.load(j)

site_vars = {
    'HEADER_LINKS': (
        Link(text="About", url="/about.html"),
        Link(text="Blog", url="/blog/blog-0.html"),
        Link(text="YouTube", url="https://www.youtube.com/channel/UCjoJU65IbXkKXsNqydro05Q"),
        Link(text="Python Community News", url='/pcn/pythoncommunitynews'),
        Link(text="Conduit", url='/conduit/conduit'),
        Link(text="Talks", url="https://github.com/stars/kjaymiller/lists/conference-talks"),
        Link(text="Contact", url="/contact"),
        ),
    'timezone': "US/Pacific",
    'SITE_TITLE': "Jay Miller",
    'SITE_SUBTITLE': "Automation, Podcasting, Development",
    'SITE_URL': "https://kjaymiller.com",
    'AUTHOR': "Jay Miller",
}


class MySite(Site):
    site_vars = site_vars
    plugins = [
        CleanOutput,
        SiteMap,
        TailwindCSS,
        YouTubeEmbed
    ]
