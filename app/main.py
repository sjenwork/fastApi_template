from fastapi import FastAPI
from app.api.endpoints import api1
from contextlib import asynccontextmanager
from app.utils.db_utils import SQLServerConnection
from app.logging_config import setup_logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
import logging
from functools import wraps
import json
import copy


def test_sqlserver_connection():
    try:
        sqlserver_connection = SQLServerConnection()
        engine = sqlserver_connection.engine
        with engine.begin() as connection:
            connection.execute(text("SELECT top 1 * from config"))

            print("Database connection test successful.")
        return engine
    except SQLAlchemyError as e:
        raise Exception(f"資料庫連線失敗: {e}")


app = FastAPI(title="My FastAPI Project")
app.include_router(api1.router, prefix="/api")

engine = test_sqlserver_connection()
logging = setup_logging(engine=engine)
logger = logging.getLogger("prod")


function_name_mapping = {
    "hello_world": "哈囉世界",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")


# app.lifespan(lifespan)
app.router.lifespan_context = lifespan


def loggerWrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(kwargs)
        log = {}
        log["FunctionName"] = function_name_mapping.get(func.__name__, func.__name__)
        log["LogMessage"] = f"""執行「{log["FunctionName"]} 」。"""
        log["AccId"] = kwargs.get("AccId", "-")
        log["OperateClass"] = kwargs.get("OperateClass", "-")
        logger.info(json.dumps(log))
        result = func(*args, **kwargs)
        return result

    return wrapper


@app.get("/helloworld")
@loggerWrapper
def hello_world(AccId: str = "-", OperateClass: str = "S"):
    return {"Hello": "World"}


@app.get("/helloworld2")
@loggerWrapper
def hello_world2(AccId: str = "-", OperateClass: str = "S"):
    return {"Hello": "World"}
