from playwright.sync_api import Page, TimeoutError

class BaseState:
    """
    Helper class for checking element states in Playwright.
    Provides common methods for verifying existence, visibility, enablement, etc.
    """

    def __init__(self, page: Page, timeout: int = 5000):
        self.page = page
        self.timeout = timeout

    def is_exists(self, selector: str) -> bool:
        """Check if element exists in the DOM."""
        count = self.page.locator(selector).count()
        return count > 0

    def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        try:
            return self.page.locator(selector).is_visible()
        except Exception:
            return False

    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled (e.g., buttons, inputs)."""
        try:
            return self.page.locator(selector).is_enabled()
        except Exception:
            return False

    def wait_for_visible(self, selector: str, timeout: int = None) -> bool:
        """Wait until element becomes visible."""
        timeout = timeout or self.timeout
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except TimeoutError:
            return False

    def wait_for_disappear(self, selector: str, timeout: int = None) -> bool:
        """Wait until element disappears."""
        timeout = timeout or self.timeout
        try:
            self.page.locator(selector).wait_for(state="hidden", timeout=timeout)
            return True
        except TimeoutError:
            return False

    def get_text(self, selector: str) -> str:
        """Get element's text if exists and visible."""
        if self.is_visible(selector):
            return self.page.locator(selector).inner_text()
        return ""

    def click_if_visible(self, selector: str) -> bool:
        """Click element if visible and enabled."""
        if self.is_visible(selector) and self.is_enabled(selector):
            self.page.locator(selector).click()
            return True
        return False
