import pathlib
import datetime
from typing import NamedTuple
import typer
import logging
import frontmatter
from pathlib import Path

app = typer.Typer()


class CorrectedTag(NamedTuple):
    tag_name: str
    tag_value: str


def process_tags_as_list(post: frontmatter.Post) -> CorrectedTag | None:
    """Convert Tags from str to List"""

    if isinstance(post.metadata.get("tags", None), str):
        return CorrectedTag(
            "tags", [tag.strip() for tag in post.metadata["tags"].split(",")]
        )


def make_tz_naive(post: frontmatter.Post) -> CorrectedTag | None:
    """Converts a tz aware to a tz naive datetime"""
    if (
        isinstance(post.metadata.get("date", None), datetime.datetime)
        and post.metadata["date"].tzinfo
    ):
        return CorrectedTag("date", post.metadata["date"].replace(tzinfo=None))


def process_frontmatter(filepath: pathlib.Path):
    """
    Process frontmatter in a file:
    Read the file and extract frontmatter
    Convert tags to list if they exist
    Overwrite the file with the updated frontmatter
    """

    post = frontmatter.load(filepath)

    MANIFEST = (process_tags_as_list, make_tz_naive)

    # Execute Function
    for transformation in MANIFEST:
        correction = transformation(post)
        if correction:
            post.metadata[correction.tag_name] = correction.tag_value

    # Write the file back with updated frontmatter
    with open(filepath, "w") as f:
        f.write(frontmatter.dumps(post))

    return post.metadata


@app.command(name="update")
def process_directory(directory: pathlib.Path):
    """Process all files with frontmatter in a directory"""

    for file_path in Path(directory).glob("*.md"):
        logging.info("processing %s" % file_path)
        metadata = process_frontmatter(file_path)
        logging.info(f"Processed {file_path.name}: {metadata}")


def prep_content(filepath: pathlib.Path):
    post = frontmatter.load(filepath)
    tags = [x for x in post.metadata.keys()]
    for tag in tags:
        post.metadata[tag.lower()] = post.metadata.pop(tag)

        with open(filepath, "w") as f:
            f.write(frontmatter.dumps(post))


@app.command(name="prep")
def prep_directory(directory: pathlib.Path):
    for filepath in Path(directory).glob("*.md"):
        logging.info("prepping %s" % filepath.name)
        prep_content(filepath)
        logging.info("Prepped %s" % filepath.name)


if __name__ == "__main__":
    app()
