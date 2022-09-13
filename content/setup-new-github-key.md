---
title: Setup New Github Key
category: code
tags: github, server, new machine
date: 24 Mar 2021 14:22
---

Another note that I wind up having to look up every time.

```
ssh-keygen -t rsa -b 4096 -C "<YOUR EMAIL>"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
pbcopy < ~/.ssh/id_rsa.pub
open https://github.com/settings/keys
```
