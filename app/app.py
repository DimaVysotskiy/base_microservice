from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from .db import postgres_manager, redis_manager



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    postgres_manager.init()
    redis_manager.init()
    

    yield

    # Shutdown 
    await postgres_manager.close()
    await redis_manager.close()




app = FastAPI(lifespan=lifespan)