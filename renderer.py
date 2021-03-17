import asyncio
import os
from datetime import datetime
from pyppeteer import launch


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({"width": 1440, "height": 900})
    await page.goto("http://localhost:8000")
    await page.screenshot(
        {
            "path": os.path.join("output", f"{datetime.now().date().isoformat()}.png"),
            "fullPage": "true",
        }
    )
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
