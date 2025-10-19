import asyncio
import sys
import os

# Get the absolute path two levels above the current file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# websites/example_site/scraper.py
from common.browser_manager import BrowserManager
from websites.google.home_page import GoogleElement, HomePage
from websites.google.resulte_page import ResultPage

class GoogleSearch:
    async def run(self):
        browser = BrowserManager(headless=False)

        async with browser as page:

            home_page = HomePage(browser, page)
            await home_page.open_google()
            await home_page.accept_consent()
            result_page = await home_page.search("Playwright Python async")

            print(">>> ดึงผลลัพธ์")
            results = await result_page.get_results(limit=5)

            print("\n=== Results ===")
            for i, r in enumerate(results, start=1):
                print(f"{i}. {r}")


if __name__ == "__main__":
    asyncio.run(GoogleSearch().run())