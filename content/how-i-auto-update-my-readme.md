---
Title: How I AutoUpdate My Github README using GitHub Actions in 5 Easy Steps
date: 10 Jul 2020 15:16
category: coding
tags: github, github actions, python, automation
---

A new phenominon in the developer space is now the 🌟_secret_🌟 README.md
trick. If you have a repository with the EXACT (case-sensitive) name as your username, it will display the contents of that readme onto your GitHub profile.

Some folks have done really cool things with it, including setting up your own
Myspace-esque top8 (including Tom!).

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Check it out. I made MySpace but on <a href="https://twitter.com/github?ref_src=twsrc%5Etfw">@github</a>.<a href="https://t.co/p4DWP4DxRR">https://t.co/p4DWP4DxRR</a> - My list is power by a GitHub Action workflow 😏 <a href="https://t.co/PN80mFCqOE">pic.twitter.com/PN80mFCqOE</a></p>&mdash; Brian Douglas (@bdougieYO) <a href="https://twitter.com/bdougieYO/status/1281699715466199040?ref_src=twsrc%5Etfw">July 10, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Inspired by [Simon Willison's](https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/) amazing self-updating profile, I wanted to do something similar.

Armed with the power of python (_and anime on my side_), I setout to do something similar. This is a look at the first steps of me automating my Github Profile.

### Step 1: Rename the repo my website to a repo named after my GitHub username

This is easy enough. Just rename the repo (in Github) to your username.
Remember this has to be exact and it is case-sensitive.

You can do this in the settings menu of your repo. You don't have to change the
directory names or anything like that on a local machine. (I'm not sure if you
are using a Git Client other than the cli).

### Step 2: Create a copy of your existing readme as a template

My goal was to create my README using a Jinja2 and Github Actions. For that I
would need a template to render. So since most of the data was the same I just
copied my existing README.

### Step 3: Add Dynamic Content using Jinja2 Variables


Starting out I wanted to show my latest blog post and my latest podcast episode
from [Productivity in Tech Podcast](https://podcast.productivityiintech.com). We will create a python script that does
this, but we needed to add the variables that Jinja2 would use for the dynamic
data.

You could do something like a search and replace, but I feel like just
rendering a template is much easier to edit and understand. Also, the compute
time for Github Actions is free and this doesn't need to be the most
performance conscious program. Also I like Jinja2, so there is also that 🙃.

```markdown
# From README_template.md

You can see what he's posting about at <https://kjaymiller.com>.

**Latest Post - [{{latest_post.title}}]({{latest_post.link}})**

**Latest Productivity in Tech Podcast Episode - [{{latest_podcast_post.title}}]({{latest_podcast_post.link}})**

## Active Projects
```

### Step 4: Build your script to get the data and write the up to date README.md

This script is pretty simple once you know what you're looking for. I'm using
the feedparser plugin to parse the rss feeds and then returning the title and
link for the latest episode.

```python
def get_latest_post(rss_feed):
    f = feedparser.parse(rss_feed)
    latest_post = sorted(f['entries'], key=lambda x:x['published_parsed'])[-1]
    return {
            'title': latest_post['title'],
            'link': latest_post['link'],
            }
```

Then you set the template to the text of your template file.
 then write the rendered text to your README.

```python
# update readme
template = Template(Path('./README_template.md').read_text())
Path('./README.md').write_text(
        template.render(
            latest_post=get_latest_post(rss_feed),
            latest_podcast_post=get_latest_post(podcast_url),
            )
        )
```

## Step 5: Setup your Github Actions File

I'm not the best at Github Actions. Luckily for me, this action was super
simple to setup. 

You can look at the [.yml file](https://github.com/kjaymiller/kjaymiller/blob/master/.github/workflows/latest_post_readme.yml) I'm not going to talk about the setup of this
because most of it is prep stuff. Here's the important bit.

```yaml
# in steps:
- name: Install Feedparser & Jinja2
  run: pip install feedparser jinja2

- name: Update Readme
  run: python ./.github/actions/update_readme.py
```

Basically it's installing the things I need and then running the script (I
saved the script in that folder, but you don't really have to as long as its in
your repo).

After that, you add some commands to update your repo and you're off to the
races.

I have mine setup to update on a github push in that repo, but in the future I
will probably setup the file on a schedule to also update when I push something
new (Future Post...Probably).

[Productivity in Tech Podcast]: https://podcast.productivityintech.com


