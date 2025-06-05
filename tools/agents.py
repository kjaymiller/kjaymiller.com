# Because Agents feel like a bunch of AI powered scripts

import json
import os
import pathlib
import subprocess

import psycopg
import frontmatter
import llm
import typer

from rich import print, print_json

db_connection = psycopg.connect(
    os.getenv("POSTGRES_SERVICE_URI"),
)

app = typer.Typer()
model = llm.get_model("claude-4-sonnet")
model.key = os.getenv("CLAUDE_API_KEY")


@app.command(name="describe")
def describe(filepath: pathlib.Path, write: bool = False, confirm: bool = True):
    """Read the contents of a filepath and return the description"""
    post = frontmatter.loads(filepath.read_text())
    response = model.prompt(
        f"create a descriptions for the content -- {post}",
        system="keep your responses in first-person and no longer than a tweet. Make your statements vague enough that potential readers will want to click but don't cross into clickbait territory.",
    )

    text = response.text()

    if write:
        if confirm:
            print(text)
            typer.confirm("Do you want to apply this description?", abort=True)
        post.metadata["description"] = text
        filepath.write_text(frontmatter.dumps(post))
        print("Success! - %s " % filepath.name)

    else:
        print(text)


@app.command(name="linkedin")
def linkedin(filepath: pathlib.Path):
    """Create a linkedin post from the content"""
    post = frontmatter.loads(filepath.read_text())
    response = model.prompt(
        f"create a linkedin post for the content -- {post}",
        system="You are a mid-level engineer that has some PostgreSQL knowledge. Your audience will be postgreSQL users and those considering moving their data to postgreSQL. Don't be over the top but speak with some authority",
    )

    print(response.text())


@app.command(name="tag")
def tag(
    filepath: pathlib.Path,
    detailed: bool = False,
    write: bool = False,
    confirm: bool = True,
):
    """Analyze existing tags and select/create tags for the content"""
    post = frontmatter.loads(filepath.read_text())
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

    response = model.prompt(
        "analyze the list of tags and the content and select/create tags for the post.",
        schema=llm.schema_dsl("tag, justification", multi=True),
        fragments=[
            "\n".join(str(x) for x in records),
            str(post),
        ],
        system_fragments=[
            "You should always prefer using existing tags over creating new ones",
            "explain why you chose the tags you did. Include if the tag already existed",
        ],
    )

    results = response.text()
    tags: list[str] = [tag["tag"] for tag in json.loads(results)["items"]]

    if write:
        if confirm:
            print_json(results)
            typer.confirm("Do you want to apply these tags?", abort=True)
        post.metadata["tags"] = tags
        filepath.write_text(frontmatter.dumps(post))
        print("Success! - %s " % filepath.name)

        if typer.confirm("Would you like to edit the file"):
            editor = os.getenv("EDITOR", "vi")
            subprocess.run([editor, filepath])

    elif detailed:
        print_json(results)

    else:
        print("\n".join(tags))


if __name__ == "__main__":
    app()
