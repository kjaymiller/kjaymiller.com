---
date: 2023-07-18 04:28:50+00:00
description: 'Here is a subtle description to encourage the reader to read the blog
  post:


  "I recently created a theme for my website that brings my design and functionality
  into a single, shareable package. Now I''m sharing the details of how Render Engine
  supports themes in an experimental update.'
image: https://kjaymiller.azureedge.net/media/templates%20dir.jpg
tags:
- devlog
- render_engine
title: Render Engine Supports Themes
---

>!!!NOTE
> This is still experimental and some decisions are still not fully figured out.
>
>I also broke a couple things in the process... Documentation coming soon.

I created a theme for kjaymiller.com. It's looks like my current website design but it does something very important.

It moves the development and design of the site to a [shareable theme](https://github.com/kjaymiller/render-engine-theme-kjaymiller).

One of my most ambitious goals for [Render Engine](https://github.com/kjaymiller/render_engine) was to have it become a realistic option for a documentation engine.

There were some basic concepts that needed to be accomplished for that to happen:

- [ ] Themes for common documentation engines like [Readthedocs](https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html) and [MkDocs Material](https://github.com/squidfunk/mkdocs-material)
- [x] Admonitions (This was supported by trentm/markdown2 and I've been told there is custom plugin support on the way)
- [ ] Autodoc discovery

Before I could start working on Autodoc I needed the ability to create plugins that could make it easy to add the feature and customize its settings.

Before I could start working on themes, I needed to figure out how to detect and add themes.

I do have plugin support (still in development but in alpha stage). And tonight we were able to add theme support.

## How did I do this?

We aren't talking about the plugin architecture (that's a whole bigger development story that's been about 6months in development and is still in progess)

That said the changes that came to support plugins made supporting themes a bit easier. The primary change was how to add `site_settings` to your site. This simplified how settings were collected and the `register_plugins` was the impetus for the 1 of the 2 changes for theme support.

### register_themes

`register_themes` is a method for `site` that adds the template path to the engine.

```python
from render_engine import Site
from render_engine_theme_kjaymiller import kjaymiller

site = Site()
site.register_themes(kjaymiller) # You can add as many themes as you wish.
```

### render_engine_loader

Now how does that _that adds the template path to the engine_ part work.

Originally, I had all the template paths (including the user's) just loaded in. This was fast and easy and probably would have lead to several problems.

Then I decided that by switching to [Jinja's `ChoiceLoader`](https://jinja.palletsprojects.com/en/3.0.x/api/?highlight=choiceloader#jinja2.ChoiceLoader), I would be able to modify the loader on the fly since nothing was generated until `site.render` was called.

```python
        for theme in themes:
            logging.info(f"Registering theme: {theme}")
            self.engine.loader.loaders.insert(0, theme) # Updates Choice Loader
```

This also created a simple LIFO (Last in First Out) order to provide a little sanity and allowed for more reliable template file choice.

## What's next

Of course there are docs and tests that need to happen. I needed a working theme to start documenting potential gotchas. 

I'd also like to start combining plugins and themes such as [my personal theme](https://github.com/kjaymiller/render-engine-theme-kjaymiller) and my [render-engine-tailwindcss](https://github.com/kjaymiller/render-engine-tailwind) plugin. 

![site missing style from bad config](https://kjaymiller.azureedge.net/media/no%20style.jpg)

This is important as currently there is a fragile song and dance around how to configure tailwind to get your site's style.

![site with styling set from output](https://kjaymiller.azureedge.net/media/with_style.jpg)

After that I'll be working on the themes.

Shout out to all the folks that have helped me getting theses updates out the window!