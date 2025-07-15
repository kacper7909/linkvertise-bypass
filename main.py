from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/bypass")
async def bypass(request: Request):
    try:
        data = await request.json()
        url = data.get("url")
    except:
        return JSONResponse(content={"success": False, "url": None})

    if not url:
        return JSONResponse(content={"success": False, "url": None})

    # fake bypass result
    return JSONResponse(content={"success": True, "url": "https://bypassed.com/example"})
