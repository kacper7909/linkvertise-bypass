from fastapi import FastAPI

app = FastAPI()

@app.get("/api/bypass")
async def test():
    return {"status": "working"}
