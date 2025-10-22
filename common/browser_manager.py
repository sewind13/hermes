import random
import asyncio
from typing import Optional, Dict, List
from playwright.async_api import async_playwright, Page, BrowserContext, Response
from pathlib import Path

# ---------------------------------------------------------------------
# USER AGENT, LANGUAGE, TIMEZONE
# ---------------------------------------------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
]

LANGUAGES = [["en-US", "en"], ["th-TH", "th", "en-US"]]
TIMEZONES = ["Asia/Bangkok", "America/New_York", "Europe/London", "Asia/Tokyo"]

def default_headers_for_ua(ua: str) -> Dict[str, str]:
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://x.com/",
        # "Sec-Ch-Ua": '"Chromium";v="128", "Google Chrome";v="128", "Not:A-Brand";v="99"',
        "Sec-Ch-Ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Upgrade-Insecure-Requests": "1",
    }

# ---------------------------------------------------------------------
# BrowserManager (FINAL)
# ---------------------------------------------------------------------
class BrowserManager:
    def __init__(
        self,
        headless: bool = False,
        persistent: bool = True,
        user_agent: Optional[str] = None,
        proxy: Optional[dict] = None,
        headers: Optional[dict] = None,
        viewport: Optional[dict] = None,
        timeout: int = 25000,
        max_retries: int = 3,
        storage_path: Optional[str] = "./user_data/x",
        executable_path: Optional[str] = None,
        custom_cookie: Optional[str] = None,
    ):
        self.headless = headless
        self.persistent = persistent
        self.proxy = proxy
        self.viewport = viewport or {"width": 1366, "height": 768}
        self.timeout = timeout
        self.max_retries = max_retries
        self.user_agent = user_agent or random.choice(USER_AGENTS)
        self.languages = ["en-US", "en"] or random.choice(LANGUAGES)
        self.timezone = random.choice(TIMEZONES)
        self.headers = headers or default_headers_for_ua(self.user_agent)
        self.storage_path = Path(storage_path)
        self.executable_path = executable_path
        self.custom_cookie = custom_cookie
        self.playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    # -----------------------------------------------------------------
    async def __aenter__(self) -> Page:
        self.playwright = await async_playwright().start()
        args = [
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--disable-web-security",
            "--disable-extensions",
            "--disable-gpu",
            "--start-maximized",
            "--disable-features=IsolateOrigins,site-per-process,FedCm",
            "--ignore-certificate-errors",
        ]

        if self.proxy:
            args.append(f"--proxy-server={self.proxy.get('server')}")

        ignore_default_args = ["--enable-automation"]

        user_data_dir = str(self.storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # --- Persistent Context ---
        if self.persistent:
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=self.headless,
                args=args,
                ignore_default_args=ignore_default_args,
                viewport=self.viewport,
                ignore_https_errors=True,
                locale=self.languages[0],
                timezone_id=self.timezone,
                user_agent=self.user_agent,
                executable_path=self.executable_path or None,
            )
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        else:
            browser = await self.playwright.chromium.launch(headless=self.headless, args=args)
            self.context = await browser.new_context(
                viewport=self.viewport,
                user_agent=self.user_agent,
                locale=self.languages[0],
                timezone_id=self.timezone,
                ignore_https_errors=True,
            )
            self.page = await self.context.new_page()

        # -------------------------------------------------------------
        # ✅ Apply Safe Headers
        # -------------------------------------------------------------
        await self.context.set_extra_http_headers(self.headers)

        # ✅ If cookie string provided — store in context
        if self.custom_cookie:
            await self._inject_cookies(self.custom_cookie)

        # ✅ Add Stealth protection
        await self._add_stealth()

        # ✅ Add Listeners
        # self._attach_listeners()

        # ✅ Default timeout
        self.page.set_default_timeout(self.timeout)
        await asyncio.sleep(random.uniform(0.5, 1.2))

        return self.page

    # -----------------------------------------------------------------
    async def _inject_cookies(self, cookie_str: str):
        """Convert raw cookie string into context cookies"""
        cookies = []
        for c in cookie_str.split(";"):
            if "=" in c:
                name, value = c.strip().split("=", 1)
                cookies.append({
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": ".x.com",
                    "path": "/"
                })
        if cookies:
            await self.context.add_cookies(cookies)

    # -----------------------------------------------------------------
    async def _add_stealth(self):
        """Anti-bot fingerprint hiding script"""
        js = """
        // Hide webdriver
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

        // Fake plugins
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });

        // Fake languages
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });

        // Fake WebGL vendor/renderer
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Intel Inc.';
            if (parameter === 37446) return 'Intel Iris OpenGL Engine';
            return getParameter.call(this, parameter);
        };

        // Fake permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters)
        );

        // Disable Chrome automation flags
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """
        await self.page.add_init_script(js)

    # -----------------------------------------------------------------
    def _attach_listeners(self):
        """Console, error, and network logging"""
        # self.page.on("console", lambda msg: print(f"[console.{msg.type}] {msg.text()}"))
        self.page.on("pageerror", lambda e: print(f"[page.error] {e}"))
        self.page.on("requestfailed", lambda req: print(f"[request.failed] {req.url} -> {req.failure}"))
        self.page.on("response", lambda r: asyncio.create_task(self._on_response(r)))

    async def _on_response(self, response: Response):
        try:
            if any(k in response.url for k in ("login", "auth", "session", "/api/")):
                print(f"[response] {response.status} {response.url}")
        except Exception:
            pass

    # -----------------------------------------------------------------
    async def safe_goto(self, url: str):
        """Robust goto with retries + human delay"""
        for attempt in range(self.max_retries):
            try:
                await self.page.goto(url, wait_until="networkidle")
                await asyncio.sleep(random.uniform(1.2, 2.5))
                return True
            except Exception as e:
                print(f"[WARN] goto attempt {attempt+1} failed: {e}")
                await asyncio.sleep(1 + attempt)
        return False

    # -----------------------------------------------------------------
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.context.close()
        except Exception:
            pass
        await self.playwright.stop()
