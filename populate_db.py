#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "psycopg[binary]>=3.0.0",
#     "pyyaml>=6.0",
#     "click>=8.0.0",
# ]
# ///

import os
import re
import sys
from pathlib import Path
from datetime import datetime
import psycopg
import yaml
import click

# Database connection
conn_string = os.environ.get('CONNECTION_STRING')
if not conn_string:
    raise ValueError("CONNECTION_STRING environment variable not set")

conn = psycopg.connect(conn_string)
cursor = conn.cursor()

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown file."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None, None

    try:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    except yaml.YAMLError:
        return None, None

def parse_markdown_files(content_dir):
    """Parse all markdown files in content directory."""
    posts = []
    content_path = Path(content_dir)

    for md_file in content_path.glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter, body = parse_frontmatter(content)
            if not frontmatter:
                print(f"Warning: Could not parse frontmatter for {md_file.name}")
                continue

            # Create slug from filename (remove extension)
            slug = md_file.stem

            post = {
                'slug': slug,
                'title': frontmatter.get('title', md_file.stem),
                'content': body or '',
                'description': frontmatter.get('description', ''),
                'external_link': frontmatter.get('external_link', None),
                'image_url': frontmatter.get('image_url', None),
                'date': frontmatter.get('date'),
                'tags': frontmatter.get('tags', [])
            }

            # Convert date string to datetime if needed
            if isinstance(post['date'], str):
                try:
                    post['date'] = datetime.fromisoformat(post['date'])
                except:
                    post['date'] = datetime.now()
            elif post['date'] is None:
                post['date'] = datetime.now()

            posts.append(post)
            print(f"Parsed: {md_file.name}")

        except Exception as e:
            print(f"Error parsing {md_file.name}: {e}")
            continue

    return posts

def get_table_columns(table_name):
    """Get list of columns for a table."""
    cursor.execute(f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position
    """, (table_name,))
    return [row[0] for row in cursor.fetchall()]

def insert_posts(posts, table_name):
    """Insert posts and tags into database based on table schema."""
    junction_table = f"{table_name}_tags"
    id_column = f"{table_name}_id"

    # Get available columns for this table
    available_columns = get_table_columns(table_name)

    # Check if junction table exists for tags
    has_tags = f"{table_name}_tags" in [row[0] for row in cursor.execute(
        "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
    ).fetchall()]

    for post in posts:
        try:
            # Build dynamic insert query based on available columns
            insert_columns = ['slug', 'content', 'date']
            insert_values = [post['slug'], post['content'], post['date']]

            # Add optional columns if they exist in the table
            for col in ['title', 'description', 'external_link', 'image_url']:
                if col in available_columns:
                    insert_columns.append(col)
                    insert_values.append(post.get(col))

            # Build the insert statement
            columns_str = ', '.join(insert_columns)
            placeholders = ', '.join(['%s'] * len(insert_columns))
            update_set = ', '.join([f"{col}=EXCLUDED.{col}" for col in insert_columns if col != 'slug'])

            query = f"""INSERT INTO {table_name} ({columns_str})
                       VALUES ({placeholders})
                       ON CONFLICT (slug) DO UPDATE SET {update_set}
                       RETURNING id"""

            cursor.execute(query, insert_values)
            post_id = cursor.fetchone()[0]

            # Insert tags if junction table exists
            if has_tags:
                for tag_name in post.get('tags', []):
                    cursor.execute(
                        """INSERT INTO tags (name) VALUES (%s)
                           ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name
                           RETURNING id""",
                        (tag_name,)
                    )
                    tag_id = cursor.fetchone()[0]

                    # Link post and tag
                    cursor.execute(
                        f"""INSERT INTO {junction_table} ({id_column}, tag_id)
                           VALUES (%s, %s)
                           ON CONFLICT DO NOTHING""",
                        (post_id, tag_id)
                    )

            print(f"Inserted: {post['slug']}")

        except Exception as e:
            print(f"Error inserting {post['slug']}: {e}")
            continue

    conn.commit()

@click.command()
@click.argument('table_name')
@click.argument('content_path', type=click.Path(exists=True))
def populate(table_name, content_path):
    """
    Populate a database table with markdown content.

    TABLE_NAME: The database table name (e.g., blog, notes, microblog)
    CONTENT_PATH: Path to directory containing markdown files
    """
    click.echo(f"Parsing markdown files from {content_path}...")
    posts = parse_markdown_files(content_path)
    click.echo(f"Found {len(posts)} posts\n")

    if not posts:
        click.echo("No posts found. Exiting.")
        cursor.close()
        conn.close()
        return

    click.echo(f"Inserting into {table_name} table...")
    insert_posts(posts, table_name=table_name)

    cursor.close()
    conn.close()

    click.echo(f"\nDatabase population complete! ({len(posts)} posts inserted)")

if __name__ == '__main__':
    populate()
