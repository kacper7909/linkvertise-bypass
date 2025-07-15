import httpx

@app.post("/bypass")
async def bypass(request: Request):
    data = await request.json()
    url = data.get("url")

    if not url:
        return JSONResponse(content={"success": False, "url": None})

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://bypass.linkvertise.download/?url={url}")
            result = response.json()

            if "destination" in result:
                return JSONResponse(content={"success": True, "url": result["destination"]})
            else:
                return JSONResponse(content={"success": False, "url": None})
    except:
        return JSONResponse(content={"success": False, "url": None})
