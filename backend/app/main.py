from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import alerts, auth, dashboard, endpoints, history, incidents
from app.core.errors import register_exception_handlers
import app.models  # noqa: F401  (registers all tables)
from app.database.base import Base
from app.database.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="OpsGuard API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from your Render frontend and local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

register_exception_handlers(app)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(endpoints.router, prefix="/endpoints", tags=["endpoints"])
app.include_router(history.router, tags=["history"])
app.include_router(incidents.router, tags=["incidents"])
app.include_router(alerts.router, tags=["alerts"])
app.include_router(dashboard.router, tags=["dashboard"])


@app.get("/health")
def health():
    return {"status": "ok"}