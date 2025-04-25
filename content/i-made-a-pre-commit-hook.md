---
date: 2024-11-05 10:21:00
description: In order to solve a problem I used AI and only to find another problem
  and create a precommit hook
tags:
- git
- pre-commit
- code-story
title: I made a precommit hook (it wasn't that bad)
---

So at work I'm on this amazing project and one of the things that I'm learning in the process is the idea of validation and pre-validation.

Here are my basics of validation and pre-validation:

1. There are things that you should do manually (test) and things that should be automated (markdownlint, prettier, etc)
2. For that second group, pre-commit is fine and honestly makes things easier to maintain
3. Failure to do the second group prior to a PR leads issues

While trying to solve a rather minor issue, I was taken on a journey that, while I don't think it's the best solution, it's a nifty one that I enjoyed working with.

## The Original problem

I noticed from a [PR in on the BPD website](https://github.com/BlackPythonDevs/blackpythondevs.github.io/pull/544) that when the we tried to pull a description from pages, that often the first couple of sentences were being grabbed and truncated. In some cases this would cut off in the middle of words and even expose some HTML if there were images too early in the post.

To solve this I made the executive decision that we could generate the summaries using _Ollama_.

Don't worry this isn't an _AI_ post in disguise. This is actually a stopgap as in my mind I resolved that if you don't want an AI generated description for your post (which I usually don't), then it would be best to add the description[^1].

I copied over my `ollama_summarizer.py`[^2] from my personal site, updated the prompt to fit the tone of the webiste and after about 10 tweaks it was..._good enough_.

## Testing the Solution and the New Problem

> 1. There are things that you should do manually (test)...

Now that I had this resolved I wanted to answer that first thing. I went in to test this but then realized that I could make a quick catch for folks not doing the thing. You see, I didn't want `ollama` to be something that everyone needed (also why I'm thinking it shouldn't live in the repo like it does.)

I decided that I would iterate through the `_posts` directory and check for a corresponding blog post. Some parameterization and _huh_ the tests sometimes failed.

## The problem I couldn't be bothered to solve _the jekyll-way_

Let's get this straight... I don't have a problem with jekyll... Honestly I've learned a lot building a simple, yet complex site with it. That said, I can't wait to port this website to [render-engine](https://github.com/render-engine/render-engine)[^3].

Something I've been doing lately is using `ephemeral_port_reserve` and `xprocess` to start the jekyll app with an open port and test against it.

**An Aside: Testing all the routes:** One benefit to static sites is that you can quickly and relatively easily test all of your pages to make sure that things are happening the way you expect. I know that it's tempting to believe that if you test one, you shouldn't haven't to test them all but let's say that if I did this I would have struggled with this.

When I was looking at some of the posts I noticed that the meta description was there but the my tests were failing on some pages and I wasn't sure what the problem was. After sleeping on it and putting about 48 hours between myself and the code I went back to it. After checking the cache from xprocess, I noticed that some pages had the full setup page and others only had the content markup. I looked at the posts and the thing I saw that felt like a revelation.

Posts that were passing the tests had `layout: post` while the others didn't. Looking at the `_config.yaml` it showed that it pointed to `article` and both `post` and `article` inherit from base. I had to assume that, for some reason the site built with `xprocess` didn't inherit things correctly. I had two choices:

1. Investigate this issue
2. ...

## The other solution

Okay so I decided that _explicit is better than implicit_ and instead I would make sure that `layout: post` was always applied.

I created a cli app called `updated_layout.py`. This raises a status code error if `layout` is not applied in the frontmatter of the post, fixing it if missing.

> ...and things that should be automated (markdownlint, prettier, etc).

Now I just need to make sure this ran without people intentionally running it. Luckily for me, we use [pre-commit](https://pre-commit.com/). I needed to figure out how to run a [pre-commit script locally](https://pre-commit.com/index.html#repository-local-hooks).

```yaml
- repo: local
  hooks:
    - id: check-for-layout
      name: check-for-layout
      files: _posts/.*.md
      entry: python update_layout.py
      language: python
      additional_dependencies: [typer, python-frontmatter, typing-extensions]
```

This means even if they don't run the tests, the PR hooks will fail (both the pytest and the pre-commit would find it). If they aren't sure why the test is failing, we are able to fix it with `pre-commit run -a`.

I thought it would be much harder to enable this. I'm actually convinced that after that, it may be a great way to solve the initial description problem the same way. I also think that I could see creating integrations for other projects in a similar way... (I'll definitely be using it on the blog).

[^1]: I actually have a better solution but as I'm tired, that will have to wait.

[^2]: I'm not sure if I should make this something that I put a little more effort into considering I'm using it in two places and it could be its own repo that is pip installable... Let me know on [social](https://mastodon.social/@kjaymiller)

[^3]: I haven't made this change because 1. I don't think the internationalization story of render-engine is good enough for this yet and 2. I don't get paid enough to work on render-engine enough to maintain it to a point that it makes sense to use more than jekyll does at this point... That said the more I run into issues, the more I'm on board with the idea.
