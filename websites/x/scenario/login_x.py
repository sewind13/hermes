import asyncio
import sys
import os

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_parent_dir)

from common.browser_manager import BrowserManager
from websites.x.pages.home_page import HomePage

username = "username"
password = "Test@1234"

class LoginX:
    async def run(self):
        browser = BrowserManager(headless=False)

        async with browser as page:

            home_page = HomePage(browser, page)
            await home_page.open_x_home_page()
            await home_page.click_sign_in()
            await home_page.enter_username(username)
            await home_page.click_next()
            await home_page.enter_password(password)
            await home_page.click_login()
            print("Login to X completed successfully.")

if __name__ == "__main__":
    asyncio.run(LoginX().run())