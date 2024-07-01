from app.utils.db_utils import SQLServerConnection
from app.utils.logger.logging_config import setup_logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from functools import wraps
from inspect import iscoroutinefunction
from app.utils.security_utils import generate_sha512_hash

import json


function_name_mapping = {
    "hello_world": "哈囉世界",
}


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


def loggerWrapper(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        log = {}
        log["FunctionName"] = function_name_mapping.get(func.__name__, func.__name__)
        log["LogMessage"] = f"""執行「{log["FunctionName"]} 」。"""
        log["AccId"] = kwargs.get("AccId", "-")
        log["OperateClass"] = kwargs.get("OperateClass", "-")
        log["Hash"] = generate_sha512_hash(log["LogMessage"])
        logger.info(json.dumps(log, ensure_ascii=False))
        result = await func(*args, **kwargs)
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        log = {}
        log["FunctionName"] = function_name_mapping.get(func.__name__, func.__name__)
        log["LogMessage"] = f"""執行「{log["FunctionName"]} 」。"""
        log["AccId"] = kwargs.get("AccId", "-")
        log["OperateClass"] = kwargs.get("OperateClass", "-")
        logger.info(json.dumps(log, ensure_ascii=False))
        result = func(*args, **kwargs)
        return result

    if iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


engine = test_sqlserver_connection()
logging = setup_logging(engine=engine)
logger = logging.getLogger("prod")
