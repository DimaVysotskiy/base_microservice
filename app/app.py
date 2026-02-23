from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .db import postgres_manager, redis_manager
from .core import settings



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


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)