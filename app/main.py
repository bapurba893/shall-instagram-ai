from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import competitor, content, caption, hashtag, posting_time

app = FastAPI(
    title="Shall Instagram AI Growth Assistant",
    description="AI-powered Instagram growth tool for Shall — AI fashion startup",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(competitor.router, prefix="/competitor", tags=["Competitor Analysis"])
app.include_router(content.router, prefix="/content", tags=["Content Ideas"])
app.include_router(caption.router, prefix="/caption", tags=["Caption Generator"])
app.include_router(hashtag.router, prefix="/hashtags", tags=["Hashtag Engine"])
app.include_router(posting_time.router, prefix="/posting-time", tags=["Posting Time Predictor"])

@app.get("/", tags=["Health"])
def root():
    return {
        "app": "Shall Instagram AI Growth Assistant",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/competitor/analyze",
            "/content/ideas",
            "/caption/generate",
            "/hashtags/recommend",
            "/posting-time/predict",
            "/docs"
        ]
    }

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
