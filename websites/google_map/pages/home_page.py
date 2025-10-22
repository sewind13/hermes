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
    url_bps = "https://www.google.com/maps/place/%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99%E0%B9%80%E0%B8%9E%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B8%AA%E0%B8%B8%E0%B8%82+%E0%B8%AD%E0%B8%B4%E0%B8%A1%E0%B9%81%E0%B8%9E%E0%B9%87%E0%B8%84+%E0%B9%80%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%AD%E0%B8%87/@12.982295,98.7196668,7z/data=!4m13!1m2!2m1!1z4Lia4LmJ4Liy4LiZ4LmA4Lie4Li04LmI4Lih4Liq4Li44LiC!3m9!1s0x30e28478a6d53af3:0x358b951f32c024da!5m2!4m1!1i2!8m2!3d13.9256014!4d100.5295965!15sCiTguJrguYnguLLguJnguYDguJ7guLTguYjguKHguKrguLjguIJaKCIm4Lia4LmJ4Liy4LiZIOC5gOC4nuC4tOC5iOC4oSDguKrguLjguIKSAQVob3RlbJoBRENpOURRVWxSUVVOdlpFTm9kSGxqUmpsdlQydEdhMlJxVm10a1ZrNTRZbXhhVDJWdVdtWk5WVFZIVWtSQ01sSlhZeEFCqgFPEAEyHxABIhtz5lsMBDh6Sj_gjXO22VDkbRUxNqpXUo4N4QsyKhACIibguJrguYnguLLguJkg4LmA4Lie4Li04LmI4LihIOC4quC4uOC4guABAPoBBAgWEDw!16s%2Fg%2F11bxjbq7dp?entry=ttu&g_ep=EgoyMDI1MTAxNC4wIKXMDSoASAFQAw%3D%3D"
    button_about = "//button[contains(@class,'hh2c6 ') and @data-tab-index='2']"
    total_score_panel = "//div[contains(@class,'Bd93Zb')]"
    reviews_section = "(//div[contains(@class, 'm6QErb DxyBCb kA9KIf dS8AEf XiKgde')])[last()]"

class HomePage(BasePage, BaseAction, BaseLocator):

    async def open_bps_location_page(self):
        await self.open(HomeElements.url_bps)

    async def click_about_button(self):
        button = self.get_locator_by_xpath(HomeElements.button_about)
        await button.click()

    async def move_mouse_to_total_score_panel(self):
        reviews_section = self.get_locator_by_xpath(HomeElements.reviews_section)
        await self.human_scroll_to_bottom(reviews_section)