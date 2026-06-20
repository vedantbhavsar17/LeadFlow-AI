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
        
        # -> Navigate to the Pricing page (the site path /pricing) so the billing frequency toggle and plan prices can be tested.
        await page.goto("http://localhost:3000/pricing")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> click
        # button
        elem = page.locator('[id="billing-toggle-btn"]')
        await elem.click(timeout=10000)
        
        # -> Switch the billing frequency back to Monthly by clicking the billing frequency toggle (the control labeled 'Monthly / Annual') so the plan cards update to show monthly prices.
        # button
        elem = page.locator('[id="billing-toggle-btn"]')
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the pricing values update for monthly billing
        # Assert: Starter plan card displays the monthly price '$49 /mo'.
        await expect(page.locator("xpath=/html/body/div[2]/div/section[2]/div/div/div[1]").nth(0)).to_contain_text("$ 49 /mo", timeout=15000), "Starter plan card displays the monthly price '$49 /mo'."
        # Assert: Growth plan card displays the monthly price '$129 /mo'.
        await expect(page.locator("xpath=/html/body/div[2]/div/section[2]/div/div/div[2]").nth(0)).to_contain_text("$ 129 /mo", timeout=15000), "Growth plan card displays the monthly price '$129 /mo'."
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
    