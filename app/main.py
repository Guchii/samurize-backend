from fastapi import FastAPI, Request, Response, Body
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from .scraper import getPara

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/home")
@limiter.limit("15/minute")
async def homepage(request: Request):
    return "test"

@app.post("/generate")
@limiter.limit("15/minute")
async def homepage(request: Request):
    print(await request.json())
    import time
    time.sleep(2)
    return {"key": "value"}

@app.get("/scraper/wiki")
async def wikiscraper(url : str = "https://en.wikipedia.org/wiki/Electron"):
    dic = getPara(url)
    return dic
