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
        
        # -> Click the 'Dashboard' link in the site header to open the Dashboard page.
        # Dashboard link
        elem = page.get_by_text('Roadmap', exact=True).locator("xpath=ancestor-or-self::*[.//a][1]").get_by_role('link', name='Dashboard', exact=True)
        await elem.click(timeout=10000)
        
        # -> Scroll the dashboard slightly to center the chart and then click the 'Conversion Performance Trajectory' chart to attempt to reveal a detailed-values tooltip.
        await page.mouse.wheel(0, 300)
        
        # -> Click the visible '20.1%' chart detail text on the dashboard (the label showing Conv. Rate: 20.1%) to try to reveal a detailed-values tooltip or focused state.
        # 20.1%
        elem = page.get_by_text('20.1%', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify detailed chart values are displayed
        # Assert: Detailed chart overlay shows the 'Week 1' label.
        await expect(page.locator("xpath=/html/body/div[2]/div/section[5]/div/div[2]/div[2]/div[3]/div[2]/div[2]").nth(0)).to_contain_text("Week 1", timeout=15000), "Detailed chart overlay shows the 'Week 1' label."
        # Assert: Detailed chart overlay shows the conversion rate '18.2%'.
        await expect(page.locator("xpath=/html/body/div[2]/div/section[5]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[3]/div[2]/span").nth(0)).to_contain_text("18.2%", timeout=15000), "Detailed chart overlay shows the conversion rate '18.2%'."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    