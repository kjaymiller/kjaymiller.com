import json

from render_engine.links import Link
from render_engine.site import Site


def load_json(filename):
    with open(filename) as j:
        return json.load(j)

site_vars = {
    'HEADER_LINKS': (
        Link(text="About", url="/about.html"),
        Link(text="Blog", url="/blog/blog-0.html"),
        Link(text="YouTube", url="https://www.youtube.com/channel/UCjoJU65IbXkKXsNqydro05Q"),
        Link(text="Talks", url="https://github.com/stars/kjaymiller/lists/conference-talks"),
        Link(text="Podcasts", url="/podcasts.html"),
        Link(text="Projects", url="/projects.html"),
        Link(text="Contact", url="/contact"),
        ),
    'timezone': "US/Pacific",
    'SITE_TITLE': "Jay Miller",
    'SITE_SUBTITLE': "Automation, Podcasting, Development",
    'SITE_URL': "https://kjaymiller.com",
    'AUTHOR': "Jay Miller",
    'GUEST_APPEARANCES': load_json("content/guest-appearances.json"),
    'PROJECTS': load_json("content/projects.json"),
    'PODCASTS': load_json("content/podcasts.json"),
    'CONFERENCE_TALKS': load_json("content/conference-talks.json"),
}


class MySite(Site):
    site_vars = site_vars
