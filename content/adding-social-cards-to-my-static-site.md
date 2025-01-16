---
title: Adding Social Cards to my Static Site
date: 2023-05-18T18:54:44Z
tags:  [render-engine]
image: https://kjaymiller.azureedge.net/media/opengraph_cards.png
description: I've given my static website the ability to create opengraph social cards.
---

In the process of getting [Render-Engine](https://github.com/kjaymiller/render_engine) ready to be considered stable and me trying to showcase what is possible, I turned to my personal blog to see what little additions could be made and made easy with render-engine.

Something that I wanted to add was social media cards. Social cards are those image cards that you see when you share your dev.to blogs, youtube videos, and other sites.

![Example of a Twitter Social Card](https://kjaymiller.azureedge.net/media/yt-social-card-twitter.png)

Neither Render Engine, nor any Python-based static site generator is in the business of adding things to your site for you. So you wouldn't get social media cards by default. This is where themes and customizability are very helpful.

The challenge with this is to make card generation both easy and automated. What I opted for was to use Pillow to overlay text on an image. I didn't want to do too much with this as I believe solving this problem is a bit more complicated than folks would expect. Also after chatGPT gave me a bunch of deprecated code, I remembered that I had already solved this problem last year for my [30 days of Neurodiversity](https://dev.to/kjaymiller/31daysofneurodivergence-4b3p). Using the [dynamic sizing code from that project](https://github.com/kjaymiller/31DaysofNeurodivergenceTweets/blob/main/TimerTrigger/image.py), I modified the code with a new image and font. Then I added some code to my site generating script to iterate through the blog entries and generate a card for each one.

```python

if not (path:=pathlib.Path("static/images/social_cards")).exists():
    path.mkdir()

for blog_post in Blog():
    overlay_text(
        text=blog_post.title,
        image_path="static/images/social_card_base.jpg",
        output_path=f"static/images/social_cards/{slugify.slugify(blog_post.title)}.jpg",
    )

```

I ensured that the `social_cards` directory was not added to source control. You're generating a lot of images and that could slow down source control so it's better to just generate them everytime (until it isn't and then of course I could eventually have the images stored in storage which I originally wanted to do...future work)

## Adding the social cards meta properties

I'm not a pro by any means but here is a basic idea of how to add social cards to a page.

Every system except Twitter (because of course it would be Twitter) uses the `og` (short for open graph) meta tags. There are several tags that you can use to populate the card like:
- `og:type`
- `og:url`
- `og:image`
- `og:description`

Twitter can fall back to these values but also uses their own `twitter:` meta tags.

Here's an example for one a previous blog post:

```html
 <meta property="og:title" content="Always be Writing things Down (Somewhere)" />
  <meta property="og:url" content="https://kjaymiller.com/blog/always-be-writing-things-down-somewhere.html" />
  <meta property="og:image" content="https://kjaymiller.com/static/image/social_cards/always-be-writing-things-down-somewhere.jpg" />

  <meta name="twitter:title" content="Always be Writing things Down (Somewhere)">
  <meta name="twitter:image" content="https://kjaymiller.com/static/image/social_cards/always-be-writing-things-down-somewhere.jpg" />
  <meta name="twitter:card" content="summary_large_image">
```

To add this, I updated the `<head></head>` section of my blog template to grab the slug of generated image and add the contents based on the page's metadata.

```html
{% block head %}
  <link rel="stylesheet" href="/static/css/pygments.css" />
  <meta property="og:title" content="{{title}}" />
  <meta property="og:type" content="article" />
  {% if description is defined %}<meta property="og:description" content="{{description}}" />{% endif %}
  <meta property="og:url" content="{{url|to_absolute}}" />
  {% set l_image="/static/images/social_cards/" + slug + ".jpg" %}
  <meta property="og:image" content="{{l_image | to_absolute}}" />

  <meta name="twitter:title" content="{{title}}" />
  {% if description is defined %}<meta name="twitter:description" content="{{description}}" />{% endif %}
  <meta name="twitter:image" content="{{l_image | to_absolute}}" />
  <meta name="twitter:card" content="summary_large_image" />
{% endblock %}
```

This greatly increases the build time of the site and again would definitely need some refactoring in the future.

You can use one of the many opengraph validators on the internet to test this.

![Social Cards](https://kjaymiller.azureedge.net/media/opengraph_cards.png)

Figuring out how to generate social media cards will be an extremely light entrance into **theme-based extensions** or adding _theme_ template paths to your website's engine so that you could add some great features without much complexity on your part.
