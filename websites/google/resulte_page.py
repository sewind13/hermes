# websites/example_site/pages/result_page.py
from common.base_page import BasePage

# ---------------------------------------------------------
# Page Object
# ---------------------------------------------------------

class ResultElements:
    RESULT_TITLES = "//div[@id='search']//a/h3"

class ResultPage(BasePage):

    async def get_results(self, limit: int = 5):
        await self.page.wait_for_selector(ResultElements.RESULT_TITLES)
        titles = await self.page.eval_on_selector_all(
            ResultElements.RESULT_TITLES,
            "nodes => nodes.map(n => n.textContent)"
        )
        return titles[:limit]
