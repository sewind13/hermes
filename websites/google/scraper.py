from pages import Browser
import asyncio


async def main_scraper():
    async with Browser(headless=False) as page:
            
            await page.open("https://www.google.com")
            await page.search("Playwright Python async")
            title = await page.get_title_text()
            print("Page Title:", title)


if __name__ == "__main__":
    asyncio.run(main_scraper())