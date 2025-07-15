from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

async def bypass_linkvertise(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
    
        final_url = page.url
        await browser.close()
        return final_url

@app.get("/bypass")
async def bypass(url: str = Query(..., description="Linkvertise URL to bypass")):
    if "linkvertise.com" not in url:
        raise HTTPException(status_code=400, detail="URL must be a Linkvertise link")
    try:
        final_url = await bypass_linkvertise(url)
        return JSONResponse(content={"final_url": final_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
