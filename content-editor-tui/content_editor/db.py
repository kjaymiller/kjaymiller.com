"""Database connection and operations."""

import os
from datetime import datetime
from typing import Optional, List, Dict, Any

import psycopg
from psycopg import sql


class DatabaseManager:
    """Manages PostgreSQL connections and operations."""

    # Collection metadata (from tui-collection.md implementation guide)
    AVAILABLE_COLLECTIONS = {
        "blog": "Blog Posts",
        "notes": "Notes",
        "microblog": "Microblog Posts",
    }

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

    def __init__(self, connection_string: Optional[str] = None, collection: str = "blog"):
        """Initialize database manager.

        Args:
            connection_string: PostgreSQL connection string (defaults to CONNECTION_STRING env var)
            collection: Collection to manage ("blog", "notes", or "microblog")
        """
        conn_str = connection_string or os.environ.get("CONNECTION_STRING")
        if not conn_str:
            raise ValueError("CONNECTION_STRING environment variable not set")

        if collection not in self.AVAILABLE_COLLECTIONS:
            raise ValueError(f"Invalid collection '{collection}'. Available: {list(self.AVAILABLE_COLLECTIONS.keys())}")

        self.connection_string = conn_str
        self.current_collection = collection
        self.conn = None
        self.connect()

    def set_collection(self, collection: str) -> None:
        """Switch to a different collection at runtime.

        Args:
            collection: Collection name ("blog", "notes", or "microblog")

        Raises:
            ValueError: If collection name is invalid
        """
        if collection not in self.AVAILABLE_COLLECTIONS:
            raise ValueError(f"Invalid collection '{collection}'. Available: {list(self.AVAILABLE_COLLECTIONS.keys())}")
        self.current_collection = collection

    def connect(self):
        """Establish database connection."""
        try:
            self.conn = psycopg.connect(self.connection_string)
        except Exception as e:
            raise RuntimeError(f"Failed to connect to database: {e}")

    def disconnect(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def get_posts(self, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all posts from current collection, optionally filtered by search term.

        For microblog, returns empty title/description since those fields don't exist.
        """
        cursor = self.conn.cursor()
        try:
            table = self.current_collection

            # Microblog doesn't have title/description fields
            if self.current_collection == "microblog":
                if search:
                    query = f"""
                        SELECT id, slug, content, date
                        FROM {table}
                        WHERE slug ILIKE %s OR content ILIKE %s
                        ORDER BY date DESC
                    """
                    search_term = f"%{search}%"
                    cursor.execute(query, (search_term, search_term))
                else:
                    query = f"""
                        SELECT id, slug, content, date
                        FROM {table}
                        ORDER BY date DESC
                    """
                    cursor.execute(query)

                posts = []
                for row in cursor.fetchall():
                    posts.append({
                        "id": row[0],
                        "slug": row[1],
                        "title": "",  # Microblog has no title
                        "description": row[2][:100],  # Use content preview as description
                        "date": row[3],
                    })
                return posts
            else:
                # Blog and Notes have title/description
                if search:
                    query = f"""
                        SELECT id, slug, title, description, date
                        FROM {table}
                        WHERE title ILIKE %s OR slug ILIKE %s OR content ILIKE %s
                        ORDER BY date DESC
                    """
                    search_term = f"%{search}%"
                    cursor.execute(query, (search_term, search_term, search_term))
                else:
                    query = f"""
                        SELECT id, slug, title, description, date
                        FROM {table}
                        ORDER BY date DESC
                    """
                    cursor.execute(query)

                posts = []
                for row in cursor.fetchall():
                    posts.append({
                        "id": row[0],
                        "slug": row[1],
                        "title": row[2],
                        "description": row[3],
                        "date": row[4],
                    })
                return posts
        finally:
            cursor.close()

    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Get a single post with all details from current collection."""
        cursor = self.conn.cursor()
        try:
            table = sql.Identifier(self.current_collection)
            junction_table = sql.Identifier(self.JUNCTION_TABLES[self.current_collection])
            id_column = sql.Identifier(self.ID_COLUMN_NAMES[self.current_collection])

            # Microblog doesn't have title/description
            if self.current_collection == "microblog":
                query = sql.SQL(
                    "SELECT id, slug, content, external_link, image_url, date FROM {} WHERE id = %s"
                ).format(table)
                cursor.execute(query, (post_id,))
                row = cursor.fetchone()
                if not row:
                    return None

                post = {
                    "id": row[0],
                    "slug": row[1],
                    "title": "",  # Microblog has no title
                    "content": row[2],
                    "description": "",  # Microblog has no description
                    "external_link": row[3],
                    "image_url": row[4],
                    "date": row[5],
                }
            else:
                # Blog and Notes have title/description
                query = sql.SQL(
                    "SELECT id, slug, title, content, description, external_link, image_url, date FROM {} WHERE id = %s"
                ).format(table)
                cursor.execute(query, (post_id,))
                row = cursor.fetchone()
                if not row:
                    return None

                post = {
                    "id": row[0],
                    "slug": row[1],
                    "title": row[2],
                    "content": row[3],
                    "description": row[4],
                    "external_link": row[5],
                    "image_url": row[6],
                    "date": row[7],
                }

            # Get tags using dynamic junction table
            query = sql.SQL(
                """
                SELECT t.id, t.name
                FROM tags t
                JOIN {} jt ON t.id = jt.tag_id
                WHERE jt.{} = %s
                ORDER BY t.name
                """
            ).format(junction_table, id_column)
            cursor.execute(query, (post_id,))
            post["tags"] = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

            return post
        finally:
            cursor.close()

    def create_post(
        self,
        slug: str,
        title: str,
        content: str,
        description: str = "",
        external_link: Optional[str] = None,
        image_url: Optional[str] = None,
        date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> int:
        """Create a new post in current collection.

        Note: For microblog, title and description are ignored (microblog has no such fields).
        """
        cursor = self.conn.cursor()
        try:
            if date is None:
                date = datetime.now()

            table = sql.Identifier(self.current_collection)
            junction_table = sql.Identifier(self.JUNCTION_TABLES[self.current_collection])
            id_column = sql.Identifier(self.ID_COLUMN_NAMES[self.current_collection])

            # Microblog doesn't have title/description
            if self.current_collection == "microblog":
                query = sql.SQL(
                    """
                    INSERT INTO {} (slug, content, external_link, image_url, date)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """
                ).format(table)
                cursor.execute(query, (slug, content, external_link, image_url, date))
            else:
                query = sql.SQL(
                    """
                    INSERT INTO {} (slug, title, content, description, external_link, image_url, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """
                ).format(table)
                cursor.execute(query, (slug, title, content, description, external_link, image_url, date))

            post_id = cursor.fetchone()[0]

            # Add tags
            if tags:
                for tag_name in tags:
                    cursor.execute(
                        "INSERT INTO tags (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id",
                        (tag_name,),
                    )
                    tag_id = cursor.fetchone()[0]
                    query = sql.SQL(
                        "INSERT INTO {} ({}, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                    ).format(junction_table, id_column)
                    cursor.execute(query, (post_id, tag_id))

            self.conn.commit()
            return post_id
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to create post: {e}")
        finally:
            cursor.close()

    def update_post(
        self,
        post_id: int,
        slug: Optional[str] = None,
        title: Optional[str] = None,
        content: Optional[str] = None,
        description: Optional[str] = None,
        external_link: Optional[str] = None,
        image_url: Optional[str] = None,
        date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """Update an existing post in current collection.

        Note: For microblog, title and description fields are ignored.
        """
        cursor = self.conn.cursor()
        try:
            table = sql.Identifier(self.current_collection)
            junction_table = sql.Identifier(self.JUNCTION_TABLES[self.current_collection])
            id_column = sql.Identifier(self.ID_COLUMN_NAMES[self.current_collection])

            updates = {}
            if slug is not None:
                updates["slug"] = slug
            if content is not None:
                updates["content"] = content
            if external_link is not None:
                updates["external_link"] = external_link
            if image_url is not None:
                updates["image_url"] = image_url
            if date is not None:
                updates["date"] = date

            # For blog/notes, also allow title/description updates
            if self.current_collection != "microblog":
                if title is not None:
                    updates["title"] = title
                if description is not None:
                    updates["description"] = description

            if updates:
                set_parts = [
                    sql.SQL("{} = %s").format(sql.Identifier(k))
                    for k in updates.keys()
                ]
                set_clause = sql.SQL(", ").join(set_parts)
                values = list(updates.values()) + [post_id]

                query = sql.SQL("UPDATE {} SET {} WHERE id = %s").format(
                    table,
                    set_clause
                )
                cursor.execute(query, values)

            # Update tags if provided
            if tags is not None:
                # Remove old tags
                query = sql.SQL("DELETE FROM {} WHERE {} = %s").format(
                    junction_table, id_column
                )
                cursor.execute(query, (post_id,))

                # Add new tags
                for tag_name in tags:
                    cursor.execute(
                        "INSERT INTO tags (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id",
                        (tag_name,),
                    )
                    tag_id = cursor.fetchone()[0]
                    query = sql.SQL(
                        "INSERT INTO {} ({}, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                    ).format(junction_table, id_column)
                    cursor.execute(query, (post_id, tag_id))

            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to update post: {e}")
        finally:
            cursor.close()

    def delete_post(self, post_id: int) -> bool:
        """Delete a post from current collection.

        Note: Cascade delete handles removing tags automatically.
        """
        cursor = self.conn.cursor()
        try:
            table = sql.Identifier(self.current_collection)
            query = sql.SQL("DELETE FROM {} WHERE id = %s").format(table)
            cursor.execute(query, (post_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to delete post: {e}")
        finally:
            cursor.close()

    def get_all_tags(self) -> List[Dict[str, Any]]:
        """Get all tags."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, name FROM tags ORDER BY name")
            return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        finally:
            cursor.close()

    def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a slug already exists."""
        cursor = self.conn.cursor()
        try:
            if exclude_id:
                cursor.execute("SELECT 1 FROM blog WHERE slug = %s AND id != %s", (slug, exclude_id))
            else:
                cursor.execute("SELECT 1 FROM blog WHERE slug = %s", (slug,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def get_posts_by_tag(self, tag_id: int) -> List[Dict[str, Any]]:
        """Get all posts associated with a tag in current collection."""
        cursor = self.conn.cursor()
        try:
            table = sql.Identifier(self.current_collection)
            junction_table = sql.Identifier(self.JUNCTION_TABLES[self.current_collection])
            id_column = sql.Identifier(self.ID_COLUMN_NAMES[self.current_collection])

            if self.current_collection == "microblog":
                query = sql.SQL(
                    """
                    SELECT t.id, t.slug, t.content, t.date
                    FROM {} t
                    JOIN {} jt ON t.id = jt.{}
                    WHERE jt.tag_id = %s
                    ORDER BY t.date DESC
                    """
                ).format(table, junction_table, id_column)
                cursor.execute(query, (tag_id,))

                posts = []
                for row in cursor.fetchall():
                    posts.append({
                        "id": row[0],
                        "slug": row[1],
                        "title": "",  # Microblog has no title
                        "description": row[2][:100],  # Use content preview
                        "date": row[3],
                    })
                return posts
            else:
                query = sql.SQL(
                    """
                    SELECT t.id, t.slug, t.title, t.description, t.date
                    FROM {} t
                    JOIN {} jt ON t.id = jt.{}
                    WHERE jt.tag_id = %s
                    ORDER BY t.date DESC
                    """
                ).format(table, junction_table, id_column)
                cursor.execute(query, (tag_id,))

                posts = []
                for row in cursor.fetchall():
                    posts.append({
                        "id": row[0],
                        "slug": row[1],
                        "title": row[2],
                        "description": row[3],
                        "date": row[4],
                    })
                return posts
        finally:
            cursor.close()

    def get_tag_post_count(self, tag_id: int) -> int:
        """Get the number of posts associated with a tag in current collection."""
        cursor = self.conn.cursor()
        try:
            junction_table = sql.Identifier(self.JUNCTION_TABLES[self.current_collection])
            query = sql.SQL("SELECT COUNT(*) FROM {} WHERE tag_id = %s").format(
                junction_table
            )
            cursor.execute(query, (tag_id,))
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def rename_tag(self, tag_id: int, new_name: str) -> bool:
        """Rename a tag."""
        cursor = self.conn.cursor()
        try:
            # Check if new name already exists
            cursor.execute("SELECT 1 FROM tags WHERE name = %s AND id != %s", (new_name, tag_id))
            if cursor.fetchone() is not None:
                raise ValueError(f"Tag '{new_name}' already exists")

            cursor.execute("UPDATE tags SET name = %s WHERE id = %s", (new_name, tag_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to rename tag: {e}")
        finally:
            cursor.close()

    def delete_tag(self, tag_id: int) -> bool:
        """Delete a tag and its associations."""
        cursor = self.conn.cursor()
        try:
            # Delete from blog_tags first (foreign key constraint)
            cursor.execute("DELETE FROM blog_tags WHERE tag_id = %s", (tag_id,))
            # Then delete the tag
            cursor.execute("DELETE FROM tags WHERE id = %s", (tag_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            raise RuntimeError(f"Failed to delete tag: {e}")
        finally:
            cursor.close()
