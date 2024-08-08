from playwright.sync_api import sync_playwright, Playwright
from routes import app
from render_engine.cli import event


# Fetch profiles from the playwright list at https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json
PROFILES = [
    "iPhone 14 Pro",
    "iPhone 14 Pro landscape",
    "Desktop Safari",
    "Desktop Chrome",
]


# start the service
#

server = event.RegExHandler(
    server_address=("127.0.0.1", 8000),
    dir_to_serve="output",
    app=app,
    module_site="",
)


with server as _:
    with sync_playwright() as p:
        for PROFILE in PROFILES:
            browser = p.webkit.launch(headless=False)
            device = p.devices[PROFILE]
            context = browser.new_context(**device)
            page = context.new_page()
            page.goto("http://localhost:8000")
            page.wait_for_load_state("networkidle")
            page.screenshot(
                type="png",
                path=f"design/test_{PROFILE}.png",
                full_page=True,
                scale="css",
            )
