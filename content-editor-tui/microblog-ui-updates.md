# Microblog UI Updates - Implementation Plan

## Overview
Update the CreatePostScreen and EditPostScreen to handle microblog-specific requirements:
- Microblog doesn't have post titles
- Slug should be auto-generated from timestamp for microblog posts

## Changes Required

### 1. Update CreatePostScreen (`content_editor/ui.py`)

**Compose Method:**
- Keep all fields in the layout (no show/hide)
- Add collection awareness to determine if editing microblog
- For microblog, disable title and description fields:
  - **Blog/Notes**: Title and description inputs enabled (required)
  - **Microblog**: Title and description inputs disabled with "Field Not Implemented" label

**Field Disabling for Microblog:**
- Disable title Input widget (grayed out, not focusable)
- Disable description Input widget (grayed out, not focusable)
- Add visual indicator: "Field Not Implemented" message
- Maintain form layout consistency across all collections

**Slug Generation & Behavior:**
- For microblog (CREATE):
  - Default: Auto-generate slug from current timestamp (format: `YYYYMMDD-HHMMSS`)
  - Field: EDITABLE - User can override timestamp if desired
- For microblog (EDIT):
  - Default: Preserve existing slug (don't change timestamp)
  - Field: EDITABLE - User can change slug if desired
- For blog/notes (CREATE):
  - Default: Generate slug from title (existing behavior, if not already doing)
  - Field: EDITABLE - User can override
- For blog/notes (EDIT):
  - Default: Preserve existing slug
  - Field: EDITABLE - User can change slug with uniqueness check

**Alert on Field Activation:**
- If user somehow tries to focus/activate disabled title field for microblog:
  - Raise alert: "Title field is not implemented for Microblog posts"
  - Return focus to content field
- Same for description field:
  - Alert: "Description field is not implemented for Microblog posts"

**Validation in action_save():**
- For blog/notes: Require title and slug
- For microblog:
  - Skip title requirement (use empty string)
  - Skip manual slug entry (use generated timestamp)
  - Validate slug doesn't already exist
  - Show info message about timestamp-based slug

**UI Layout:**
```
All Collections (same layout):
- Title: [input or disabled "Field Not Implemented"]
- Slug: [input or read-only "YYYYMMDD-HHMMSS"]
- Description: [input or disabled "Field Not Implemented"]
- Tags: [input]
- Content: [textarea]
- ... rest of fields
```

### 2. Update EditPostScreen (`content_editor/ui.py`)

**Compose Method:**
- Keep all fields in layout (same as CreatePostScreen)
- Disable title and description for microblog (with "Field Not Implemented" indicator)
- Keep enabled for blog/notes

**Load Post:**
- For microblog:
  - Disable title field (grayed out, not focusable)
  - Disable description field (grayed out, not focusable)
  - Display slug as read-only (timestamp preserved)
- For blog/notes:
  - Enable title and description fields normally
  - Allow slug editing with uniqueness check

**Alert on Field Activation:**
- Same as CreatePostScreen
- If user tries to focus disabled title/description for microblog, show alert

**action_save():**
- For microblog:
  - Use empty string for title
  - Preserve existing slug (don't change timestamp)
  - Skip slug existence check if slug hasn't changed
- For blog/notes: Keep current behavior

### 3. UI Implementation Details

**Collection Detection:**
- Access `self.db.current_collection` to determine if editing microblog
- Detect in both `on_mount()` and when handling field interactions

**Timestamp Generation:**
```python
from datetime import datetime
slug = datetime.now().strftime("%Y%m%d-%H%M%S")
```

**Disabling Fields for Microblog:**
```python
if is_microblog:
    title_input = self.query_one("#title-input", Input)
    title_input.disabled = True  # Grayed out, not focusable

    description_input = self.query_one("#description-input", Input)
    description_input.disabled = True
```

**Field Placeholder Text:**
- For disabled title field: "Field Not Implemented"
- For disabled description field: "Field Not Implemented"
- Update placeholder in compose() based on collection detection in on_mount()

**Alert on Field Focus Attempt:**
```python
def on_input_focus(self, event: Input.Focused) -> None:
    """Handle input focus and alert for disabled fields."""
    input_widget = event.control

    if self.db.current_collection == "microblog":
        if input_widget.id == "title-input":
            self.app.notify("Title field is not implemented for Microblog posts", severity="warning")
            # Focus content field instead
            content_input = self.query_one("#content-input", TextArea)
            content_input.focus()

        elif input_widget.id == "description-input":
            self.app.notify("Description field is not implemented for Microblog posts", severity="warning")
            # Focus content field instead
            content_input = self.query_one("#content-input", TextArea)
            content_input.focus()
```

**Slug Field:**
- ALWAYS EDITABLE for all collections (not disabled)
- For microblog (CREATE): Default populated with timestamp, user can edit
- For microblog (EDIT): Default populated with existing slug, user can edit
- For blog/notes (CREATE): Default empty or populated from title, user can edit
- For blog/notes (EDIT): Default populated with existing slug, user can edit
- Placeholder: "url-slug" or "e.g., my-post-slug"

## Implementation Steps

### CreatePostScreen

1. **Modify compose():**
   - Keep all fields in layout (no hiding)
   - Keep IDs and structure the same
   - No changes needed here actually (logic in on_mount)

2. **Modify on_mount():**
   - Detect if current collection is microblog: `is_microblog = self.db.current_collection == "microblog"`
   - If microblog:
     - Disable title input: `self.query_one("#title-input", Input).disabled = True`
     - Disable description input: `self.query_one("#description-input", Input).disabled = True`
     - Update title placeholder to "Field Not Implemented"
     - Update description placeholder to "Field Not Implemented"
     - Auto-generate slug: `slug = datetime.now().strftime("%Y%m%d-%H%M%S")`
     - Set slug input value to generated slug (KEEP EDITABLE)
     - Keep slug input ENABLED (not disabled)
   - If blog/notes:
     - Keep title, description, and slug inputs ENABLED (existing behavior)

3. **Add Input focus handler:**
   - Implement `on_input_focus()` event handler (see code example above)
   - Alert and redirect focus if user tries to focus disabled fields for microblog

4. **Modify action_save():**
   - Conditional validation:
     ```python
     if self.db.current_collection == "microblog":
         title = ""  # Empty string for microblog
         slug = self.query_one("#slug-input", Input).value  # Use generated slug
         # Skip title requirement check
     else:
         title = self.query_one("#title-input", Input).value
         slug = self.query_one("#slug-input", Input).value
         # Require title and slug
     ```

### EditPostScreen

1. **Modify on_mount() (after load_post()):**
   - Same disable logic as CreatePostScreen for title and description
   - For microblog:
     - Disable title and description inputs (with "Field Not Implemented" placeholders)
     - Keep slug input ENABLED (editable)
     - Slug will be populated by load_post() with existing slug (no changes needed)

2. **Modify load_post():**
   - Handle empty title gracefully for microblog (already returns empty string from db)
   - Slug is populated with existing value (no special handling needed)

3. **Add Input focus handler:**
   - Same as CreatePostScreen

4. **Modify action_save():**
   - Same conditional validation as CreatePostScreen
   - For microblog:
     - Use empty string for title
     - Use slug value from input (allows user to have changed it)
     - Preserve original slug if not changed, allow change with uniqueness check

## Code Changes Summary

### Key Methods to Modify

**CreatePostScreen:**
- `on_mount()` - Disable fields for microblog, auto-generate slug
- `on_input_focus()` - NEW - Alert and redirect focus for disabled fields
- `action_save()` - Conditional validation based on collection

**EditPostScreen:**
- `on_mount()` - Disable fields for microblog after loading post
- `on_input_focus()` - NEW - Alert and redirect focus for disabled fields
- `action_save()` - Conditional validation based on collection

### Helper Code
```python
from datetime import datetime

# In CreatePostScreen.on_mount():
is_microblog = self.db.current_collection == "microblog"
if is_microblog:
    # Disable title and description only
    self.query_one("#title-input", Input).disabled = True
    self.query_one("#description-input", Input).disabled = True

    # Update placeholders for disabled fields
    self.query_one("#title-input", Input).placeholder = "Field Not Implemented"
    self.query_one("#description-input", Input).placeholder = "Field Not Implemented"

    # Auto-generate slug for microblog (but keep it EDITABLE)
    slug = datetime.now().strftime("%Y%m%d-%H%M%S")
    self.query_one("#slug-input", Input).value = slug
    # DO NOT disable slug input - leave it editable
```

```python
# In both CreatePostScreen and EditPostScreen - new event handler:
def on_input_focus(self, event: Input.Focused) -> None:
    """Handle input focus and alert for disabled fields."""
    input_widget = event.control

    if self.db.current_collection == "microblog":
        if input_widget.id == "title-input":
            self.app.notify("Title field is not implemented for Microblog posts", severity="warning")
            # Focus content field instead
            self.query_one("#content-input", TextArea).focus()

        elif input_widget.id == "description-input":
            self.app.notify("Description field is not implemented for Microblog posts", severity="warning")
            # Focus content field instead
            self.query_one("#content-input", TextArea).focus()
```

## UI/UX Considerations

1. **Visual Feedback:**
   - Disabled title/description fields appear grayed out in Textual
   - "Field Not Implemented" placeholder clearly indicates why fields are disabled
   - Slug field appears NORMAL/EDITABLE for all collections
   - Consistent layout across all collections (no layout shifts)
   - Slug has sensible defaults (timestamp for microblog create, existing slug for edit)

2. **User Alerts:**
   - If user accidentally tries to focus disabled title/description:
     - Clear warning alert: "Title/Description field is not implemented for Microblog posts"
     - Auto-focus redirects to content field
     - User understands why and what to do next

3. **Slug Field Behavior:**
   - Always editable for all collections
   - Microblog CREATE: Pre-populated with timestamp, user can change it
   - Microblog EDIT: Pre-populated with existing slug, user can change it
   - Blog/Notes: Existing behavior preserved
   - Uniqueness validation applied when saving

4. **Accessibility:**
   - Disabled fields are properly marked (screen readers understand)
   - Placeholders provide context
   - Focus redirection is smooth and predictable
   - Slug field is fully accessible and editable

5. **Consistency:**
   - Same form layout for all collections
   - Field disabling is clear and consistent (only title/description for microblog)
   - Slug always available for user control
   - No hidden complexity or confusing UI changes

## Testing Plan

1. **Create Microblog Post:**
   - Verify title field is DISABLED with "Field Not Implemented" placeholder
   - Verify description field is DISABLED with "Field Not Implemented" placeholder
   - Verify slug field is ENABLED and pre-populated with timestamp
   - Verify slug field is EDITABLE (user can change it)
   - Verify attempting to focus title/description shows alert
   - Verify alert redirects focus to content field
   - Verify post creates successfully with empty title and custom slug (if changed)
   - Verify slug is unique (timestamp-based by default)

2. **Edit Microblog Post:**
   - Verify title field is DISABLED
   - Verify description field is DISABLED
   - Verify slug field is ENABLED with existing slug pre-populated
   - Verify slug field is EDITABLE (user can change it)
   - Verify can edit content, tags, etc.
   - Verify save allows slug change with uniqueness check
   - Verify save preserves slug if unchanged

3. **Create Blog/Notes Post:**
   - Verify title field is ENABLED and required
   - Verify description field is ENABLED
   - Verify slug field is ENABLED
   - Verify existing behavior unchanged
   - Verify all fields are editable

4. **Edit Blog/Notes Post:**
   - Verify title/description/slug all ENABLED
   - Verify can change slug (with uniqueness check)
   - Verify existing behavior unchanged
   - Verify all fields are editable

5. **Focus Attempts:**
   - Click/focus title field in microblog → Alert appears
   - Click/focus description field in microblog → Alert appears
   - Focus automatically redirects to content field

## Files to Modify
- `content_editor/ui.py` - CreatePostScreen and EditPostScreen classes only

## Risk Assessment
- **Low Risk**: Changes are isolated to UI layer
- **Low Risk**: DB layer already handles empty titles for microblog
- **Low Risk**: Slug validation already exists in DB layer
- **Testing**: Need manual testing of microblog forms in TUI
- **No breaking changes**: Blog/Notes behavior remains unchanged

## Notes
- Timestamp slug format: `YYYYMMDD-HHMMSS` (e.g., `20251105-143022`)
- Second precision is sufficient for uniqueness (very rare collisions possible)
- If collision occurs (same second), user can manually change slug
- Slug format must match database schema constraints (VARCHAR 255 is fine)
- Slug field always remains EDITABLE - user has full control
- Only title and description are disabled for microblog
- Disabled fields show "Field Not Implemented" placeholder text
- Alerts help users understand why fields are disabled and guide them to valid fields
