from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import asyncio
import os

app = FastAPI()

@app.post("/bypass")
async def bypass_linkvertise(req: Request):
    data = await req.json()
    url = data.get("url")
    if not url or "linkvertise" not in url:
        return JSONResponse(status_code=400, content={"error": "Invalid URL."})

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, timeout=60000)
            await asyncio.sleep(7)  # wait for Linkvertise timer
            await page.wait_for_selector("a[href^='https://']")

            final_url = await page.get_attribute("a[href^='https://']", "href")
            await browser.close()

            return {"final_url": final_url}

        except Exception as e:
            await browser.close()
            return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def root():
    return {"status": "Linkvertise bypasser is running."}
