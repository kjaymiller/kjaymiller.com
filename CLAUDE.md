# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static site generator for [kjaymiller.com](https://kjaymiller.com) built with **render-engine**, a Python-based static site framework. The site uses a hybrid architecture:

- **Markdown-based content** for blog posts, notes, and pages (stored in `content/`)
- **PostgreSQL database** for blog content (primary data source)
- **JSON data** for structured content like conferences and guest appearances
- **render-engine themes and plugins** for rendering and styling

The site generates static HTML output to the `output/` directory.

## Development Setup

### Prerequisites
- Python 3.14+
- `uv` package manager
- PostgreSQL connection (via `CONNECTION_STRING` environment variable)

### Installation
```bash
uv sync  # Install dependencies using uv lock file
```

### Environment Variables
The project requires `CONNECTION_STRING` (PostgreSQL connection URI) to be set for database operations.

## Common Commands

### Building the Site
```bash
uv run render-engine build
```
Renders all collections and pages to the `output/` directory.

### Development Server
```bash
uv run render-engine serve
```
Starts a local development server at `localhost:8000` with live reload.

### Creating New Content
```bash
uv run render-engine new-entry <collection-name>
```
Creates a new entry in a collection (e.g., `blog`, `notes`, `microblog`).

### Populating Database from Markdown
```bash
uv run populate_db.py
```
Parses markdown files from `content/` directory and inserts them into PostgreSQL. Uses frontmatter metadata (title, description, tags, date, etc.). Handles slug generation and tag linking.

### LLM-Based Content Tools
Located in `tools/`:

```bash
uv run python -m tools.agents describe <filepath>
```
Generate AI-powered descriptions for content using Claude. Use `--write --confirm` to apply changes.

```bash
uv run python -m tools.agents tag <filepath>
```
Analyze and suggest tags for content based on existing tags in the database.

```bash
uv run python -m tools.agents linkedin <filepath>
```
Generate LinkedIn post copies from blog content.

```bash
uv run python -m tools.no_tags <files>
```
Legacy tool for bulk tag assignment using LLM.

## Architecture

### Collections & Pages
Defined in `routes.py`:

- **Blog** - PostgreSQL-backed blog posts (`/blog/`) - Main content source from `blog` table
- **Notes** - Markdown-based notes (`/notes/`) - Self-contained markdown files
- **Pages** - Static markdown pages (`/pages/`) - Standalone content pages
- **MicroBlog** - Short-form content (`/microblog/`) - Microblog entries
- **Conferences** - Structured event data from JSON (`/conferences.html`)
- **GuestAppearances** - Guest appearance data from JSON (`/guest_appearances.html`)
- **AllPosts** - Aggregate feed combining MicroBlog posts

### Data Sources

- `content/` - Markdown files for blog posts, notes, and pages
- `data/` - JSON files for conferences and guest appearances
- PostgreSQL database - Primary blog content via `PGMarkdownCollectionParser`
- `settings.json` - Site configuration (navigation, branding, social links)

### Theming
- Primary theme: `render-engine-theme-kjaymiller` (custom theme)
- Additional plugins:
  - FontAwesome icons
  - Lunr search indexing
  - JSON parser for structured data
  - YouTube embed support
  - Microblog formatting
  - Sitemap generation

### Templates
Located in `templates/`:
- `blog.html` - Blog post template
- `blog_list.html` - Blog archive/listing
- `page.html` - Static page template
- `custom_index.html` - Homepage
- `conferences.html` - Conferences page
- `guest_appearances.html` - Guest appearances page
- `microblog_post.html` - Microblog entry template
- `404.html` - 404 error page
- Custom blocks for footer sections

## Database Schema

The PostgreSQL database includes:

- `blog` table - Blog posts with slug, title, content, description, date, tags
- `tags` table - Tag definitions
- `blog_tags` - Junction table linking posts to tags
- `conferences` table - Conference data with geospatial location (PostGIS)

See `schema.sql` for full schema definition.

## Code Quality & Pre-commit

Pre-commit hooks are configured in `.pre-commit-config.yaml`:

- **trailing-whitespace** - Removes trailing whitespace
- **end-of-file-fixer** - Ensures files end with newline
- **check-yaml** - Validates YAML syntax
- **check-added-large-files** - Prevents committing large files
- **frontmatter-check** - Validates markdown frontmatter in content files

Run pre-commit manually with:
```bash
uv run pre-commit run --all-files
```

## Important Notes

- The `routes.py` file uses PostgreSQL for blog content while maintaining markdown-based content for notes and pages
- Content frontmatter requires proper YAML format (title, date, description, tags, etc.)
- The site uses Markdown extras: admonitions, footnotes, fenced code blocks, header IDs, mermaid diagrams, and tables
- Markdown files in `content/` must have frontmatter with at least title and date
- The PostgreSQL integration is configured via the `CONNECTION_STRING` environment variable
- Output is generated to `output/` directory; this is a build artifact and should not be committed

If you have to run `just tui` or the command it equates to, Note that it opens a textual session that you will need to exit from after a few seconds otherwise you will stall.
