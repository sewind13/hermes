import sys
import os

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_parent_dir)

from common.base_page import BasePage
from common.base_action import BaseAction
from common.base_locator import BaseLocator

class HomeElements:
    url = "https://x.com/"
    sign_in_button = "//span[contains(text(), 'Sign in')]"
    username_input = "//input[contains(@autocomplete,'username')]"
    next_button = "//span[contains(text(), 'Next')]"
    password_input = "//input[contains(@name,'password')]"
    login_button = "//span[contains(text(), 'Log in')]"

class HomePage(BasePage, BaseAction, BaseLocator):

    async def open_x_home_page(self):
        await self.open(HomeElements.url)

    async def click_sign_in(self):
        sign_in_button = self.get_locator_by_xpath(HomeElements.sign_in_button)
        await sign_in_button.click()

    async def enter_username(self, username):
        username_input = self.get_locator_by_xpath(HomeElements.username_input)
        await self.human_type(username_input, username)

    async def click_next(self):
        next_button = self.get_locator_by_xpath(HomeElements.next_button)
        await next_button.click()

    async def enter_password(self, password):
        password_input = self.get_locator_by_xpath(HomeElements.password_input)
        await self.human_type(password_input, password)

    async def click_login(self):
        login_button = self.get_locator_by_xpath(HomeElements.login_button)
        await login_button.click()

    