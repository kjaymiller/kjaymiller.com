from playwright.sync_api import sync_playwright
from axe_playwright_python.sync_playwright import Axe
import typer 
import pathlib

axe = Axe()


def main(url: str, output: str = "test-results.json") -> None:
    """Run Axe on a URL and save the results to a file."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        results = axe.run(page)
        browser.close()

    pathlib.Path(output).write_text(results.generate_report())

if __name__ == "__main__":
    typer.run(main)