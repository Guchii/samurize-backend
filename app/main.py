from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .model import query
from .scraper import getPara

origins = ["*"]


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


@app.get("/scraper/wiki")
async def wiki_scraper(url: str = "https://en.wikipedia.org/wiki/Electron"):
    dic = getPara(url)
    return dic


@app.post("/gensum")
async def generate_summary(payload):
    output = query({"inputs": payload})
    return output
