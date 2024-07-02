from app.utils.db_utils import sql_conn
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
        log["Hash"] = generate_sha512_hash(log["LogMessage"])
        logger.info(json.dumps(log, ensure_ascii=False))
        result = func(*args, **kwargs)
        return result

    if iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


# engine = test_sqlserver_connection()
engine = sql_conn.test_connection()
logging = setup_logging(engine=engine)
logger = logging.getLogger("prod")

logger_local = logging.getLogger("debug")
