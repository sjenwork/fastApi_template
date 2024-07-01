from fastapi import FastAPI

from app.api.endpoints import upload
from contextlib import asynccontextmanager
from app.utils.logger.create_logger import loggerWrapper


app = FastAPI(title="My FastAPI Project")
app.include_router(upload.router, prefix="/api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")


# app.lifespan(lifespan)
app.router.lifespan_context = lifespan


@app.get("/helloworld")
@loggerWrapper
async def hello_world(AccId: str = "-", OperateClass: str = "S"):
    return {"Hello": "World"}


@app.get("/helloworld2")
@loggerWrapper
async def hello_world2(AccId: str = "-", OperateClass: str = "S"):
    return {"Hello": "World"}
