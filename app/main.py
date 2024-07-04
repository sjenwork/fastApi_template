from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.endpoints import upload
from contextlib import asynccontextmanager

from app.utils.logger.logging_config import setup_logging
from app.utils.db_utils import sql_conn
from app.api.index import router
from app.utils.security_utils import generate_sha512_hash
import json


app = FastAPI(title="My FastAPI Project")
app.include_router(upload.router, prefix="/api")

engine = sql_conn.test_connection()
logging = setup_logging(engine=engine)
logger = logging.getLogger("prod")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")


# app.lifespan(lifespan)
app.router.lifespan_context = lifespan


@app.middleware("http")
async def middleware(request: Request, call_next):
    try:
        # 獲取路由路徑和參數
        path = request.url.path
        params = dict(request.query_params)

        # 這裡可以執行任何你想要的邏輯，例如記錄請求信息
        print(f"Path: {path}")
        print(f"Params: {params}")
        log = {}
        log["FunctionName"] = router.get(path)
        log["LogMessage"] = f"""執行「{log["FunctionName"]} 」。"""
        log["AccId"] = params.get("AccId", "-")
        log["OperateClass"] = params.get("OperateClass", "-")
        log["Hash"] = generate_sha512_hash(log["LogMessage"])
        logger.info(json.dumps(log, ensure_ascii=False))
        # 繼續處理請求
        response = await call_next(request)
        return response

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "detail": str(e)},
        )


@app.get("/helloworld")
# @loggerWrapper
def hello_world(AccId: str = "-", OperateClass: str = "S"):
    # logger_local.info("Hello World")
    return {"Hello": "World"}


@app.get("/helloworld2")
# @loggerWrapper
async def hello_world2(AccId: str = "-", OperateClass: str = "S"):
    return {"Hello": "World"}
