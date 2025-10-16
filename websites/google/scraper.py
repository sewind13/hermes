from common.browser_manager import BrowserManager
from common.base_action import BaseAction

class ExampleScraper:
    async def run(self):
        browser = BrowserManager(headless=False)

        async with browser as page:
            actions = BaseAction(page)

            success = await browser.safe_goto("https://google.com")
            if not success:
                return

            await actions.wait_for_selector("h1")
            title = await page.text_content("h1")
            print("Title:", title)

            await actions.scroll_to_bottom()
