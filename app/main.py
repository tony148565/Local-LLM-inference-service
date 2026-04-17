from fastapi import FastAPI

from app.api.analyze import router_api as analyze_router
from app.api.classify import router_api as classify_router
from app.api.track2event import router_api as track2event_router
from app.dependencies import local_backend

app = FastAPI(title="Local AI Backend")


@app.get("/health")
def health() -> dict:
    return local_backend.health()


app.include_router(analyze_router)
app.include_router(classify_router)
app.include_router(track2event_router)