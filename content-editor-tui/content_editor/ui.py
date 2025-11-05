"""UI screens for modals and secondary screens."""

from datetime import datetime
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.widgets import (
    Static,
    Input,
    TextArea,
    Button,
    Label,
    ListView,
    ListItem,
    DataTable,
    Markdown,
)
from textual.binding import Binding
from textual.screen import Screen, ModalScreen

from .db import DatabaseManager


class SearchModal(ModalScreen):
    """Modal screen for searching posts."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]

    CSS = """
    SearchModal {
        align: center middle;
    }

    SearchModal > Vertical {
        width: 60;
        height: 7;
        border: solid $accent;
        background: $panel;
    }
    """

    def __init__(self, on_search):
        """Initialize the search modal."""
        super().__init__()
        self.on_search = on_search

    def compose(self) -> ComposeResult:
        """Compose the search modal."""
        yield Vertical(
            Static("Search Posts"),
            Input(
                id="search-modal-input",
                placeholder="Enter search term (press Enter to search)",
            ),
        )

    def on_mount(self):
        """Mount the modal."""
        self.title = "Search"
        input_widget = self.query_one("#search-modal-input", Input)
        input_widget.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search submission."""
        if event.input.id == "search-modal-input":
            search_term = event.input.value.strip()
            self.on_search(search_term if search_term else None)
            self.app.pop_screen()

    def action_cancel(self):
        """Cancel the search."""
        self.app.pop_screen()


class CreatePostScreen(Screen):
    """Screen for creating a new blog post."""

    BINDINGS = [
        Binding("ctrl+s", "save", "Save", show=True),
        Binding("escape", "quit_screen", "Cancel", show=True),
    ]

    def __init__(self, db: DatabaseManager, on_created):
        """Initialize the create post screen."""
        super().__init__()
        self.db = db
        self.on_created = on_created

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        yield Horizontal(
            ScrollableContainer(
                Vertical(
                    Static("Title:"),
                    Input(id="title-input", placeholder="Post title"),
                    Static("Slug:"),
                    Input(id="slug-input", placeholder="url-slug"),
                    Static("Description:"),
                    Input(id="description-input", placeholder="Short description"),
                    Static("Tags (comma-separated):"),
                    Input(id="tags-input", placeholder="tag1, tag2, tag3"),
                    Static("External Link (optional):"),
                    Input(id="external-link-input", placeholder="https://example.com"),
                    Static("Image URL (optional):"),
                    Input(
                        id="image-url-input",
                        placeholder="https://example.com/image.jpg",
                    ),
                    Horizontal(
                        Button("Save", id="save-btn", variant="primary"),
                        Button("Cancel", id="cancel-btn"),
                    ),
                    id="form-sidebar",
                ),
                id="sidebar-container",
            ),
            Vertical(
                Static("Content:"),
                TextArea(id="content-input", language="markdown"),
                id="content-container",
            ),
        )

    def on_mount(self):
        """Mount the screen."""
        self.title = "Create New Post"

        # Handle collection-specific field configuration
        is_microblog = self.db.current_collection == "microblog"

        if is_microblog:
            # Disable title and description for microblog
            title_input = self.query_one("#title-input", Input)
            title_input.disabled = True
            title_input.placeholder = "Field Not Implemented"

            description_input = self.query_one("#description-input", Input)
            description_input.disabled = True
            description_input.placeholder = "Field Not Implemented"

            # Auto-generate slug from timestamp for microblog (but keep it editable)
            slug = datetime.now().strftime("%Y%m%d-%H%M%S")
            slug_input = self.query_one("#slug-input", Input)
            slug_input.value = slug

    def on_input_focus(self, event: Input.Focused) -> None:
        """Handle input focus and alert for disabled fields in microblog."""
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

    def action_save(self):
        """Save the new post."""
        try:
            is_microblog = self.db.current_collection == "microblog"

            title = self.query_one("#title-input", Input).value
            slug = self.query_one("#slug-input", Input).value
            description = self.query_one("#description-input", Input).value
            content = self.query_one("#content-input", TextArea).text
            tags_str = self.query_one("#tags-input", Input).value
            external_link = self.query_one("#external-link-input", Input).value or None
            image_url = self.query_one("#image-url-input", Input).value or None

            # Conditional validation based on collection
            if is_microblog:
                # For microblog: title is empty, but slug and content are required
                if not slug or not content:
                    self.app.notify(
                        "Slug and content are required", severity="error"
                    )
                    return
                title = ""  # Force empty title for microblog
                description = ""  # Force empty description for microblog
            else:
                # For blog/notes: title, slug, and content are required
                if not title or not slug or not content:
                    self.app.notify(
                        "Title, slug, and content are required", severity="error"
                    )
                    return

            if self.db.slug_exists(slug):
                self.app.notify("Slug already exists", severity="error")
                return

            tags = [t.strip() for t in tags_str.split(",") if t.strip()]

            post_id = self.db.create_post(
                slug=slug,
                title=title,
                content=content,
                description=description,
                external_link=external_link,
                image_url=image_url,
                tags=tags,
            )

            self.on_created(post_id)
            self.app.pop_screen()
        except Exception as e:
            self.app.notify(f"Error creating post: {e}", severity="error")

    def action_quit_screen(self):
        """Quit the screen without saving."""
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-btn":
            self.action_save()
        elif event.button.id == "cancel-btn":
            self.action_quit_screen()


class EditPostScreen(Screen):
    """Screen for editing a blog post."""

    BINDINGS = [
        Binding("ctrl+s", "save", "Save", show=True),
        Binding("escape", "quit_screen", "Cancel", show=True),
    ]

    def __init__(self, db: DatabaseManager, post_id: int, on_updated):
        """Initialize the edit post screen."""
        super().__init__()
        self.db = db
        self.post_id = post_id
        self.post = None
        self.on_updated = on_updated

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        yield Horizontal(
            ScrollableContainer(
                Vertical(
                    Static("Title:"),
                    Input(id="title-input", placeholder="Post title"),
                    Static("Slug:"),
                    Input(id="slug-input", placeholder="url-slug"),
                    Static("Description:"),
                    Input(id="description-input", placeholder="Short description"),
                    Static("Tags (comma-separated):"),
                    Input(id="tags-input", placeholder="tag1, tag2, tag3"),
                    Static("External Link (optional):"),
                    Input(id="external-link-input", placeholder="https://example.com"),
                    Static("Image URL (optional):"),
                    Input(
                        id="image-url-input",
                        placeholder="https://example.com/image.jpg",
                    ),
                    Horizontal(
                        Button("Save", id="save-btn", variant="primary"),
                        Button("Cancel", id="cancel-btn"),
                    ),
                    id="form-sidebar",
                ),
                id="sidebar-container",
            ),
            Vertical(
                Static("Content:"),
                TextArea(id="content-input", language="markdown"),
                id="content-container",
            ),
        )

    def on_mount(self):
        """Mount the screen."""
        self.title = "Edit Post"
        self.load_post()

        # Handle collection-specific field configuration
        is_microblog = self.db.current_collection == "microblog"

        if is_microblog:
            # Disable title and description for microblog
            title_input = self.query_one("#title-input", Input)
            title_input.disabled = True
            title_input.placeholder = "Field Not Implemented"

            description_input = self.query_one("#description-input", Input)
            description_input.disabled = True
            description_input.placeholder = "Field Not Implemented"

    def load_post(self):
        """Load the post from the database."""
        try:
            self.post = self.db.get_post(self.post_id)
            if self.post:
                self.query_one("#title-input", Input).value = self.post["title"]
                self.query_one("#slug-input", Input).value = self.post["slug"]
                self.query_one("#description-input", Input).value = (
                    self.post["description"] or ""
                )
                self.query_one("#content-input", TextArea).text = self.post["content"]
                tags = ", ".join([t["name"] for t in self.post["tags"]])
                self.query_one("#tags-input", Input).value = tags
                self.query_one("#external-link-input", Input).value = (
                    self.post["external_link"] or ""
                )
                self.query_one("#image-url-input", Input).value = (
                    self.post["image_url"] or ""
                )
        except Exception as e:
            self.app.notify(f"Error loading post: {e}", severity="error")

    def on_input_focus(self, event: Input.Focused) -> None:
        """Handle input focus and alert for disabled fields in microblog."""
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

    def action_save(self):
        """Save the post."""
        try:
            is_microblog = self.db.current_collection == "microblog"

            title = self.query_one("#title-input", Input).value
            slug = self.query_one("#slug-input", Input).value
            description = self.query_one("#description-input", Input).value
            content = self.query_one("#content-input", TextArea).text
            tags_str = self.query_one("#tags-input", Input).value
            external_link = self.query_one("#external-link-input", Input).value or None
            image_url = self.query_one("#image-url-input", Input).value or None

            # Conditional validation based on collection
            if is_microblog:
                # For microblog: slug and content are required
                if not slug or not content:
                    self.app.notify(
                        "Slug and content are required", severity="error"
                    )
                    return
                title = ""  # Force empty title for microblog
                description = ""  # Force empty description for microblog
            else:
                # For blog/notes: title, slug, and content are required
                if not title or not slug or not content:
                    self.app.notify(
                        "Title, slug, and content are required", severity="error"
                    )
                    return

            if slug != self.post["slug"] and self.db.slug_exists(slug, self.post_id):
                self.app.notify("Slug already exists", severity="error")
                return

            tags = [t.strip() for t in tags_str.split(",") if t.strip()]

            self.db.update_post(
                self.post_id,
                slug=slug,
                title=title,
                content=content,
                description=description,
                external_link=external_link,
                image_url=image_url,
                tags=tags,
            )

            self.on_updated()
            self.app.pop_screen()
        except Exception as e:
            self.app.notify(f"Error saving post: {e}", severity="error")

    def action_quit_screen(self):
        """Quit the screen without saving."""
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-btn":
            self.action_save()
        elif event.button.id == "cancel-btn":
            self.action_quit_screen()


class ConfirmDeleteScreen(Screen):
    """Screen for confirming deletion."""

    def __init__(self, post_title: str, on_confirm):
        """Initialize the confirm delete screen."""
        super().__init__()
        self.post_title = post_title
        self.on_confirm = on_confirm

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        yield Vertical(
            Static(f'Delete "{self.post_title}"?', classes="title"),
            Static("This action cannot be undone."),
            Horizontal(
                Button("Delete", id="confirm-btn", variant="error"),
                Button("Cancel", id="cancel-btn"),
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "confirm-btn":
            self.on_confirm()
            self.app.pop_screen()
        elif event.button.id == "cancel-btn":
            self.app.pop_screen()


class TagsScreen(Screen):
    """Screen for viewing and managing tags."""

    BINDINGS = [
        Binding("escape", "quit_screen", "Back", show=True),
        Binding("r", "rename_tag", "Rename", show=True),
        Binding("d", "delete_tag", "Delete", show=True),
    ]

    def __init__(self, db: DatabaseManager):
        """Initialize the tags screen."""
        super().__init__()
        self.db = db
        self.selected_tag_id = None
        self.tags = []
        self.current_posts = []

    def compose(self) -> ComposeResult:
        """Compose the screen with three-pane layout."""
        yield Vertical(
            Horizontal(
                Vertical(
                    Static("Tags"),
                    DataTable(id="tags-table"),
                    id="tags-pane",
                ),
                Vertical(
                    Static("Posts"),
                    DataTable(id="posts-table"),
                    Markdown(
                        "Select a post to preview",
                        id="post-preview-content",
                    ),
                    id="posts-pane",
                ),
                id="content-area",
            ),
            Horizontal(
                Button("Rename", id="rename-btn", variant="primary"),
                Button("Delete", id="delete-btn", variant="error"),
                Button("Back", id="back-btn"),
            ),
        )

    def on_mount(self):
        """Mount the screen."""
        self.title = "Tag Management"
        self.load_tags()
        tags_table = self.query_one("#tags-table", DataTable)
        tags_table.cursor_type = "row"
        tags_table.focus()
        if self.tags:
            self.load_posts_for_tag(self.tags[0]["id"])

    def load_tags(self):
        """Load tags from database."""
        try:
            self.tags = self.db.get_all_tags()
            table = self.query_one("#tags-table", DataTable)
            table.clear()
            table.add_columns("Tag Name", "Posts")

            for tag in self.tags:
                post_count = self.db.get_tag_post_count(tag["id"])
                table.add_row(tag["name"], str(post_count), key=str(tag["id"]))
        except Exception as e:
            self.app.notify(f"Error loading tags: {e}", severity="error")

    def load_posts_for_tag(self, tag_id: int):
        """Load posts for the selected tag."""
        try:
            posts = self.db.get_posts_by_tag(tag_id)
            self.current_posts = posts
            table = self.query_one("#posts-table", DataTable)
            table.clear()
            table.add_columns("Title", "Date")

            for post in posts:
                date_str = post["date"].strftime("%Y-%m-%d") if post["date"] else "N/A"
                table.add_row(post["title"], date_str, key=str(post["id"]))

            self.update_post_preview()
        except Exception as e:
            self.app.notify(f"Error loading posts: {e}", severity="error")

    def action_quit_screen(self):
        """Quit the screen."""
        self.app.pop_screen()

    def action_rename_tag(self):
        """Rename the selected tag."""
        tags_table = self.query_one("#tags-table", DataTable)
        cursor_row = tags_table.cursor_row

        if cursor_row is None or cursor_row >= len(self.tags):
            self.app.notify("No tag selected", severity="warning")
            return

        tag = self.tags[cursor_row]
        self.app.push_screen(
            RenameTagScreen(
                tag["id"],
                tag["name"],
                self.db,
                self.on_tag_renamed,
            )
        )

    def action_delete_tag(self):
        """Delete the selected tag."""
        tags_table = self.query_one("#tags-table", DataTable)
        cursor_row = tags_table.cursor_row

        if cursor_row is None or cursor_row >= len(self.tags):
            self.app.notify("No tag selected", severity="warning")
            return

        tag = self.tags[cursor_row]
        self.app.push_screen(
            ConfirmDeleteTagScreen(
                tag["name"],
                lambda: self.confirm_delete_tag(tag["id"]),
            )
        )

    def confirm_delete_tag(self, tag_id: int):
        """Confirm and delete a tag."""
        try:
            self.db.delete_tag(tag_id)
            self.app.notify("Tag deleted successfully", severity="information")
            self.load_tags()
            posts_table = self.query_one("#posts-table", DataTable)
            posts_table.clear()
        except Exception as e:
            self.app.notify(f"Error deleting tag: {e}", severity="error")

    def on_tag_renamed(self):
        """Handle tag rename."""
        self.load_tags()
        tags_table = self.query_one("#tags-table", DataTable)
        if tags_table.cursor_row is not None and tags_table.cursor_row < len(self.tags):
            self.load_posts_for_tag(self.tags[tags_table.cursor_row]["id"])

    def update_post_preview(self):
        """Update the preview panel with the currently selected post."""
        posts_table = self.query_one("#posts-table", DataTable)
        preview = self.query_one("#post-preview-content", Markdown)

        if (
            self.current_posts
            and posts_table.cursor_row is not None
            and posts_table.cursor_row < len(self.current_posts)
        ):
            post = self.current_posts[posts_table.cursor_row]
            full_post = self.db.get_post(post["id"])

            if full_post.get("content"):
                content_preview = full_post["content"]
            else:
                content_preview = "No content available"
            preview.update(f"# {post['title']}\n\n{content_preview}")
        else:
            preview.update("Select a post to preview")

    def on_data_table_row_selected(self, event):
        """Update preview when row is selected or cursor moves."""
        if event.control.id == "posts-table":
            self.update_post_preview()

    def on_data_table_row_highlighted(self, event):
        """Update posts list when a tag is highlighted."""
        if event.control.id == "tags-table":
            if event.cursor_row is not None and event.cursor_row < len(self.tags):
                tag_id = self.tags[event.cursor_row]["id"]
                self.selected_tag_id = tag_id
                self.load_posts_for_tag(tag_id)
        elif event.control.id == "posts-table":
            self.update_post_preview()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "rename-btn":
            self.action_rename_tag()
        elif event.button.id == "delete-btn":
            self.action_delete_tag()
        elif event.button.id == "back-btn":
            self.action_quit_screen()


class RenameTagScreen(Screen):
    """Screen for renaming a tag."""

    BINDINGS = [
        Binding("ctrl+s", "save", "Save", show=True),
        Binding("escape", "quit_screen", "Cancel", show=True),
    ]

    def __init__(self, tag_id: int, current_name: str, db: DatabaseManager, on_renamed):
        """Initialize the rename tag screen."""
        super().__init__()
        self.tag_id = tag_id
        self.current_name = current_name
        self.db = db
        self.on_renamed = on_renamed

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        yield Vertical(
            Static(f'Rename tag "{self.current_name}"', classes="title"),
            Static("New tag name:"),
            Input(id="new-name-input", placeholder="Enter new tag name"),
            Horizontal(
                Button("Save", id="save-btn", variant="primary"),
                Button("Cancel", id="cancel-btn"),
            ),
        )

    def on_mount(self):
        """Mount the screen."""
        self.title = "Rename Tag"
        input_widget = self.query_one("#new-name-input", Input)
        input_widget.value = self.current_name
        input_widget.focus()

    def action_save(self):
        """Save the new tag name."""
        try:
            new_name = self.query_one("#new-name-input", Input).value.strip()

            if not new_name:
                self.app.notify("Tag name cannot be empty", severity="error")
                return

            if new_name == self.current_name:
                self.app.notify("No changes made", severity="information")
                self.app.pop_screen()
                return

            self.db.rename_tag(self.tag_id, new_name)
            self.app.notify(f"Tag renamed to '{new_name}'", severity="information")
            self.on_renamed()
            self.app.pop_screen()
        except Exception as e:
            self.app.notify(f"Error renaming tag: {e}", severity="error")

    def action_quit_screen(self):
        """Quit the screen without saving."""
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-btn":
            self.action_save()
        elif event.button.id == "cancel-btn":
            self.action_quit_screen()


class ConfirmDeleteTagScreen(Screen):
    """Screen for confirming tag deletion."""

    def __init__(self, tag_name: str, on_confirm):
        """Initialize the confirm delete screen."""
        super().__init__()
        self.tag_name = tag_name
        self.on_confirm = on_confirm

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        yield Vertical(
            Static(f'Delete tag "{self.tag_name}"?', classes="title"),
            Static("This action cannot be undone."),
            Horizontal(
                Button("Delete", id="confirm-btn", variant="error"),
                Button("Cancel", id="cancel-btn"),
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "confirm-btn":
            self.on_confirm()
            self.app.pop_screen()
        elif event.button.id == "cancel-btn":
            self.app.pop_screen()


class CollectionSelectScreen(ModalScreen):
    """Modal screen for selecting a collection."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]

    CSS = """
    CollectionSelectScreen {
        align: center middle;
    }

    CollectionSelectScreen > Vertical {
        width: 50;
        height: 15;
        border: solid $accent;
        background: $panel;
    }

    #collection-list {
        height: 8;
    }
    """

    def __init__(self, on_collection_selected):
        """Initialize the collection selection modal.

        Args:
            on_collection_selected: Callback function that receives the selected collection name
        """
        super().__init__()
        self.on_collection_selected = on_collection_selected

    def compose(self) -> ComposeResult:
        """Compose the collection selection modal."""
        yield Vertical(
            Static("Select Collection", classes="title"),
            ListView(id="collection-list"),
        )

    def on_mount(self):
        """Mount the modal and populate collections."""
        self.title = "Change Collection"
        list_view = self.query_one("#collection-list", ListView)

        # Add available collections from DatabaseManager
        for collection_name, collection_display in DatabaseManager.AVAILABLE_COLLECTIONS.items():
            label = Label(collection_display, id=f"collection-{collection_name}")
            list_item = ListItem(label, id=collection_name)
            list_view.append(list_item)

        # Focus the list
        list_view.focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle collection selection."""
        selected_item = event.item
        if selected_item and selected_item.id:
            self.on_collection_selected(selected_item.id)
            self.app.pop_screen()

    def action_cancel(self):
        """Cancel the selection."""
        self.app.pop_screen()
