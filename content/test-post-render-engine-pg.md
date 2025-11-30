---
date: 2025-11-14 12:00:00
title: "Building Database-Driven Content with render-engine-pg"
tags: ["render-engine", "postgresql", "static-sites"]
description: "A guide to integrating PostgreSQL with render-engine using render-engine-pg to create database-driven static sites and collections."
---

I've spent a lot of time building static sites with render-engine, and I've also spent a lot of time managing databases with PostgreSQL. What if you could bring the two together? That's exactly what `render-engine-pg` does, and I think it's a game changer for how we think about static site generation.

## The Problem

When you build a static site, your content is typically stored in markdown files on disk. When you work with databases, your content lives in PostgreSQL. If you're like me, you have content in both places and want a seamless way to manage them.

render-engine-pg solves this by allowing you to:

1. Define SQL queries in your `pyproject.toml`
2. Use those queries to generate pages and collections
3. Leverage the power of SQL while keeping the simplicity of static site generation

## Getting Started

First, you'll need to install render-engine-pg:

```bash
uv pip install render-engine-pg
```

Then configure your database connection and queries in `pyproject.toml`:

```toml
[tool.render-engine.pg.read_sql]
blog = "SELECT id, title, slug, content FROM blog WHERE published = true"
```

## Using Queries in Your Site

Now you can use PostgreSQL queries directly in your render-engine collections:

```python
from render_engine_pg import PostgresQuery, PGPageParser

@site.collection
class BlogPosts(Collection):
    content_path = PostgresQuery(
        connection=db,
        collection_name="blog"
    )
    parser = PGPageParser
```

This will fetch all published blog posts from your database and generate pages for each one.

## Why This Matters

The beauty of render-engine-pg is that it bridges two worlds. You get:

- **Database flexibility**: Query and filter content however you need
- **Static site benefits**: Fast, secure, and easy to deploy
- **Markdown support**: Parse markdown with YAML frontmatter stored in your database
- **Configuration-driven approach**: All your queries live in one place

If you're building anything that combines database content with static site generation, this is worth exploring.

Have you used render-engine-pg? I'd love to hear how you're using it in your projects.

---

*This is a test post created to demonstrate the structure and capabilities of render-engine-pg.*
