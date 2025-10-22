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

username = "bluedottest002"
password = "Test@1234"

cookie_string = """__cuid=76ac6e6c6137423a9845252e47ce176d;
kdt=G1t9rQJDgWuob1VbmwQ8Sort3CTxKvFm3M6aRAiV;
d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw;
guest_id_ads=v1%3A176087369242034482;
guest_id_marketing=v1%3A176087369242034482;
personalization_id="v1_eTXyf/9dgKGeQ7lQiz1gkg==";
dnt=1;
att=1-17CMITpiChC8NFNOhBb7GAcMX2Raigo3aODs4Biz;
gt=1980027948011843870;
guest_id=v1%3A176091042466176528;
__cf_bm=EZG74RCcRRx5MHizzUFiHZYRFpqFLuIhPyDwyvEKV0c-1760910451.5449271-1.0.1.1-3Q.bUhjNLf2NM6Ec6ixX0UEDKoPMDFlPfg3EhLXyQUxJHhOKvMJPuJF2PLhgGOU6S9ULb4QUiZZ1Knwb1b0h6s7DNQxRpfblnKF2llQ_z5.4116UKGR2MoGvv0QWCuax"""

class LoginX:
    async def run(self):
        browser = BrowserManager(headless=False, persistent=True)

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