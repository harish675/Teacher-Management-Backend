from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware



from typing import Annotated
import logging
from pythonjsonlogger import jsonlogger

from .router import router
from .lib.database import mongo_connection

# ---------------------
# Logging Configuration
# ---------------------
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()  # You can replace with FileHandler
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s %(funcName)s %(lineno)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


# ---------------------
# FastAPI Lifespan
# ---------------------
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("##########Startup###############")
    try:
        logger.debug("Connecting to MongoDB...")
        mongo_connection.connect()
        logger.debug("MongoDB connected successfully.")

        # Seed initial data
        from .modules.seed_data.seed_data import SeedData
        SeedData()

        yield
    finally:
        logger.debug("##########Shutdown###############")
        mongo_connection.close()


# ---------------------
# FastAPI App Instance
# ---------------------
app = FastAPI(root_path="/rent-easy/api", lifespan=lifespan)


# ---------------------
# Exception Handling
# ---------------------
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    logger.error(f"Unhandled exception occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "An internal server error occurred. Please try again later."
        },
    )


# ---------------------
# CORS Middleware
# ---------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Include Routes
# ---------------------
app.include_router(router)


