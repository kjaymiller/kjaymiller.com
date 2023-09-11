from playwright.sync_api import sync_playwright
from axe_playwright_python.sync_playwright import Axe

axe = Axe()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://kjaymiller.com")
    results = axe.run(page)
    browser.close()

print(results.save_to_file(file_path="test-results.json"))
print(results.generate_report())
