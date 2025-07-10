---
date: 2023-11-17 01:59:43
description: 'Here''s a subtle description to encourage the reader to read the blog
  post:


  "I recently discovered a convenient way to turn my Python package into a CLI. Want
  to learn how I did it?'
image: https://jmblogstorrage.blob.core.windows.net/media/__main__dot_py.png
tags:
- python
title: Making your python package CLI callable
---

Render Engine has a cli that can be called with `render-engine --help` or `python -m render_engine --help`.

To do the first command you need to have a `[project.scripts]` that points to the code being called. Render engine's cli is in cli.py and can be called with the `cli` function.

```python
[project.scripts]
render-engine = "render_engine.cli:cli"

```

To do the `python -m` version, you need to add a call to your code in a `__main__.py` file.  Since I'm using typer I can just call the app directly.

```python
"""
Enables the use of `python -m render_engine` to run the CLI.
"""

from .cli import app

if __name__ == "__main__":
    app()
```
