---
date: 2023-10-30 00:56:57+00:00
description: 'Here''s a subtle description to encourage the reader to read the blog
  post:


  "I recently dove into the world of Render Engine themes and subthemes. As I worked
  on my first template based on my existing website, I encountered challenges that
  forced me to rethink how templates are structured and what makes something a theme
  versus a plugin. In this update, I''ll share my findings and insights on themes,
  subthemes, and carve-outs, as well as some of the new features and updates that
  came with the latest Render Engine release.'
subtitle: Render Engine update 2023.10.4
title: About Render Engines Themes, Subthemes, and Carve-outs
---

Render Engine update [2023.10.4](https://github.com/render-engine/render-engine/releases/tag/2023.10.4) was a massive update that mostly provided support around themes and created the foundation for `--reload` support to the cli. There are still some things to iron out on the reload site but let's take a look at some things around the theming.

## Subtheming

The biggest challenge with making the first render-engine template based on my existing website was to figure out where the logical splits were.

My template was designed with my site in mind. That means there were templates for a microblog and used tailwindcss along with third-party services like formspree and fontawesome. The first big decision would be _what would **come with** the template, what would be **optional**, and what would I just **remove**.

I decided to keep [tailwindcss](https://github.com/kjaymiller/render-engine-tailwindcss), making it a plugin that was associated with the theme. This meant that if you installed the theme you **HAD to use tailwind**. This was much easier than trying to reverse engineer all the tailwind things (though I could have minified and included it in static). The biggest issue with keeping the dependency was that I don't have [a check for the config file.](https://github.com/kjaymiller/render-engine-tailwindcss/issues/4)

Formspree in the end would be removed... Mostly because I forgot that I was even using it and I didn't feel like dealing with it. At the time I wasn't sure how I even would and it didn't feel like it was worth the effort. Looking back now... I have some ideas on how I would implement it that only came with figuring out how to work with fontawesome.

Speaking of, I don't fully like how I implemented fontawesome support but I think it's the most expandable method. Simply put, there are theme settings that can be used. In this case I can ask for the fontawesome key.

```python
site.update_theme_settings = ({"fontawesome": "123456890"})
```

This is used by the fontawesome theme to inject a style into the template. This meant that fontawesome became its own theme with only the one template. 

I'm a little concerned by doing this in that I think there could be some confusion on when a theme is a theme and when a plugin is a plugin. This gets even more confusing when themes can have plugins that they rely on to function properly (like render-engine-tailwindcss). My ruling on this is as such:

If the code only modifies a template and not any of the generated content itself, it is a _theme_.

If the code modifies created content or modifies a render-engine object (`Page`, `Collection`, `parser`, etc) then it is a _plugin_.

That being said I can already see how folks will want to make themes that should be plugins and plugins that should be themes.

It can also be checked against in [other themes](https://github.com/kjaymiller/render_engine_theme_kjaymiller/blob/main/src/render_engine_theme_kjaymiller/templates/components/social-cards.html). 

### Template injections

So what I described above wasn't the thing that I didn't like. It was how I would ensure that fontawesome, stylesheets, and even javascript files could be inserted into the `head` of my html files without having to constantly provide a custom `base.html` file with every template that would cause overwriting issues.

I did this by creating some base globals that could be checked against. I chose this option so that other theme creators could also use them.

I started with creating the `head` key which is checked against in the  `base.html` template.

```python
        {% block head %}
        {% for content in head %}
        {% include content %}
        {% endfor %}
        {% endblock %}
```

This string of jinja checks for anything in the `head` global attribute and will `include` it into the template. 

I've also created some class entrypoints like `body_class` and `page_title_class`. These are strings that can be inserted to add classes in common places.

I'm weary of this solution as it will create a brittle point that if overused can break a lot of things. Even the decision of switching from a string to a list of strings (which I've done) could completely screw up a template. But it does make it significantly easier to build off the base templates instead of rolling everything from scratch.

## Other Updates

I also updated many of the supporting repos in the render-engine ecosystem to support these changes:
- [Render Engine TailwindCSS](https://github.com/kjaymiller/render-engine-tailwindcss)
- [Render Engine Fontawesome](https://github.com/kjaymiller/render_engine_fontawesome)
- [Render Engine Kjaymiller Theme](https://github.com/kjaymiller/render_engine_theme_kjaymiller)
- [Render Engine Microblogging](https://github.com/kjaymiller/render_engine_microblogging)