# Create a script that iterates through the content folder and looks
# install dateutil, frontmatter
# `pip install python-dateutil frontmatter`
# Run with `python convert_dates.py <CONTENT_DIRECTORY>`

from sys import argv
from dateutil.parser import parse
import frontmatter
import pathlib


date_values = [
    "date",
    "Date",
    "date_published",
    "date_modified",
    "published_date",
    "modified_date",
]


def iterate_through_content(path: pathlib.Path):
    for file in path.rglob("**/*.md"):
        post = frontmatter.loads(file.read_text())
        changed = False

        for date_value in date_values:
            if post.get(date_value, None):
                if isinstance(post[date_value], str):
                    post[date_value] = parse(post[date_value]).astimezone()
                    changed = True
                    print(
                        f"Updating {file.name}: {date_value} to {post[date_value]}..."
                    )

        if changed:
            print(f"Updating {file}...")
            new_post = frontmatter.dumps(post)
            file.write_text(new_post)


if __name__ == "__main__":
    path = pathlib.Path(argv[1])
    iterate_through_content(path)
