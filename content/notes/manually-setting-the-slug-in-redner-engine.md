---
date: 2025-09-11 21:21:00
title: Manually Settings the file_path in Render Engine
---

Based on Dan's suggestion if you need to create a non-slugified file_path in render engine, you can just use the `file_path` attribute.


In my current site:

```python
@app.page
class _404(Page):
    template = "404.html"
    path_name = "_404.html"
```
