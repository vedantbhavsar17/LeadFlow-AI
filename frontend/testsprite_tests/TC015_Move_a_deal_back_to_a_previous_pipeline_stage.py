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
        
        # -> Open the 'Pipeline' page by navigating to /pipeline so the pipeline board with deal cards is visible.
        await page.goto("http://localhost:3000/pipeline")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Click the 'Load 50 Leads' button in the Demo Control Hub to populate the pipeline with more leads so a backward move can be tested.
        # Load 50 Leads button
        elem = page.get_by_role('button', name='Load 50 Leads', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the left 'Move Stage' control for a card in the 'Qualified' column (for example the 'Integra Lab Ltd' card) to move it back into the 'New Leads' column, then verify the card appears in the earlier column.
        # button
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div[2]/div[2]/div[2]/div/div[2]/button')
        await elem.click(timeout=10000)
        
        # -> Click the left 'Move Stage' button on the 'LaunchPad Software Ltd' card in the 'Qualified' column to move it back into the 'New Leads' column.
        # button
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div[2]/div[2]/div[2]/div/div[2]/button')
        await elem.click(timeout=10000)
        
        # -> Click the left 'Move Stage' button on the 'Aero Manufacturing Group' card in the 'Qualified' column to move it back into the 'New Leads' column, then verify the card appears in the earlier stage column.
        # button
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div[2]/div[2]/div[2]/div/div[2]/button')
        await elem.click(timeout=10000)
        
        # -> Click the left 'Move Stage' button on the 'Northstar FinTech Ltd' card in the 'Qualified' column to move it back into the 'New Leads' column, then verify the card appears in the earlier stage column.
        # button
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div[2]/div[2]/div[2]/div/div[2]/button')
        await elem.click(timeout=10000)
        
        # -> click
        # Prism Consulting Ltd
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div[2]/div[2]/div[2]/div/div/h4')
        await elem.click(timeout=10000)
        
        # -> Change the lead's 'Update Stage' from 'Qualified' to 'New Lead' on the Prism Consulting Ltd detail page to move the deal back one stage, then verify it appears in the earlier column on the pipeline board.
        # New Lead Qualified Outreach Sent Customer Replied... dropdown
        elem = page.get_by_text('New Lead Qualified Outreach Sent Customer Replied Followup Scheduled Converted', exact=True)
        await elem.click(timeout=10000)
        
        # -> Change the lead's 'Update Stage' from 'Qualified' to 'New Lead' on the Prism Consulting Ltd detail page to move the deal back one stage, then verify it appears in the earlier column on the pipeline board.
        # New Lead
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div[2]/div/div[2]/div/span')
        await elem.click(timeout=10000)
        
        # -> Click the 'Pipeline' link in the left sidebar to open the pipeline board and verify that the 'Prism Consulting Ltd' card is displayed in the New Leads column.
        # Pipeline link
        elem = page.get_by_role('link', name='Pipeline', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the left 'Move Stage' button on the 'Prism Consulting Ltd' card in the 'Qualified' column, then locate 'Prism Consulting Ltd' on the pipeline board to confirm whether it now appears in the 'New Leads' column.
        # button
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div[2]/div[2]/div[2]/div/div[2]/button')
        await elem.click(timeout=10000)
        
        # -> Open the 'Elevate HR Group' lead detail by clicking its card title to edit the stage from the detail view.
        # Elevate HR Group
        elem = page.get_by_text('Elevate HR Group', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the card is displayed in the earlier stage column
        # Assert: The lead's stage is shown as 'New Lead', confirming it is in the earlier stage column.
        await expect(page.locator("xpath=/html/body/div[2]/div[1]/main/div/div[2]/div/div[2]/div[1]/span").nth(0)).to_have_text("New Lead", timeout=15000), "The lead's stage is shown as 'New Lead', confirming it is in the earlier stage column."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    