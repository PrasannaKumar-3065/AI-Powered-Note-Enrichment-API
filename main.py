from fastapi import FastAPI, Request
from app.api.notes import router
from app.core.database import Base, engine
from fastapi.responses import JSONResponse
import httpx

from core.exceptions import GlobalExceptionHandler

app = FastAPI(title="Notes API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    app.state.http_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown():
    await app.state.http_client.aclose()

@app.exception_handler(GlobalExceptionHandler)
async def global_http_exception_handler(
    request: Request,
    exc: GlobalExceptionHandler,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

app.include_router(router)