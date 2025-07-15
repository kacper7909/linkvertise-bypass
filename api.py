from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from playwright.async_api import async_playwright
from datetime import datetime
import os

app = FastAPI()
LOG_FILE = "logs.txt"

@app.on_event("startup")
async def startup_event():
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if domain:
        print(f"https://{domain}/bypass?url=YOUR_ENCODED_LINKVERTISE_URL")
    else:
        print("No Railway domain found.")

async def bypass_linkvertise(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        final_url = page.url
        await browser.close()
        return final_url

def log_request(ip: str, url: str):
    time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {ip} → {url}\n")

@app.get("/bypass")
async def bypass(request: Request, url: str = Query(...)):
    if "linkvertise.com" not in url:
        raise HTTPException(status_code=400, detail="Must be a Linkvertise URL")
    ip = request.client.host
    log_request(ip, url)
    final_url = await bypass_linkvertise(url)
    return JSONResponse(content={"final_url": final_url})

@app.get("/logs")
async def view_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return PlainTextResponse(content=f.read())
    except FileNotFoundError:
        return PlainTextResponse(content="No logs yet.")
