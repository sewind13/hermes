# common/base_page.py
from common.base_action import BaseAction
from common.base_locator import BaseLocator
from common.browser_manager import BrowserManager

class BasePage(BaseAction, BaseLocator):
    """Reusable Base Page class for all web pages."""

    def __init__(self, browser_manager: BrowserManager, page):
        super().__init__(page)
        self.page = page
        self.browser_manager = browser_manager

    async def open(self, url: str):
        """Open new page by using browser manager"""
        await self.browser_manager.safe_goto(url)
