import sys
import os

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from common.base_page import BasePage
from common.base_action import BaseAction
from common.base_locator import BaseLocator
from websites.herokuapp.add_remove_page import AddRemovePage



class HerokuElement:
    url = "https://the-internet.herokuapp.com/"
    add_remove_button = "//a[text()='Add/Remove Elements']"


class HomePage(BasePage, BaseAction, BaseLocator):
    async def open_heroku(self):
        await self.open(HerokuElement.url)

    async def open_add_remove_page(self):
        add_remove_button = self.get_locator_by_xpath(HerokuElement.add_remove_button)
        await add_remove_button.click()
        await self.page.wait_for_load_state("networkidle")
    
        return AddRemovePage(self.browser_manager, self.page)