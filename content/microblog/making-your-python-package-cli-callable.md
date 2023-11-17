---
title: Making your python package CLI callable
date: 2023-11-17T01:59:43Z
tags: python
image: https://kjaymiller.azureedge.net/media/__main__dot_py.png
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

