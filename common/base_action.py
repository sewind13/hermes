import asyncio
import random
import time
from playwright.async_api import Locator, Page


class BaseAction:
    def __init__(self, page):
        self.page = page

    async def __execture_script(self, script: str):
        result = await self.page.evaluate(script)
        return result
    
    async def human_type(
        self,
        target,
        text: str,
        min_delay: float = 0.05,
        max_delay: float = 0.25,
        clear_first: bool = True
    ):
        
        """
        Typeing text as a human (accept both string selector and Locator object)
        """

        # Support both string selector and Locator object
        if isinstance(target, str):
            locator = self.page.locator(target)
        elif isinstance(target, Locator):
            locator = target
        else:
            raise TypeError("target ต้องเป็น string selector หรือ Locator object")


        if clear_first:
            await locator.fill("")

        for char in text:
            await locator.type(char)
            await asyncio.sleep(random.uniform(min_delay, max_delay))

            # simulate occasional longer pause
            if random.random() < 0.05:
                await asyncio.sleep(random.uniform(0.5, 1.2))

    async def human_mouse_move(self, start, end, duration=0.7, steps=25):
        """
        Move mouse as a human-like manner

        param:
            start: (x, y)
            end: (x, y)
            duration: total seconds
            steps: number of intermediate points
        """
        sx, sy = start
        ex, ey = end
        for i in range(1, steps+1):
            t = i/steps
            # simple ease-in-out cubic
            ease = 3*t**2 - 2*t**3
            # add small random jitter
            nx = sx + (ex - sx) * ease + random.uniform(-1.5, 1.5)
            ny = sy + (ey - sy) * ease + random.uniform(-1.5, 1.5)
            await self.page.mouse.move(nx, ny)
            await asyncio.sleep(duration/steps + random.uniform(-0.002, 0.01))

    async def random_scroll(self, total_distance=None, step_min=200, step_max=800):
        height = await self.page.evaluate("() => document.body.scrollHeight")
        pos = await self.page.evaluate("() => window.scrollY")
        if total_distance is None:
            total_distance = height - pos
        remaining = total_distance
        while remaining > 0:
            step = min(remaining, random.randint(step_min, step_max))
            pos += step
            await self.page.evaluate(f"window.scrollTo(0, {pos})")
            await asyncio.sleep(random.uniform(0.2, 1.0))
            remaining -= step

    async def human_click(self, target, before_move=True, pause_min=0.05, pause_max=0.2):
        """
        target can be selector string or Locator
        """
        from playwright.async_api import Locator
        if isinstance(target, str):
            locator = self.page.locator(target)
        elif isinstance(target, Locator):
            locator = target
        else:
            raise TypeError("target must be selector or Locator")

        box = await locator.bounding_box()
        if not box:
            raise Exception("Element not visible for click")
        cx = box["x"] + box["width"]/2
        cy = box["y"] + box["height"]/2

        current = await self.page.mouse.position() if hasattr(self.page.mouse, "position") else (cx + random.uniform(-50,50), cy + random.uniform(-50,50))
        if before_move:
            try:
                await self.human_mouse_move(current, (cx, cy), duration=random.uniform(0.15,0.6))
            except Exception:
                # fallback: direct move
                await self.page.mouse.move(cx, cy)
        await asyncio.sleep(random.uniform(pause_min, pause_max))
        await locator.click(force=False)



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
