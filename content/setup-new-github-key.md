---
category: code
date: 2021-03-24 14:22:00-07:00
description: I recently set up a new GitHub key on my freshly acquired server - now
  I wish I had written this down sooner.
tags: github, server, new machine
title: Setup New Github Key
---

Another note that I wind up having to look up every time.

```
ssh-keygen -t rsa -b 4096 -C "<YOUR EMAIL>"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
pbcopy < ~/.ssh/id_rsa.pub
open https://github.com/settings/keys
```