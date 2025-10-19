import asyncio
import sys
import os

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from common.browser_manager import BrowserManager
from websites.herokuapp.home_page import HomePage

class HerokuAddRemove:
    async def run(self):
        browser = BrowserManager(headless=False)

        async with browser as page:

            home_page = HomePage(browser, page)
            await home_page.open_heroku()
            add_remove_page = await home_page.open_add_remove_page()
            await add_remove_page.click_add_button()
            await add_remove_page.click_delete_button()

if __name__ == "__main__":
    asyncio.run(HerokuAddRemove().run())