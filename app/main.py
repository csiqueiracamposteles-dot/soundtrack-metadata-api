import logging
from contextlib import asynccontextmanager

# Load environment configuration
from app.core import config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cache import init_cache
from app.routers.soundtrack import router as soundtrack_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

log = logging.getLogger("soundtrack-api")


# ===========================================================
# LIFESPAN
# ===========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(
        "Soundtrack Metadata API started - profile=%s",
        config.ACTIVE_PROFILE
    )

    try:
        init_cache()
    except Exception as e:
        # Cache initialization failures should not stop the API.
        log.exception("Failed to initialize cache: %s", e)

    yield

    log.info("Soundtrack Metadata API stopped")


# ===========================================================
# FASTAPI APP
# ===========================================================
ROUTE_PREFIX = config.ROUTE_PREFIX

app = FastAPI(
    title="Soundtrack Metadata API",
    description="REST API for retrieving soundtrack metadata from public music and entertainment services.",
    version="1.0.0",
    docs_url=f"{ROUTE_PREFIX}/docs",
    redoc_url=f"{ROUTE_PREFIX}/redoc",
    openapi_url=f"{ROUTE_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# ===========================================================
# CORS
# ===========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================================
# ROUTERS
# ===========================================================
app.include_router(soundtrack_router, prefix=ROUTE_PREFIX)


# ===========================================================
# ROOT / HEALTH
# ===========================================================
@app.get("/healthz")
def healthz():
    return {"status": "healthy"}


@app.get(f"{ROUTE_PREFIX}/")
def home():
    return {
        "status": "ok",
        "api": "Soundtrack Metadata API",
        "profile": config.ACTIVE_PROFILE,
    }


@app.get(f"{ROUTE_PREFIX}/health")
def health():
    return {"status": "healthy"}