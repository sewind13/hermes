import asyncio
import sys
import os

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_parent_dir)

from common.browser_manager import BrowserManager
from websites.google_map.pages.home_page import HomePage

class LoginX:
    async def run(self):
        browser = BrowserManager(headless=False, persistent=True)

        async with browser as page:

            home_page = HomePage(browser, page)
            await home_page.open_bps_location_page()
            await home_page.click_consent_button()
            await home_page.click_review_button()
            await home_page.wait(2)
            await home_page.scroll_on_reviews_section()
            await home_page.get_reviews()
            print("Opened BPS location page on Google Maps successfully.")

if __name__ == "__main__":
    asyncio.run(LoginX().run())

