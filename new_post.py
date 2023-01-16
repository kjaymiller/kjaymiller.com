import typer
from pathlib import Path
from datetime import datetime



app = typer.Typer()

@app.command()
def new_post(content: str=typer.Option(..., prompt=True)):
    date = datetime.now()
    post_date = date.strftime("%Y-%m-%d %H:%M")
    title = date.strftime("%Y%m%d%H%M%S")
    path = Path(f"content/microblog/{title}.md")

    template = f"""---
date: {post_date}
---

{content}
"""

    return path.write_text(template)

if __name__ == "__main__":
    app()
