# Content Editor TUI

A terminal user interface for editing blog content stored in PostgreSQL. Built with [Textual](https://textual.textualize.io/).

## Features

- **Browse Posts**: View all blog posts in a sortable, searchable table
- **Search**: Full-text search across post titles, slugs, and content
- **Create**: Add new blog posts with metadata
- **Edit**: Modify existing posts (title, slug, content, description, tags, images, links)
- **Delete**: Remove posts with confirmation
- **Tag Management**: View and manage all tags in the database
- **Validation**: Slug uniqueness checking and required field validation

## Installation

1. Navigate to the TUI directory:
```bash
cd content-editor-tui
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Set up your environment:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL CONNECTION_STRING
```

## Usage

Run the application:

```bash
# From the content-editor-tui directory
uv run content-editor

# Or directly with Python if installed in virtual environment
.venv/bin/content-editor
```

The application requires the `CONNECTION_STRING` environment variable pointing to your PostgreSQL database.

## Navigation

### Post List Screen (Main)
- **Search**: Type in the search field to filter posts
- **Up/Down**: Navigate through the posts table
- **Enter**: Open selected post for editing
- **n**: Create a new post
- **d**: Delete selected post
- **Tags button**: View all tags in database
- **Edit button**: Edit selected post
- **New button**: Create a new post
- **Delete button**: Delete selected post
- **q**: Quit application

### Create/Edit Post Screens
- **Fields**: Title, slug, description, content (markdown), tags, external link, image URL
- **Ctrl+S**: Save the post
- **Escape**: Cancel without saving
- **Tab**: Move between fields (in text input areas)

### Delete Confirmation
- **Delete button**: Confirm deletion
- **Cancel button**: Abort deletion

### Tags Screen
- View all tags in the database
- **Escape**: Return to post list

## Database Schema

The application expects the following tables:
- `blog` - Blog posts with title, slug, content, description, metadata
- `tags` - Tag definitions
- `blog_tags` - Junction table linking posts to tags

See the main project's `schema.sql` for the full schema.

## Project Structure

```
content-editor-tui/
├── content_editor/
│   ├── __init__.py
│   ├── main.py          # Application entry point and styling
│   ├── db.py            # Database operations
│   └── ui.py            # UI screens and components
├── pyproject.toml       # Project configuration
├── .env.example         # Environment variable template
└── README.md            # This file
```

## Development

The project uses:
- **Textual**: Modern Python TUI framework
- **psycopg**: PostgreSQL adapter
- **Python 3.10+**: Requires Python 3.10 or later

## Keyboard Shortcuts Summary

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `n` | New post |
| `Enter` | Edit selected post |
| `d` | Delete selected post |
| `Ctrl+S` | Save changes |
| `Escape` | Cancel/Go back |
| `↑/↓` | Navigate list |

## Troubleshooting

### "CONNECTION_STRING environment variable not set"
Make sure you've set the `CONNECTION_STRING` environment variable before running the app:
```bash
export CONNECTION_STRING="postgresql://user:password@localhost:5432/database"
```

### "Failed to connect to database"
Verify that:
- PostgreSQL is running
- The connection string is correct
- Your database exists and tables are created (run the parent project's schema setup)

### Text area not showing content
Use arrow keys to navigate within text areas. The content is there even if not fully visible.
