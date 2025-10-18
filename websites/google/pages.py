import sys
import os
import asyncio

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from common.base_action import BaseAction
from common.base_locator import BaseLocator
from common.browser_manager import BrowserManager


# ---------------------------------------------------------
# Element locators
# ---------------------------------------------------------
class GoogleElement:
    search_box = "//textarea[contains(@class, 'gLFyf')]"
    button_search = "//div[contains(@class, 'FPdoLc lJ9FBc')]/center/input[contains(@class, 'gNO89b')]"
    title = "h1"


# ---------------------------------------------------------
# Page Object
# ---------------------------------------------------------
class Page(BaseAction, BaseLocator):

    def __init__(self, browser_manager: BrowserManager, page):
        super().__init__(page)
        self.page = page
        self.browser_manager = browser_manager  

    async def open(self, url: str):
        """เปิดหน้าเว็บใหม่โดยใช้ BrowserManager"""
        await self.browser_manager.safe_goto(url)

    async def get_title_text(self) -> str:
        """ตัวอย่างการใช้ BaseLocator"""
        locator = self.get_locator_by_xpath(GoogleElement.title)
        return await locator.text_content() or ""
    
    async def search(self, query: str):
        """ตัวอย่าง action"""
        search_box = self.get_locator_by_xpath(GoogleElement.search_box)
        await search_box.fill(query)
        await search_box.press("Enter")
        await self.page.wait_for_timeout(2000)


# ---------------------------------------------------------
# Browser Controller
# ---------------------------------------------------------
class Browser:
    def __init__(self, headless: bool = True):
        self.manager = BrowserManager(headless=headless)
        self.page = None

    async def __aenter__(self):
        self.page = await self.manager.__aenter__()
        return Page(self.manager, self.page)  
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.manager.__aexit__(exc_type, exc_val, exc_tb)