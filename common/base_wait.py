import asyncio
import random
from typing import Union, Callable, Optional
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError


class BaseWait:
    """Reusable async wait helper with human-like delays and flexible conditions."""

    def __init__(self, page: Page):
        self.page = page

    # ------------- BASIC HUMAN WAITING ------------- #
    async def human_sleep(
        self,
        min_seconds: float = 0.3,
        max_seconds: float = 1.2,
        reason: Optional[str] = None,
    ):
        """Human-like random sleep."""
        duration = random.uniform(min_seconds, max_seconds)
        if reason:
            print(f"[wait] sleeping {duration:.2f}s ({reason})")
        await asyncio.sleep(duration)

    async def wait(self, seconds: float, reason: Optional[str] = None):
        """Deterministic sleep (fixed time)."""
        if reason:
            print(f"[wait] fixed {seconds:.2f}s ({reason})")
        await asyncio.sleep(seconds)

    # ------------- SELECTOR-BASED WAITS ------------- #
    async def wait_for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: int = 10000,
    ):
        try:
            await self.page.wait_for_selector(selector, state=state, timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            print(f"[wait_for_selector] Timeout waiting for {selector} -> {state}")
            return False

    async def wait_until_visible(self, selector: str, timeout: int = 10000):
        return await self.wait_for_selector(selector, state="visible", timeout=timeout)

    async def wait_until_hidden(self, selector: str, timeout: int = 10000):
        return await self.wait_for_selector(selector, state="hidden", timeout=timeout)

    async def wait_until_clickable(self, selector: str, timeout: int = 10000):
        """Wait until an element is both visible and enabled."""
        end_time = asyncio.get_event_loop().time() + timeout / 1000
        while True:
            try:
                locator = self.page.locator(selector)
                if await locator.is_visible() and await locator.is_enabled():
                    return True
            except Exception:
                pass

            if asyncio.get_event_loop().time() > end_time:
                print(f"[wait_until_clickable] Timeout: {selector}")
                return False
            await asyncio.sleep(0.3)

    async def wait_for_text(
        self,
        selector: str,
        text: str,
        timeout: int = 10000,
        exact: bool = False,
    ):
        """Wait until element's text contains or equals the given text."""
        end_time = asyncio.get_event_loop().time() + timeout / 1000
        while True:
            try:
                content = await self.page.text_content(selector)
                if content:
                    if (exact and content.strip() == text) or (not exact and text in content):
                        return True
            except Exception:
                pass

            if asyncio.get_event_loop().time() > end_time:
                print(f"[wait_for_text] Timeout waiting for '{text}' in {selector}")
                return False
            await asyncio.sleep(0.3)

    # ------------- ADVANCED WAITS ------------- #
    async def wait_for_condition(
        self,
        condition: Union[str, Callable, Callable[[], bool]],
        timeout: int = 10000,
        check_interval: float = 0.3,
        description: Optional[str] = None,
    ):
        """Wait for a custom condition (JS string, async fn, or callable)."""
        end_time = asyncio.get_event_loop().time() + timeout / 1000

        if isinstance(condition, str):
            async def check():
                return await self.page.evaluate(f"() => Boolean({condition})")
        elif asyncio.iscoroutinefunction(condition):
            check = condition
        elif callable(condition):
            async def check():
                return bool(condition())
        else:
            raise TypeError("Condition must be a string, callable, or async function")

        while True:
            try:
                if await check():
                    return True
            except Exception:
                pass

            if asyncio.get_event_loop().time() > end_time:
                msg = description or str(condition)
                print(f"[wait_for_condition] Timeout waiting for condition: {msg}")
                return False
            await asyncio.sleep(check_interval)

    async def wait_for_network_idle(self, timeout: int = 10000):
        """Wait until the network is idle (no ongoing requests)."""
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            print("[wait_for_network_idle] Timeout waiting for network to be idle")
            return False
