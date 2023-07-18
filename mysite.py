import dataclasses
from render_engine.site import Site
from render_engine.plugins.site_map import SiteMap
from render_engine_tailwindcss import TailwindCSS
from render_engine_youtube_embed import YouTubeEmbed
from render_engine_theme_kjaymiller import kjaymiller


@dataclasses.dataclass
class Link:
    text: str
    url: str


site_vars = {
    'HEADER_LINKS': (
        Link(text="About", url="/about.html"),
        Link(text="Blog", url="/blog/blog1.html"),
        Link(text="YouTube", url="https://www.youtube.com/channel/UCjoJU65IbXkKXsNqydro05Q"),
        Link(text="Python Community News", url='/pcn/python-community-news'),
        Link(text="Conduit", url='https://relay.fm/conduit'),
        Link(text="Talks", url="https://github.com/stars/kjaymiller/lists/conference-talks"),
        Link(text="Contact", url="/contact"),
        ),
    'timezone': "US/Pacific",
    'SITE_TITLE': "Jay Miller",
    'SITE_SUBTITLE': "Automation, Podcasting, Development",
    'SITE_URL': "https://kjaymiller.com",
    'AUTHOR': "Jay Miller",
}


app = Site()
app.site_vars.update(site_vars)
app.register_plugins(SiteMap, TailwindCSS, YouTubeEmbed) 
app.register_themes(kjaymiller)
