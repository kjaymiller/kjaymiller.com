---
title: Switching from TailwindCSS to PyTailwindCSS
slug: switch-to-pytailwindcss
date: 07 Sep 2022 10:34
tags: tailwind, python
image: https://kjaymiller.azureedge.net/media/pytailwindcss.png
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