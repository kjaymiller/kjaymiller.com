from playwright.sync_api import sync_playwright
from axe_playwright_python.sync_playwright import Axe
from multiprocessing import Process
import http
import typer
import pathlib
import render_engine.cli.cli as render_engine

axe = Axe()


def run_server():
    class server(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory="output", **kwargs)

    httpd = http.server.HTTPServer(("localhost", 8000), server)
    httpd.serve_forever()


def main(url: str = "http://localhost", output: str = "test-results.md") -> None:
    """Run Axe on a URL and save the results to a file."""
    render_engine.build(module_site=("routes","app")
    proc = Process(target=run_server, daemon=True)
    proc.start()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(f"{url}:8000")
        results = axe.run(page)
        browser.close()
    proc.kill()

    pathlib.Path(output).write_text(results.generate_report())


if __name__ == "__main__":
    typer.run(main)
