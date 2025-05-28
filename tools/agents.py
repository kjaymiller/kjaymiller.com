# Because Agents feel like a bunch of AI powered scripts

import os
import pathlib

import frontmatter
import llm
import typer


app = typer.Typer()
model = llm.get_model("claude-4-sonnet")
model.key = os.getenv("CLAUDE_API_KEY")


@app.command(name="describe")
def describe(filepath: pathlib.Path, write: bool = False):
    """Read the contents of a filepath and return the description"""
    post = frontmatter.loads(filepath.read_text())
    response = model.prompt(
        f"create a descriptions for the content -- {post}",
        system="keep your responses in first-person and no longer than a tweet. Make your statements vague enough that potential readers will want to click but don't cross into clickbait territory.",
    )

    text = response.text()

    if write:
        post.metadata["description"] = text
        filepath.write_text(frontmatter.dumps(post))


if __name__ == "__main__":
    app()
