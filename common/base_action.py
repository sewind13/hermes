import asyncio

class BaseAction:
    def __init__(self, page):
        self.page = page

    async def scroll_to_bottom(self, step=1000, delay=0.5):
        """Scroll ลงสุดของหน้า (แบบ async)"""
        height = await self.page.evaluate("() => document.body.scrollHeight")
        for i in range(0, height, step):
            await self.page.evaluate(f"window.scrollTo(0, {i});")
            await asyncio.sleep(delay)

    async def click_element(self, selector):
        await self.page.click(selector)

    async def wait_for_selector(self, selector, timeout=10000):
        await self.page.wait_for_selector(selector, timeout=timeout)
