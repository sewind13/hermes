import sys
import os

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from common.base_page import BasePage
from common.base_action import BaseAction
from websites.google.resulte_page import ResultPage



# ---------------------------------------------------------
# Element locators
# ---------------------------------------------------------
class GoogleElement:
    url = "https://www.google.com"
    search_box = "//textarea[contains(@class, 'gLFyf')]"
    button_search = "//div[contains(@class, 'FPdoLc lJ9FBc')]/center/input[contains(@class, 'gNO89b')]"
    button_consent = "//button[contains(@id,'W0wltc')]"
    title = "h1"


# ---------------------------------------------------------
# Page Object
# ---------------------------------------------------------
class HomePage(BasePage):
    SEARCH_BOX = "//textarea[contains(@class, 'gLFyf')]"

    async def open_google(self):
        await self.open(GoogleElement.url)

    async def search(self, query: str) -> ResultPage:
        box = self.get_locator_by_xpath(self.SEARCH_BOX)
        await self.human_type(box, query)
        await box.press("Enter")
        await self.page.wait_for_load_state("networkidle")

        # คืน ResultPage (ใช้ BrowserManager เดิม)
        return ResultPage(self.browser_manager, self.page)
    
    async def accept_consent(self):
        consent_button = self.get_locator_by_xpath(GoogleElement.button_consent)
        if await consent_button.is_visible():
            await consent_button.click()    