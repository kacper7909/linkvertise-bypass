from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

@app.get("/api/bypass")
async def bypass(request: Request):
    url = request.query_params.get("url")
    if not url or "linkvertise.com" not in url:
        return JSONResponse(status_code=400, content={"success": False, "error": "Invalid Linkvertise URL"})

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            await asyncio.sleep(5) 

           
            for _ in range(15):
                current = page.url
                if "linkvertise" not in current:
                    await browser.close()
                    return {"success": True, "url": current}
                await asyncio.sleep(1)

            await browser.close()
            return {"success": False, "error": "Bypass timed out"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
