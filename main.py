from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/bypass")
async def bypass(request: Request, url: str = Query(...)):
    if "linkvertise.com" not in url:
        return JSONResponse(content={"success": False, "url": None})

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        final_url = page.url
        await browser.close()

    return JSONResponse(content={"success": True, "final_url": final_url})
