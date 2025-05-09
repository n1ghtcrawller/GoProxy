from fastapi import FastAPI, Request
from app.api.routes.auth import router as auth_router
from app.api.routes.ss_links import router as ss_router
from app.db.base import Base
from app.db.session import engine
import asyncio
import logging
from app.bot.bot import start_bot
from app.log.log import setup_logging
import uvicorn
app = FastAPI()



@app.middleware("http")
async def log_requests(request: Request, call_next):
    loggers = logging.getLogger("request")
    loggers.info(f"Request: {request.method} {request.url}")

    try:
        response = await call_next(request)
    except Exception as e:
        loggers.error(f"Error: {str(e)}")
        raise

    loggers.info(f"Response: {response.status_code}")
    return response


@app.on_event("startup")
async def on_startup():
    setup_logging()
    loggers = logging.getLogger(__name__)
    loggers.info("Starting application...")

    try:
        asyncio.create_task(start_bot())
        loggers.info("Bot started successfully")
    except Exception as e:
        loggers.error(f"Error starting bot: {str(e)}")
        raise
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    loggers = logging.getLogger(__name__)
    loggers.info("Shutting down application...")



app.include_router(auth_router)
app.include_router(ss_router)




if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting server...")
    uvicorn.run("main:app", reload=True, port=8001)