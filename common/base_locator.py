from playwright.async_api import Page, Locator

class BaseLocator:
    """Base class สำหรับหา elements แบบยืดหยุ่น"""

    def __init__(self, page: Page):
        self.page = page

    def get_locator_by_text(self, text: str) -> Locator:
        """หา element ที่มีข้อความตรงกับ text"""
        return self.page.get_by_text(text, exact=True)

    def get_locator_by_partial_text(self, text: str) -> Locator:
        """หา element ที่มีข้อความบางส่วนตรงกับ text"""
        return self.page.get_by_text(text, exact=False)

    def get_locator_by_xpath(self, xpath: str) -> Locator:
        """หา element ด้วย XPath"""
        return self.page.locator(f"xpath={xpath}")

    def get_locator_by_role(self, role: str, name: str | None = None) -> Locator:
        """หา element ด้วย role เช่น button, link, textbox"""
        return self.page.get_by_role(role, name=name)

    def get_locator_by_label(self, label: str) -> Locator:
        """หา input element ด้วย label"""
        return self.page.get_by_label(label)

    def get_locator_by_placeholder(self, placeholder: str) -> Locator:
        """หา input element ด้วย placeholder"""
        return self.page.get_by_placeholder(placeholder)

    def get_locator_by_alt_text(self, alt_text: str) -> Locator:
        """หา element (เช่น <img>) ด้วย alt text"""
        return self.page.get_by_alt_text(alt_text)
