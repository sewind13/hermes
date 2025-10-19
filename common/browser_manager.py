import random
import asyncio
from playwright.async_api import async_playwright

USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
]

DEFAULT_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}

DEFAULT_PROXY = None  # หรือกำหนด {"server": "http://proxy.example:8080", "username": "foo", "password": "bar"}

class BrowserManager:
    def __init__(
        self,
        headless: bool = True,
        incognito: bool = True,
        user_agent: str | None = None,
        proxy: dict | None = None,
        headers: dict | None = None,
        viewport: dict | None = None,
        timeout: int = 20000,
        max_retries: int = 3,
    ):
        self.headless = headless
        self.incognito = incognito
        self.user_agent = user_agent or random.choice(USER_AGENTS)
        self.proxy = proxy or DEFAULT_PROXY
        self.headers = headers or DEFAULT_HEADERS
        self.viewport = viewport or {"width": 1366, "height": 768}
        self.timeout = timeout
        self.max_retries = max_retries
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()

        launch_args = {
            "headless": self.headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-infobars",
                "--disable-web-security",
                "--disable-gpu",
                "--start-maximized",
            ],
        }
        
        if self.proxy:
            launch_args["proxy"] = self.proxy

        self.browser = await self.playwright.chromium.launch(**launch_args)

        context_args = {
            "viewport": self.viewport,
            "ignore_https_errors": True,
            "user_agent": self.user_agent,
            "extra_http_headers": self.headers,
            "java_script_enabled": True,
            "locale": "en-US",
            "timezone_id": "Asia/Bangkok",
        }

        self.context = await self.browser.new_context(**context_args)
        self.page = await self.context.new_page()
        await self._stealth_script()
        self.page.set_default_timeout(self.timeout)

        return self.page

    async def _stealth_script(self):
        """จำลอง behavior ของ human browser เพื่อลดการถูก detect"""
        await self.page.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) =>
                parameters.name === 'notifications'
                    ? Promise.resolve({ state: Notification.permission })
                    : originalQuery(parameters);
            """
        )

    async def safe_goto(self, url: str):
        """เข้าเว็บแบบ retry หลายครั้งเมื่อเจอ error"""
        for attempt in range(self.max_retries):
            try:
                await self.page.goto(url, wait_until="domcontentloaded")
                return True
            except Exception as e:
                print(f"[WARN] Attempt {attempt+1} failed: {e}")
                await asyncio.sleep(2 + attempt)
        print(f"[ERROR] Failed to open {url} after {self.max_retries} attempts")
        return False

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
