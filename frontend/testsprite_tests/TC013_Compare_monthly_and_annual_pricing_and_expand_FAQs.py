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
        
        # -> Click the 'Pricing' link in the top navigation to open the Pricing page so the billing toggle and FAQ sections can be tested.
        # Pricing link
        elem = page.get_by_role('link', name='Pricing', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Annual' billing toggle (the billing switch labeled 'Monthly / Annual Save 20%') to switch pricing cadence to annual, then scroll down to reveal the FAQ section.
        # button
        elem = page.locator('[id="billing-toggle-btn"]')
        await elem.click(timeout=10000)
        
        # -> Click the 'Annual' billing toggle (the billing switch labeled 'Monthly / Annual Save 20%') to switch pricing cadence to annual, then scroll down to reveal the FAQ section.
        await page.mouse.wheel(0, 300)
        
        # -> Expand the FAQ item titled 'How does the AI lead qualification engine score leads?' by clicking its accordion button, then expand the FAQ 'Is there a setup fee or long-term contract?'.
        # How does the AI lead qualification engine score... button
        elem = page.get_by_role('button', name='How does the AI lead qualification engine score leads?', exact=True)
        await elem.click(timeout=10000)
        
        # -> Expand the FAQ item titled 'How does the AI lead qualification engine score leads?' by clicking its accordion button, then expand the FAQ 'Is there a setup fee or long-term contract?'.
        # Is there a setup fee or long-term contract? button
        elem = page.get_by_role('button', name='Is there a setup fee or long-term contract?', exact=True)
        await elem.click(timeout=10000)
        
        # -> Expand the FAQ item titled 'How does the AI lead qualification engine score leads?' by clicking its accordion button, then expand the FAQ 'Is there a setup fee or long-term contract?'.
        await page.mouse.wheel(0, 300)
        
        # -> Click the 'Monthly / Annual Save 20%' billing toggle to switch the pricing view back to Monthly, then verify that the pricing cards update to show monthly billing labels and amounts.
        # button
        elem = page.locator('[id="billing-toggle-btn"]')
        await elem.click(timeout=10000)
        
        # -> Click the 'Annual' option on the billing toggle (the 'Monthly / Annual Save 20%' switch) to switch the pricing view to Annual and verify the pricing cards show 'BILLED ANNUALLY' or annual amounts.
        # button
        elem = page.locator('[id="billing-toggle-btn"]')
        await elem.click(timeout=10000)
        
        # -> Switch the billing toggle to the 'Monthly' view and verify the pricing cards show a monthly billing label (e.g., 'Billed monthly' or '/mo'), then switch back to 'Annual' and verify the cards show the annual billing label 'Billed annually'.
        # button
        elem = page.locator('[id="billing-toggle-btn"]')
        await elem.click(timeout=10000)
        
        # -> Switch the billing toggle to the 'Monthly' view and verify the pricing cards show a monthly billing label (e.g., 'Billed monthly' or '/mo'), then switch back to 'Annual' and verify the cards show the annual billing label 'Billed annually'.
        # button
        elem = page.locator('[id="billing-toggle-btn"]')
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify pricing options for both billing views are displayed
        # Assert: Verify the pricing card shows the monthly billing label '/mo'.
        await expect(page.locator("xpath=/html/body/div[2]/section[2]/div/div/div[1]/div[1]/div[1]/span[3]").nth(0)).to_have_text("/mo", timeout=15000), "Verify the pricing card shows the monthly billing label '/mo'."
        # Assert: Verify the pricing card displays the 'Billed annually' label for annual billing.
        await expect(page.locator("xpath=/html/body/div[2]/section[2]/div/div/div[1]").nth(0)).to_contain_text("Billed annually", timeout=15000), "Verify the pricing card displays the 'Billed annually' label for annual billing."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    