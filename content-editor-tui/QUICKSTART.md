# Content Editor TUI - Quick Start

## 1. Install Dependencies

From the `content-editor-tui` directory:

```bash
uv sync
```

## 2. Set Up Environment

### Option A: Using .env file (Recommended)

```bash
cp .env.example .env
# Edit .env and add your PostgreSQL CONNECTION_STRING
nano .env  # or your preferred editor
```

Example `.env`:
```
CONNECTION_STRING=postgresql://user:password@localhost:5432/kjaymiller
```

Then run:
```bash
./run.sh
```

### Option B: Using environment variable

```bash
export CONNECTION_STRING="postgresql://user:password@localhost:5432/kjaymiller"
uv run content-editor
```

Or in one command:
```bash
CONNECTION_STRING="postgresql://..." uv run content-editor
```

## 3. Launch the Application

```bash
# Using the run script (if you have .env set up)
./run.sh

# Or directly
uv run content-editor
```

## Features Overview

### Main Screen (Post List)
- **Search box**: Filter posts by title, slug, or content
- **Table**: Shows all blog posts with ID, title, slug, date, and description
- **Navigation**: Use arrow keys to select posts
- **Buttons**: Edit, New, Delete, Tags

### Create/Edit Post
- **Title**: Post title (required)
- **Slug**: URL slug (required, must be unique)
- **Description**: Short summary
- **Content**: Full post content in Markdown
- **Tags**: Comma-separated tags
- **External Link**: Optional link
- **Image URL**: Optional featured image
- **Save**: Ctrl+S
- **Cancel**: Escape

### Delete Confirmation
- Confirm or cancel post deletion

### Tags Screen
- View all tags in the database
- Access via "Tags" button

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `q` | Quit application |
| `n` | New post |
| `Enter` | Edit selected post |
| `d` | Delete selected post |
| `Ctrl+S` | Save changes |
| `Escape` | Cancel/Go back |
| `↑/↓` | Navigate table |
| `Tab` | Switch fields in forms |

## Troubleshooting

**"CONNECTION_STRING environment variable not set"**
- Check that either `.env` file exists or the environment variable is set
- Run: `echo $CONNECTION_STRING` to verify

**"Failed to connect to database"**
- Verify PostgreSQL is running
- Check the connection string is correct
- Test: `psql $CONNECTION_STRING -c "SELECT 1"`

**"Table not visible or behaving strangely"**
- Try resizing your terminal window
- The table needs at least 80x20 character space

**Text area not showing all content**
- Use arrow keys or Page Up/Down to navigate through longer content
- Content is there, just not all visible at once

## File Structure

```
content-editor-tui/
├── content_editor/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # App entry point & styling
│   ├── db.py                # Database operations
│   └── ui.py                # UI screens & components
├── .env.example             # Environment template
├── .env                      # Your local config (ignored by git)
├── .gitignore               # Git ignore rules
├── pyproject.toml           # Project dependencies
├── uv.lock                  # Locked dependency versions
├── run.sh                   # Quick start script
├── README.md                # Full documentation
└── QUICKSTART.md            # This file
```

## Development

To extend or modify the application:

1. **Database operations**: Edit `content_editor/db.py`
2. **UI screens**: Edit `content_editor/ui.py`
3. **Styling**: Update CSS in `content_editor/main.py`

All changes require restarting the application.

## More Information

See `README.md` for detailed documentation.
