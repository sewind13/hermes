import asyncio
from websites.google.home_page import ExampleScraper

async def main():
    scraper = ExampleScraper()
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
