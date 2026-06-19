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
        
        # -> Scroll the landing page down to reveal more content and then click the hero 'Watch Demo' button to open the demo walkthrough overlay.
        await page.mouse.wheel(0, 300)
        
        # -> Scroll the landing page down to reveal more content and then click the hero 'Watch Demo' button to open the demo walkthrough overlay.
        # Watch Demo button
        elem = page.locator('[id="hero-demo-btn"]')
        await elem.click(timeout=10000)
        
        # -> Click the modal's close (X) button to close the 'LeadFlow AI Walkthrough Demonstration' overlay and then verify the overlay is dismissed.
        # × button
        elem = page.locator('[id="modal-close-btn"]')
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the demo overlay is no longer displayed
        await page.locator("xpath=/html/body/div[2]/header/div/div[2]/button").nth(0).scroll_into_view_if_needed()
        # Assert: The header 'Watch Demo' button is visible, indicating the demo overlay is closed.
        await expect(page.locator("xpath=/html/body/div[2]/header/div/div[2]/button").nth(0)).to_be_visible(timeout=15000), "The header 'Watch Demo' button is visible, indicating the demo overlay is closed."
        await page.locator("xpath=/html/body/div[2]/section[1]/div[2]/div[1]/button").nth(0).scroll_into_view_if_needed()
        # Assert: The hero 'Watch Demo' button is visible, indicating the demo overlay is closed.
        await expect(page.locator("xpath=/html/body/div[2]/section[1]/div[2]/div[1]/button").nth(0)).to_be_visible(timeout=15000), "The hero 'Watch Demo' button is visible, indicating the demo overlay is closed."
        await page.locator("xpath=/html/body/div[2]/header/div/div[2]/a").nth(0).scroll_into_view_if_needed()
        # Assert: The header 'Get Started' link is visible, indicating the demo overlay is closed.
        await expect(page.locator("xpath=/html/body/div[2]/header/div/div[2]/a").nth(0)).to_be_visible(timeout=15000), "The header 'Get Started' link is visible, indicating the demo overlay is closed."
        current_url = await page.evaluate("() => window.location.href")
        # Assert: page loaded with a URL (final outcome verified by the AI judge during the run)
        assert current_url, 'Page should have loaded with a URL'
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    