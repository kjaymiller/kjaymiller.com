"""Main TUI application."""

from typing import Optional
from textual.app import ComposeResult, App
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import (
    Header,
    Footer,
    Static,
    DataTable,
    MarkdownViewer,
    Label,
    ListView,
    ListItem,
)
from textual.binding import Binding

from .db import DatabaseManager


class ContentEditorApp(App):
    """Main application."""

    BINDINGS = [
        Binding("e", "edit_post", "Edit", show=True),
        Binding("n", "new_post", "New", show=True),
        Binding("d", "delete_post", "Delete", show=True),
        Binding("/", "search", "Search", show=True),
        Binding("c", "change_collection", "Collection", show=True),
        Binding("r", "reset", "Reset", show=True),
        Binding("q", "app.quit", "Quit", show=True),
    ]

    CSS = """
    #preview-content {
        height: 80%;
        overflow: auto;
    }

    #posts-table {
        width: 75%;
    }

    #tags-sidebar-list {
        width: 25;
    }

    #sidebar-container {
        width: 50;
    }
    """

    def __init__(self):
        """Initialize the app."""
        super().__init__()
        self.db = DatabaseManager()
        self.current_post = None
        self.posts = []
        self.tags = []
        self.selected_tag_id = None
        self.current_collection = "blog"  # Default collection

    def compose(self) -> ComposeResult:
        """Compose the app."""
        yield Header()
        yield MarkdownViewer(
            "Select a post to preview",
            id="preview-content",
            show_table_of_contents=False,
        )
        yield Horizontal(
            DataTable(id="posts-table"),
            ListView(id="tags-sidebar-list"),
        )
        yield Footer()

    def on_mount(self) -> None:
        """App mounted."""
        try:
            self.title = "Content Editor"
            self._update_subtitle()
            self.load_posts()
            self.load_tags_sidebar()
            table = self.query_one("#posts-table", DataTable)
            table.focus()
        except Exception as e:
            self.title = "Content Editor"
            error_message = f"Error: {e}"
            self.sub_title = error_message
            self.notify(error_message, severity="error")

    def _update_subtitle(self) -> None:
        """Update the subtitle to show current collection."""
        collection_display = self.db.AVAILABLE_COLLECTIONS.get(
            self.current_collection, self.current_collection
        )
        self.sub_title = f"Editing {collection_display}"

    def load_posts(self, search: Optional[str] = None):
        """Load posts from database."""
        try:
            self.posts = self.db.get_posts(search)
            self.populate_table()
        except Exception as e:
            self.notify(f"Error loading posts: {e}", severity="error")

    def populate_table(self):
        """Populate the data table with posts.

        Collection-specific column handling:
        - Blog/Notes: ID | Title | Date
        - Microblog: ID | Content Preview | Date
        """
        table = self.query_one("#posts-table", DataTable)
        table.clear(columns=True)
        table.cursor_type = "row"

        # Add columns based on collection
        if self.current_collection == "microblog":
            table.add_columns(
                "ID",
                "Content",
                "Date",
            )
        else:
            table.add_columns(
                "ID",
                "Title",
                "Date",
            )

        # Add rows
        for post in self.posts:
            date_str = post["date"].strftime("%Y-%m-%d") if post["date"] else "N/A"
            if self.current_collection == "microblog":
                # For microblog, show content preview (description field has content preview)
                content_preview = post["description"][:50] if post["description"] else "(empty)"
                table.add_row(
                    str(post["id"]),
                    content_preview,
                    date_str,
                    key=str(post["id"]),
                )
            else:
                table.add_row(
                    str(post["id"]),
                    post["title"],
                    date_str,
                    key=str(post["id"]),
                )

        # Update preview to show the first post
        self.update_preview()

    def load_tags_sidebar(self):
        """Load tags into the sidebar."""
        try:
            self.tags = self.db.get_all_tags()
            list_view = self.query_one("#tags-sidebar-list", ListView)
            list_view.clear()

            for tag in self.tags:
                post_count = self.db.get_tag_post_count(tag["id"])
                label = Label(f"{tag['name']} ({post_count})", id=f"tag-{tag['id']}")
                list_view.append(ListItem(label))
        except Exception as e:
            self.notify(f"Error loading tags: {e}", severity="error")

    def update_preview(self):
        """Update the preview panel with the currently selected post."""
        table = self.query_one("#posts-table", DataTable)
        preview = self.query_one("#preview-content", MarkdownViewer)

        if (
            self.posts
            and table.cursor_row is not None
            and table.cursor_row < len(self.posts)
        ):
            post = self.posts[table.cursor_row]
            self.current_post = post
            full_post_load = self.db.get_post(self.current_post["id"])

            # Show title and content
            if full_post_load.get("content", None):
                content_preview = full_post_load["content"]
            else:
                content_preview = "No content available"
            preview.document.update(f"# {post['title']}\n\n{content_preview}")
        else:
            preview.document.update("Select a post to preview")

    @property
    def cursor_row(self):
        """Get current cursor row."""
        table = self.query_one("#posts-table", DataTable)
        return table.cursor_row

    def on_data_table_row_highlighted(self, event):
        """Update preview when row is highlighted."""
        self.update_preview()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle tag selection in the sidebar."""
        if event.control.id == "tags-sidebar-list":
            # Get the selected index
            selected_index = event.control.index
            if selected_index is not None and selected_index < len(self.tags):
                self.selected_tag_id = self.tags[selected_index]["id"]
                # Filter posts by selected tag
                self.load_posts_for_tag(self.selected_tag_id)

    def load_posts_for_tag(self, tag_id: int):
        """Load posts filtered by tag."""
        try:
            posts = self.db.get_posts_by_tag(tag_id)
            self.posts = posts
            self.populate_table()
        except Exception as e:
            self.notify(f"Error loading posts for tag: {e}", severity="error")

    def action_reset(self):
        """Reset the view to default state: show all posts, clear tag filter, go to top."""
        # Clear the tag filter
        self.selected_tag_id = None

        # Deselect any selected tag in the sidebar
        list_view = self.query_one("#tags-sidebar-list", ListView)
        list_view.index = None

        # Load all posts (no search, no tag filter)
        self.load_posts(search=None)

        # Move cursor to the top of the table
        table = self.query_one("#posts-table", DataTable)
        table.focus()

        # Move cursor to the first row (row 0, column 0)
        if table.row_count > 0:
            table.move_cursor(row=0)

        # Notify user
        self.notify("View reset to default", severity="information")

    def action_edit_post(self):
        """Edit the currently selected post."""
        if self.current_post is None:
            self.notify("No post selected", severity="warning")
            return

        from .ui import EditPostScreen

        def on_updated():
            self.load_posts()
            self.notify("Post updated successfully", severity="information")

        self.push_screen(EditPostScreen(self.db, self.current_post["id"], on_updated))

    def action_new_post(self):
        """Create a new blog post."""
        from .ui import CreatePostScreen

        def on_created(post_id):
            self.load_posts()
            self.notify("Post created successfully", severity="information")

        self.push_screen(CreatePostScreen(self.db, on_created))

    def action_delete_post(self):
        """Delete the currently selected post."""
        if self.current_post is None:
            self.notify("No post selected", severity="warning")
            return

        from .ui import ConfirmDeleteScreen

        def confirm_delete():
            try:
                self.db.delete_post(self.current_post["id"])
                self.notify("Post deleted successfully", severity="information")
                self.load_posts()
            except Exception as e:
                self.notify(f"Error deleting post: {e}", severity="error")

        self.push_screen(
            ConfirmDeleteScreen(self.current_post["title"], confirm_delete)
        )

    def action_search(self):
        """Open search modal."""
        from .ui import SearchModal

        def on_search(search_term):
            self.load_posts(search=search_term)
            if search_term:
                self.notify(f"Searching for: {search_term}", severity="information")
            else:
                self.notify("Search cleared", severity="information")

        self.push_screen(SearchModal(on_search))

    def action_change_collection(self):
        """Open collection selector modal."""
        from .ui import CollectionSelectScreen

        def on_collection_selected(collection: str):
            """Handle collection selection."""
            if collection != self.current_collection:
                self.current_collection = collection
                self.db.set_collection(collection)
                self._update_subtitle()
                self.selected_tag_id = None  # Reset tag filter
                self.load_posts()
                self.load_tags_sidebar()
                self.notify(
                    f"Switched to {self.db.AVAILABLE_COLLECTIONS[collection]}",
                    severity="information"
                )

        self.push_screen(CollectionSelectScreen(on_collection_selected))


def run():
    """Run the content editor TUI."""
    app = ContentEditorApp()
    app.run()


def main():
    """Entry point."""
    run()


if __name__ == "__main__":
    main()
