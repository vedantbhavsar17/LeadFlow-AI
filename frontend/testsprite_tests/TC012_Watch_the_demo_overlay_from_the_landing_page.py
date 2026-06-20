import asyncio
import re
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None

    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()

        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",
                "--disable-dev-shm-usage",
                "--ipc=host",
                "--single-process"
            ],
        )

        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        # Wider default timeout to match the agent's DOM-stability budget;
        # auto-waiting Playwright APIs (expect, locator.wait_for) inherit this.
        context.set_default_timeout(15000)

        # Open a new page in the browser context
        page = await context.new_page()

        # Interact with the page elements to simulate user flow
        # -> navigate
        await page.goto("http://localhost:3000")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Click the 'Watch Demo' button in the hero section to open the demo walkthrough overlay, then verify the overlay is displayed.
        # Watch Demo button
        elem = page.locator('[id="hero-demo-btn"]')
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the demo overlay is displayed
        await page.locator("xpath=/html/body/div[2]/div/div[2]").nth(0).scroll_into_view_if_needed()
        # Assert: The demo walkthrough modal is visible.
        await expect(page.locator("xpath=/html/body/div[2]/div/div[2]").nth(0)).to_be_visible(timeout=15000), "The demo walkthrough modal is visible."
        # Assert: The modal shows the play CTA text 'Click to play interactive sales workflow demo'.
        await expect(page.locator("xpath=/html/body/div[2]/div/div[2]/div/div[2]/div/div[1]").nth(0)).to_have_text("Click to play interactive sales workflow demo", timeout=15000), "The modal shows the play CTA text 'Click to play interactive sales workflow demo'."
        await page.locator("xpath=/html/body/div[2]/div/div[2]/div/div[1]/button").nth(0).scroll_into_view_if_needed()
        # Assert: The modal's close (×) button is visible.
        await expect(page.locator("xpath=/html/body/div[2]/div/div[2]/div/div[1]/button").nth(0)).to_be_visible(timeout=15000), "The modal's close (\u00d7) button is visible."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    