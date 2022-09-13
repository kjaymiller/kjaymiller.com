---
title: Creating a Blog Post from Bunch, pipx, and sed
date: 05/19/21 16:59:54
tags:
---

Shell scripting is a weakness of mine. I know how to navigate a terminal and enter commands but there are a lot of things that differ in entering the commands directly or running a gamut of commands in a single script.

That said, bunch gives me a lot of reason to think about doing things with shell scripts and applescript[^1].

## Creating a Template for Blog Posts

Render Engine allows you to create a new entry in a collection. The frontmatter parser allows for consistent entry of content (in Markdown) and metadata.

```
---
title: Hello World
date: 19 May 2021 17:20
tags: test
---

Hello from the other side...

```

Anything consistent can be made into a template.

```
---
title: TITLE
date: DATE
tags:
---

CONTENT HERE

```

I can now copy this template and use it as a starting point for new posts.

But a better template will do more than just the content.

## Set the filename and title

[^1]: That includes _javascript for automation_ which is my primary way to do scripted macOS Automation
