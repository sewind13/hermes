import asyncio
import random
import time
from playwright.async_api import Locator, Page


class BaseAction:
    def __init__(self, page):
        self.page = page

    async def __execute_script(self, script: str):
        result = await self.page.evaluate(script)
        return result
    
    async def __get_locator(self, target):
        '''
        Get Locator object from string selector or Locator object
        Args:
            target (str | Locator): Selector or Locator of the element.
        Returns:
            Locator: Locator object
        '''
        if isinstance(target, str):
            locator = self.page.locator(target)
        elif isinstance(target, Locator):
            locator = target
        else:
            raise TypeError("target must be text selector or locator object")
        return locator
    
    async def human_type(
        self,
        target,
        text: str,
        min_delay: float = 0.05,
        max_delay: float = 0.25,
        clear_first: bool = True
    ):
        
        """
        Type text into input field in a human-like manner
        param:
            target: str or Locator - selector or Locator of the input field
            text: str - text to type
            min_delay: float - minimum delay between keystrokes
            max_delay: float - maximum delay between keystrokes
            clear_first: bool - whether to clear the field before typing    
        """

        locator = await self.__get_locator(target)

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
        Move mouse from start to end in a human-like manner
        param:
            start: tuple(float, float) - starting (x, y) position
            end: tuple(float, float) - ending (x, y) position
            duration: float - total duration of the movement
            steps: int - number of intermediate steps
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
        '''
        Scroll the page down by a total distance in random steps
        param:
            total_distance: int - total distance to scroll (if None, scroll to bottom)
            step_min: int - minimum step size
            step_max: int - maximum step size
        '''
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
        '''
        Click element in a human-like manner
        param:
            target: str or Locator - selector or Locator of the element to click
            before_move: bool - whether to move mouse to element before clicking
            pause_min: float - minimum pause before click
            pause_max: float - maximum pause before click
        '''
       
        locator = await self.__get_locator(target)

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

    async def _human_like_mouse_move(self, target_x: float, target_y: float):
        '''
        Smooth, human-like mouse path movement.
        param:
            target_x: float - target x coordinate
            target_y: float - target y coordinate
        '''
        try:
            last_pos = await self.page.evaluate(
                "({x: window._lastMouseX || 0, y: window._lastMouseY || 0})"
            )
            start_x, start_y = last_pos["x"], last_pos["y"]
        except:
            start_x, start_y = random.randint(0, 50), random.randint(0, 50)

        steps = random.randint(20, 40)
        for i in range(steps):
            t = i / steps
            ease = 3 * t ** 2 - 2 * t ** 3  # smooth easing
            x = start_x + (target_x - start_x) * ease + random.uniform(-0.5, 0.5)
            y = start_y + (target_y - start_y) * ease + random.uniform(-0.5, 0.5)
            await self.page.mouse.move(x, y)
            await self.page.evaluate(f"window._lastMouseX={x};window._lastMouseY={y};")
            await asyncio.sleep(random.uniform(0.01, 0.04))

    async def move_mouse_to_element(
        self,
        target,
        jitter: bool = True,
        retry: int = 3,
        settle_delay: float = 0.2,
    ):
        '''
        Move mouse to element (accepts str or Locator).
        param:
            target: str or Locator - selector or Locator of the element
            jitter: bool - whether to add small random jitter to final position
            retry: int - number of retry attempts
            settle_delay: float - delay after scrolling into view
        '''
        for attempt in range(retry):
            try:

                locator = await self.__get_locator(target)

                # normalize to Locator
                box = await locator.bounding_box()
                if not box:
                    raise Exception("Element not visible")

                # ensure visible
                await locator.scroll_into_view_if_needed()
                await asyncio.sleep(settle_delay + random.uniform(0.1, 0.3))

                # compute random position
                offset_x = random.uniform(-3, 3) if jitter else 0
                offset_y = random.uniform(-3, 3) if jitter else 0
                x = box["x"] + box["width"] / 2 + offset_x
                y = box["y"] + box["height"] / 2 + offset_y

                # simulate human-like mouse movement
                await self._human_like_mouse_move(x, y)
                return True

            except Exception as e:
                print(f"[WARN] move_to_element attempt {attempt+1} failed: {e}")
                await asyncio.sleep(0.6)
        return False

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


    async def human_scroll_to_bottom(
        self,
        target=None,
        scroll_step_range=(200, 400),
        delay_range=(0.2, 0.6),
        settle_wait=0.8,
    ):
        """
        Human-like scroll to the bottom of the page or a scrollable element.

        Args:
            target (str | Locator | None): Element to scroll. None = scroll main page.
            scroll_step_range (tuple): Min/max pixels per scroll step.
            delay_range (tuple): Min/max delay between scroll steps.
            settle_wait (float): Wait time after finishing scroll.
        """
        # --- scroll the main page ---
        if target is None:
            scroll_height = await self.page.evaluate("document.body.scrollHeight")
            current = await self.page.evaluate("window.scrollY")

            while current < scroll_height:
                step = random.randint(*scroll_step_range)
                await self.page.evaluate(f"window.scrollBy(0, {step});")
                current += step
                await asyncio.sleep(random.uniform(*delay_range))
                scroll_height = await self.page.evaluate("document.body.scrollHeight")

            await asyncio.sleep(settle_wait)
            return True

        # --- scroll inside a specific element ---
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        element_handle = await locator.element_handle()
        if not element_handle:
            raise ValueError("Target element not found or not visible")

        scroll_height = await element_handle.evaluate("(el) => el.scrollHeight")
        scroll_top = await element_handle.evaluate("(el) => el.scrollTop")
        client_height = await element_handle.evaluate("(el) => el.clientHeight")

        while scroll_top + client_height < scroll_height:
            step = random.randint(*scroll_step_range)
            await element_handle.evaluate("(el, s) => el.scrollBy(0, s)", step)
            scroll_top = await element_handle.evaluate("(el) => el.scrollTop")
            scroll_height = await element_handle.evaluate("(el) => el.scrollHeight")
            await asyncio.sleep(random.uniform(*delay_range))

        await asyncio.sleep(settle_wait)
        print("[INFO] Finished human-like scroll to bottom of element.")
        return True
       