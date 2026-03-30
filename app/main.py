from fastapi import FastAPI
from app.core.config import settings
from app.api import auth, documents

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME
    }