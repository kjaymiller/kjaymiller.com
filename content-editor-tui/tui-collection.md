# TUI Collection Switcher Implementation Plan

## Overview
Add the ability to switch between different content collections (blog, notes, microblog) in the content editor TUI application.

## Collections to Support
Based on `routes.py`, the available collections are:
- **Blog** - PostgreSQL-backed blog posts from `blog` table
- **Notes** - PostgreSQL-backed notes from `notes` table
- **MicroBlog** - PostgreSQL-backed microblog posts from `microblog` table

## Implementation Steps

### 1. Update DatabaseManager (`content_editor/db.py`)
**Changes:**
- Add `AVAILABLE_COLLECTIONS` dictionary mapping table names to display names
- Add `current_collection` parameter to `__init__()` (default: "blog")
- Add mapping for junction table names per collection
- Update all query methods to use dynamic table and junction table names
- Methods that need updates:
  - `get_posts()` - use dynamic table name and junction table
  - `get_post()` - use dynamic table name and junction table
  - `create_post()` - insert into appropriate table and junction table
  - `update_post()` - update appropriate table and junction table
  - `delete_post()` - delete from appropriate table (cascade handles junction)
  - `get_posts_by_tag()` - query appropriate table with dynamic junction table
  - `get_tag_post_count()` - use dynamic junction table
  - Add new method `set_collection()` to switch collections at runtime

**Junction Table Mapping:**
```python
JUNCTION_TABLES = {
    "blog": "blog_tags",
    "notes": "notes_tags",
    "microblog": "microblog_tags",
}

ID_COLUMN_NAMES = {
    "blog": "blog_id",
    "notes": "notes_id",
    "microblog": "microblog_id",
}
```

**Special Handling for Microblog:**
- Microblog lacks `title` and `description` fields
- When switching to microblog:
  - `get_posts()` should not select title/description columns
  - `create_post()` should allow None for title/description or use empty strings
  - UI layer must handle missing fields gracefully

### 2. Update ContentEditorApp (`content_editor/main.py`)
**UI Changes:**
- Add a collection selector widget to display current collection in subtitle
- Bind a key (e.g., `c`) to `action_change_collection`
- Display current collection in title/subtitle (e.g., "Content Editor - Blog Posts")
- Update table columns dynamically based on collection

**App State Changes:**
- Add `current_collection` instance variable
- Add `action_change_collection()` method to show collection selection modal/screen
- Update `on_mount()` to initialize with default collection (blog)
- Add method to reload content when collection changes
- Update `populate_table()` to hide title/description columns for microblog

**Collection-Specific Column Handling:**
```
Blog/Notes:       ID | Title | Date
Microblog:        ID | Content (first 50 chars) | Date
```

### 3. Update UI Screens (`content_editor/ui.py`)
**Changes:**
- Pass `collection` parameter to DatabaseManager in all screens
- Ensure `CreatePostScreen` and `EditPostScreen` work with dynamic collection
- Handle microblog-specific UI:
  - Hide title/description input fields when editing microblog
  - Show warning if user tries to add title/description to microblog
  - Focus on content-only form for microblog
- Update field validation to account for missing fields in microblog

### 4. Add Collection Selection Modal/Screen
**New Components:**
- Create a simple selection screen in `ui.py` that:
  - Shows available collections
  - Allows user to select one
  - Returns the selected collection name
  - Callback to main app to reload with new collection

**Binding:**
- Key: `c` (Change collection)
- Shows modal with numbered options
- Updates app state and reloads posts

### 5. Tag Management (Architecture Confirmed)
**Good News:**
- ✅ Separate junction tables already exist: `blog_tags`, `notes_tags`, `microblog_tags`
- ✅ Unified `tags` table (id, name, created_at) shared across all collections
- ✅ Clean separation allows independent tag management per collection

**Implementation Notes:**
- Tag sidebar in main app will show tags for current collection only
- Filtering by tag will filter posts in current collection
- Creating tags works the same way across all collections
- Each collection has independent tag-post relationships

## File Structure
```
content-editor-tui/
├── content_editor/
│   ├── __init__.py
│   ├── main.py          (ContentEditorApp - add collection selector)
│   ├── db.py            (DatabaseManager - make collection-aware)
│   ├── ui.py            (Screens - ensure compatibility)
│   └── [...other files]
├── pyproject.toml
└── tui-collection.md    (this file)
```

## Key Decisions

1. **Collection Switching Timing**: Collection changes will reload all content from database
2. **Default Collection**: "blog" (most common use case)
3. **Tag Handling**: Dependent on database schema - needs verification
4. **UI Pattern**: Modal selection screen triggered by `c` key binding

## Testing Plan

1. **Test collection switching:**
   - Switch from blog → notes → microblog
   - Verify posts load for each collection
   - Verify tag filtering works per collection

2. **Test CRUD operations:**
   - Create post in each collection
   - Edit post in each collection
   - Delete post in each collection
   - Search in each collection

3. **Test edge cases:**
   - Empty collection handling
   - Collection with no tags
   - Search across different collections

## Database Schema (Verified)

### Table Schemas

**Blog Table:**
- id, slug, title, content, description, external_link, image_url, date, created_at, updated_at

**Notes Table:**
- id, slug, title, content, description, external_link, image_url, date, created_at, updated_at
- ✅ Matches blog schema exactly

**Microblog Table:**
- id, slug, **content**, external_link, image_url, date, created_at, updated_at
- ⚠️ **NO title or description fields** - important for UI handling

### Tag Junction Tables
- ✅ `blog_tags` (blog_id, tag_id)
- ✅ `notes_tags` (notes_id, tag_id)
- ✅ `microblog_tags` (microblog_id, tag_id)
- ✅ All share unified `tags` table (id, name, created_at)

### Key Findings
1. **Unified tags table** - All collections reference the same tags table (good architecture)
2. **Separate junction tables** - Each collection has its own junction table (clean separation)
3. **Schema differences** - Microblog lacks title and description (must handle in UI)
4. **Identical structure for blog/notes** - Can mostly copy logic between them

## Risk Assessment

**Low Risk:**
- ✅ UI changes (adding collection selector)
- ✅ DatabaseManager refactoring (straightforward with known schema)
- ✅ Tag handling (architecture already supports it)

**Medium Risk:**
- Microblog UI handling (lacks title/description fields)
- Column visibility in table (dynamic columns)

**Mitigation:**
- Test all CRUD operations for each collection
- Handle None/missing values for microblog title/description
- Test tag filtering for each collection independently
- Ensure backwards compatibility (default to blog)

**Schema Advantages:**
- Clean separation with junction tables
- Unified tags table reduces complexity
- Consistent schema for blog/notes simplifies implementation
- Cascade deletes handle cleanup automatically
