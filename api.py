from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from playwright.async_api import async_playwright
from datetime import datetime
import os

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    print(f"https://{domain}/bypass?url=" if domain else "No Railway domain")

@app.get("/bypass")
async def bypass(request: Request, url: str = Query(...)):
    if "linkvertise.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid URL")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        final_url = page.url
        await browser.close()
    with open("logs.txt", "a") as f:
        f.write(f"[{datetime.utcnow()}] {request.client.host} → {url}\n")
    return JSONResponse(content={"final_url": final_url})

@app.get("/logs")
async def view_logs():
    try:
        with open("logs.txt", "r") as f:
            return PlainTextResponse(content=f.read())
    except:
        return PlainTextResponse(content="No logs")
