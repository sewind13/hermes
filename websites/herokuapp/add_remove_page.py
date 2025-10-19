import sys
import os

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from common.base_page import BasePage
from common.base_action import BaseAction
from common.base_locator import BaseLocator

class AddRemoveElement:
    title = "//h3[contains(text(), 'Add/Remove Elements')]"
    button_add = "//button[contains(text(),'Add Element')]"
    button_delete = "//button[contains(text(), 'Delete')]"

class AddRemovePage(BasePage, BaseAction, BaseLocator):
    async def click_add_button(self):
        button_add = self.get_locator_by_xpath(AddRemoveElement.button_add)
        await button_add.click()

    async def click_delete_button(self):
        button_delete = self.get_locator_by_xpath(AddRemoveElement.button_delete)
        await button_delete.click()