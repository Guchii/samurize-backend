from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .logic import generate_summary, video_summary, wiki_summary

origins = ["*"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": True}


@app.post("/wiki-summarize")
async def wiki_summarize(title: str = "Electron"):
    summary = wiki_summary(title)
    return {"title": title, "summary": summary}


@app.post("/gensum")
async def generate_summaries(payload):
    summary = generate_summary([payload])
    return {"summary": summary}


@app.post("/video-summarize")
async def video_summarize(url: str):
    summary = video_summary(url)
    return {"url": url, "summary": summary}
