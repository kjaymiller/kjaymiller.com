---
category: meetups
date: 2021-01-28 17:00:00-08:00
description: 'Here''s a subtle description to encourage readers to read the blog post:


  "Ever found yourself on the brink of disaster after adding just one too many files
  to GitHub? Learn how to avoid the dreaded ''volcano'' effect and keep your projects
  tidy with Jay Miller''s expert tips and tricks.'
image: https://kjaymiller.s3-us-west-2.amazonaws.com/images/volcano_presentaion.jpg
slug: dont-volcano-your-project
tags: git, talks, lightning-talks
title: "How to Not \U0001F30B your Project"
youtube: https://www.youtube.com/embed/V_5FV4LkQyc
---

# Talk Slides

## Definition

> Volcano - Take a small issue in git and have it erupt into a massive issue.

---

## Example 1 #

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">WHAT YOU SHOULD NEVER DO<br><br>&quot;Me: Now to add these 2 days of code to GitHub.<br>`git add .`<br>whoops I added environment vars lets just revert...&quot;<br><br>2 days of work <a href="https://t.co/346grNXfUz">pic.twitter.com/346grNXfUz</a></p>&mdash; Jay Miller - #BlackLivesMatter (@kjaymiller) <a href="https://twitter.com/kjaymiller/status/1350241433836351489?ref_src=twsrc%5Etfw">January 16, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## How to solve this problem ##

[.column]
### If you pushed to github.  ###

Sorry gonna have to delete that repo in GH. To really clean the history.

[.column]
### If you didn't... ###

```zsh
rm -rf .git
git init
```

---

## Example 2

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Who just spent the last 3 hours trying to squash a commit (I accidentally uploaded some CSV files and it&#39;s making the pulls take much longer and they are unnecessary)<br><br>The same person that couldn&#39;t get it to work. That person.. <a href="https://t.co/ezIIlCYJmw">pic.twitter.com/ezIIlCYJmw</a></p>&mdash; Jay Miller - #BlackLivesMatter (@kjaymiller) <a href="https://twitter.com/kjaymiller/status/1338591508048408576?ref_src=twsrc%5Etfw">December 14, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

---

via @anthonypjshaw

```
git rebase -i

commit hash before the one you want to drop
```

---

## **Preventative Measures**

---

### DON'T LOAD EVERYTHING AT ONCE

`git commit <filenames> -m 'update to specific piece of code'`

Bonus Points to IDEs
- Tower
- GitHub
- PyCharm
- VSCode

---

### Before Doing Anything ⚠️

git template or git script

```sh

npx gitignore python
echo .envrc >> .gitignore
echo node_modules >> .gitignore
echo *.json *.csv >> .gitignore

```

---

<script id="asciicast-T7epmpQCjNIOevERvSkzOZmDJ" src="https://asciinema.org/a/T7epmpQCjNIOevERvSkzOZmDJ.js" async></script>

---

## No `git add .` ##

`git status` before you `git wrecked`
