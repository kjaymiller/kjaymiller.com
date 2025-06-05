"""
Script that should really only be needed once so this will likely be moved to a gist

The script grabs tags from the metadata in postgres and uses llm and claude-4-sonnet
to select tags.

These selected tags are added to the files.
"""

import logging
import json
import os
import pathlib
import typing

import frontmatter
import llm
import psycopg
import typer


app = typer.Typer()

db_connection = psycopg.connect(
    os.getenv("POSTGRES_SERVICE_URI"),
)

model = llm.get_model("claude-4-sonnet")
model.key = os.getenv("CLAUDE_API_KEY")

with db_connection.cursor() as cursor:
    cursor.execute(
        """
        SELECT DISTINCT
        jsonb_array_elements_text(meta->'tags') AS individual_tag
        FROM contentitem
        WHERE meta->'tags' IS NOT NULL;
        """
    )
    records = cursor.fetchall()


def get_tags(post_content: str) -> list[str]:
    response = model.prompt(
        "analyze the list of tags and the content and select/create tags for the post.",
        schema=llm.schema_dsl("tag", multi=True),
        fragments=[post_content],
        system_fragments=[
            "The list of tags",
            "\n".join(str(x) for x in records),
            "prefer selecting existing tags vs creating new ones.",
            "most content will have between 1-3 tags",
        ],
    )
    results = response.text()
    tags: list[str] = [tag["tag"] for tag in json.loads(results)["items"]]
    return tags


def check_for_tags(filepath: pathlib.Path) -> bool:
    post = frontmatter.loads(filepath.read_text())

    typer.echo(post.metadata)

    if "tags" in post.metadata:
        typer.echo("tags exists for %s" % str(filepath))
        return True

    typer.echo(f"Creating Tags for - {filepath}")
    tags = get_tags(post.content)
    typer.echo(", ".join(tags))
    post.metadata["tags"] = tags
    filepath.write_text(frontmatter.dumps(post))
    return False


@app.command()
def cli(target_files: typing.List[pathlib.Path]):
    return_code = 0

    for filepath in target_files:
        typer.echo("Processing %s" % filepath)
        if not check_for_tags(filepath):
            return_code = 1

    typer.echo(f"{return_code=}")
    typer.Exit(code=return_code)


def main():
    app()


if __name__ == "__main__":
    app()
