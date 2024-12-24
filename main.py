import asyncio
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from  fastapi.responses import RedirectResponse, JSONResponse

app = FastAPI(debug=True)



@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/hello")
async def hello_rout(user: str = "Anonimus"):
    await asyncio.sleep(0.2)
    return f"Hello, {user}!"

@app.middleware("http")
async def middleware(request: Request, call_next):
    method = request.method
    url = str(request.url.path)
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    response = await call_next(request)
    bad_urls = ["/docs", "/openapi.json"]

    if url not in bad_urls:
        logs = f"Method: {method}, URL: {url}, Time: {time}\n"
        with open("logs.txt", "a") as log_file:
            log_file.write(logs)

    exempt_urls = ["/", "/docs", "/openapi.json"]

    if url not in exempt_urls:
        if "X-Special-Header" not in request.headers:
            log_entry = f"WARNING: X-Special-Header didn`t find for  {method} {url} in {time}\n"
            with open("logs.txt", "a") as log_file:
                log_file.write(log_entry)


    return response


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)