from fastapi import FastAPI, Request, Response
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/home")
@limiter.limit("10/minute")
async def homepage(request: Request):
    return "test"

@app.get("/mars")
@limiter.limit("10/minute")
async def homepage(request: Request, response: Response):
    return {"key": "value"}