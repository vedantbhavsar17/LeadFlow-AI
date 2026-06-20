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
        
        # -> Click the 'Watch Demo' button in the hero section to open the demo modal.
        # Watch Demo button
        elem = page.locator('[id="hero-demo-btn"]')
        await elem.click(timeout=10000)
        
        # -> Click the modal's close button (the 'X' at the top-right of the 'LeadFlow AI Walkthrough Demonstration' modal) to dismiss the demo and return to the landing page.
        # × button
        elem = page.locator('[id="modal-close-btn"]')
        await elem.click(timeout=10000)
        
        # -> Click the hero 'Get Started' button to enter the dashboard (the large primary 'Get Started' CTA in the hero section).
        # Get Started link
        elem = page.get_by_text('Qualified Sales Conversations', exact=True).locator("xpath=ancestor-or-self::*[.//a][1]").get_by_role('link', name='Get Started', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the dashboard is displayed
        # Assert: The URL contains '/dashboard', confirming the dashboard route is loaded.
        await expect(page).to_have_url(re.compile("/dashboard"), timeout=15000), "The URL contains '/dashboard', confirming the dashboard route is loaded."
        await page.locator("xpath=/html/body/div[3]/aside/div[1]/nav/a[1]").nth(0).scroll_into_view_if_needed()
        # Assert: The 'Dashboard' navigation link is visible in the sidebar, indicating the dashboard is displayed.
        await expect(page.locator("xpath=/html/body/div[3]/aside/div[1]/nav/a[1]").nth(0)).to_be_visible(timeout=15000), "The 'Dashboard' navigation link is visible in the sidebar, indicating the dashboard is displayed."
        await page.locator("xpath=/html/body/div[3]/div[2]/div[1]").nth(0).scroll_into_view_if_needed()
        # Assert: The 'Demo Control Hub' panel is visible on the page, confirming dashboard content is shown.
        await expect(page.locator("xpath=/html/body/div[3]/div[2]/div[1]").nth(0)).to_be_visible(timeout=15000), "The 'Demo Control Hub' panel is visible on the page, confirming dashboard content is shown."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    