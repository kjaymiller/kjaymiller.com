---
title: Render Engine 2023.1.2 brings CLI, Parsers, and Begins Extensions Work and More
tag: render-engine
date: 16 Jan 2023 21:00
link: https://render-engine.readthedocs.io/en/latest/
image: https://kjaymiller.azureedge.net/media/render-engine-logo.png
---

[Render Engine](https://render-engine.readthedocs.io/en/latest/), my long term static site generator project, has been updated to version `2023.1.2`. This was the biggest update I've made and also begins creating a more structured update cycle. 

I talked about some of the development process and reasoning in a recent _Developer Journal_ update.

https://www.youtube.com/watch/8WYK_9Nk2i8

There are many updates (sorry I'm not that great at managing my changelog), but here are a few of the big topics.

## Return of the Route List and `{{url_for}}`
A few years ago, Render Engine had a `route-list` that held all the pages prior to being generated. Due to issues with performance, `route_list` was removed and instead pages were generated in-place. 

With recent versions of Python stressing performance, I've brought back the `route_list` to allow for pages to be able to reference one another. 

`{{url_for}}` creates the ability to reference a page in your `content` or jinja template . 

```frontmatter
---
slug: hello
---

My url is hello.html
```

```html
# in index.html
<div>
Say <a href={{url_for 'hello'}}>Hello</a>
</div>
```

This will allow for internal site references to help prevent breaking links from being created.

## [BREAKING] Changes to how pages/collections are rendered
A minor yet breaking change is the commands that render the pages and collections. The rendering for the pages has completely changed internally which called for a rewrite of the rendering methods as well. 

Instead of `render_page` and `render_collection` now sites use `page` for single page entries and `collection` for collection-based entries.

The removal of `render_` was to highlight how pages were created. Rendering a page or collection now happens in `site.render`.  This was done to consolidate all of the building into a function to make it easier to make changes in the future.

```python

from render_engine import Site, Page

site = Site()

@site.page
class Index(Page):
	pass
```

## [BREAKING] More Structure and Removal of `site_vars` in `Page` Objects

`site_vars` were originally setup to give you access to site variables in jinja templates. This responsibility has been moved to Jinja which means page objects no longer store `site_vars` in every page. 

## Collection Variables now in `collection_vars`

There were times where `Collection` information overwrote `Page` information. To avoid this, a`collection_vars` property create a similar structure to `site_vars`. That said, attributes in `collection_vars` are passed in as CONSTANTS in the `Page` object

```frontmatter
---
title: custom page
attr: Attribute 1
---

...
```

```python
from render_engine import Collection

class MyCollection:
    attr1 = "Attribute 2"
    content_path = "path/to/custom/page"

page = MyCollection().pages[0]
page.attr1
>>> "Attribute 1"

page.COLLECTION_ATTR1
>>> "Attribute 2"
```

##  [Breaking] Custom Parsers and Collections

This is perhaps the biggest change for Render Engine.

Since the beginning, Render Engine primarily used Markdown ([Markdown 2](https://github.com/trentm/python-markdown2) to be specific). That said I've used many hacks to build pages from custom datatypes. This update does two things:

- Removes all parsing out of the Render Engine components.
- Parsing is done using Parsers 

## PageParsers

`PageParsers` are a new component `Page` objects use to generate HTML.

The default parser, `BasePageParser`, defines the [_frontmatter_](https://daily-dev-tips.com/posts/what-exactly-is-frontmatter/) attribute component for all content. This means that unless explicitly overwritten you can use frontmatter to define attributes.

A `MarkdownPageParser` has been included with render engine and is accessed in `render_engine.parsers.markdown`.

```python
from render_engine import Page, Collection
from render_engine.parsers.markdown import MarkdownPageParser

class MyPage(Page):
    Parser=MarkdownPageParser

class MyCollection(Collection):
    PageParser=MarkdownPageParser # sets the parser for all pages
``` 

## Custom Collections

Along with `PageParsers`, Custom Collections now exist. This has always been supported, but now we're working to provide structure for Parser/Collection Extensions.

A few of these already exist and can be found in the [discussions section]((https://github.com/kjaymiller/render_engine/discussions/categories/extensions)) of the repo.

## CLI
You can now setup and build your Render Engine site using the cli command `render-engine`. 

Create a new site with `render-engine init`. You can also pass several commands to create the base template quickly.

![`render-engine init --help`](https://kjaymiller.azureedge.net/media/render-engine-init.png)

You can build your site with `render-engine build`. This is akin to using `@site.render` in your actual render-engine build file.

![`render-engine build` where `routes.py` is the script and `mysite` is the Site object](https://kjaymiller.azureedge.net/media/render-engine-build.gif)

I've been thinking a lot about what to expose in the CLI. Expect a few more commands in the future.

## What's Next

### Extensions?
I've been working to support validators and [other types of extensions](https://github.com/kjaymiller/render_engine/discussions/49). I hope to have a roadmap soon and this will be on it.

### More Tests and Docs
We had to rewrite our tests and docs so that many of our changes were tested. That said there are many edge-cases that haven't been covered.

Also our docs definitely need more love. I hope to add that as well.

### Better Automated Infrastructure around Content
While this blog post was fun, I struggled to remember all of the things that were added in this post. I also have some looming fear that I may have missed something.

I plan to add better version control, a proper changelog, and more (necessary) CI/CD.

A friendly reminder that Render Engine is an open source project and contributions are welcome.

I hope you check out Render Engine. This update brings a lot and some of the updates were only because of the amazing conversations I've had with a few folks that are using it, supporting it through [GitHub Sponsors](https://github.com/sponsors/kjaymiller).

<iframe src="https://github.com/sponsors/kjaymiller/button" title="Sponsor kjaymiller" height="35" width="116" style="border: 0;"></iframe>
