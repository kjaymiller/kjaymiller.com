---
date: 2022-09-07 17:34:00
description: 'Here''s a subtle description to encourage the reader to read the blog
  post:


  "I''ve recently discovered a game-changing alternative to TailwindCSS - PyTailwindCSS.
  After switching to this Python-based tool, I was able to simplify my project setup
  and enjoy more flexibility without sacrificing performance.'
image: https://jmblogstorrage.blob.core.windows.net/media/media/pytailwindcss.png
slug: switch-to-pytailwindcss
tags:
- tailwind
- python
title: Switching from TailwindCSS to PyTailwindCSS
---

I often use [TailwindCSS](https://tailwindcss.com) for my web project and this often means that wind up with a package.json and lock-file just for tailwind.

[Jon Banafato](https://twitter.com/jonafato), my Cohost on [Python Community News](https://pythoncommunitynews.com) showed me [pytailwindcss](https://pypi.org/project/pytailwindcss/).

This will be a short post as pytailwindcss is the standalone tailwind CLI but available through pip.

## Installing and Running PyTailwindCSS

pytailwindcss makes tailwind pip-able.

`pip install pytailwindcss`

To run pytailwindcss you send the commands as you would had it been installed with NPM.

`tailwindcss -c tailwindcss.config.js -o tailwind.css --minify`

You lose access to custom plugins but you still have the ability to use the built in plugins and you can customize your settings with in your config file.

But if you're not doing much more than the custom framework, feel free to remove those `node_modules`, `package.json` and `package-lock.json` files.
