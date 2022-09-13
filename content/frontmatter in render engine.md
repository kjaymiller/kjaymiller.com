---
title: Frontmatter replacing custom parser in Render Engine
date: 23 Apr 2021 07:00
tags: development, render-engine
---

There's a tug-of-war in software development around whether or not your products
should be dependent light or heavy. Render Engine has always taken the stance of
in order to make the best possible service with my limited availability for
maintenance, I have to rely on folks how are putting energy into components. One
area that I did implement myself was a custom parser that allowed you to add all
the metadata for your page objects in the file themselves. This was to replicate
what static generators like Pelican and and Jekyl were doing to make migrating
to Render Engine feel simpler.

Recently, friend and mad-yogi of the internet, [Brett Terpstra][8173-0001] added support for a framework called Frontmatter to his
application bunch. This greatly enhanced the applications ability to customize
how and when bunches triggered and increased his ability to add other features
to the app.

After that friend and mentor, [Jeff Triplett](https://twitter.com/webology) showed me how he was
using python-frontmatter along with PyDantic to help build some custom sites to
support businesses during the COVID-19 pandemic. Well, that was enough to
encourage me to give it a try.

It's not ready yet. There is a bunch of planning that is still needed to make it stable and to provide an easy conversion path,
but [in testing](https://github.com/kjaymiller/render_engine) I have built
initial support for frontmatter in Render Engine.

IT'S NOT TESTED, IT WILL REWRITE YOUR CONTENT TO FIT THAT FORMAT. There will be updates in the future so
keep an eye out.

[8173-0001]: https://brettterpstra.com/
