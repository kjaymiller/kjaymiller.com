---
title: How to disable the markdown extras in Lazy NVIM
tags: ["nvim"]
description: This was getting on my nerves
date: 2025-06-16T10:08:29
---

While working on the update on <https://kjaymiller.com/blog/i-am-no-longer-a-developer-advocate.html>, The RST-style admonitions kept breaking. This wasn't the first time this had happened.

So to fix this I just disabled the Markdown Extras for a bit until I can better diagnose.

## How to do disable the extras

- Open the extras with `:LazyExtras`
- Find the line with markdown language extras
- press `x`
- restart NVIM
