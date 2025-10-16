import asyncio
from websites.google.scraper import ExampleScraper

async def main():
    scraper = ExampleScraper()
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
