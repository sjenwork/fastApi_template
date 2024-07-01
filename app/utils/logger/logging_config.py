import logging
import logging.config
import yaml
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Log, WebOpteLog
import json
import os

default_logging_config = "app/config/logging_config.yaml"


class SQLServerHandler(logging.Handler):
    def __init__(self, engine: Engine = None):
        logging.Handler.__init__(self)
        self.engine = engine
        self.metadata = MetaData()

        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def emit(self, record):
        session = self.Session()
        # log_dict = {
        #     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #     "name": record.name,
        #     "level": record.levelname,
        #     "message": record.msg,
        # }

        message = json.loads(record.msg)
        log_dict = {
            "AccId": message["AccId"],
            "OperateClass": message["OperateClass"],
            "LogMessage": message["LogMessage"],
            "FunctionName": message["FunctionName"],
            "Hash": message["Hash"],
        }
        log_entry = WebOpteLog(**log_dict)
        session.add(log_entry)
        session.commit()
        session.close()


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, "client_addr"):
            record.client_addr = record.client_addr
        else:
            record.client_addr = "N/A"

        if hasattr(record, "request_line"):
            record.request_line = record.request_line
        else:
            record.request_line = "N/A"

        if hasattr(record, "status_code"):
            record.status_code = record.status_code
        else:
            record.status_code = "N/A"

        return super().format(record)


def setup_logging(default_path=default_logging_config, default_level=logging.INFO, env_key="LOG_CFG", engine=None):
    """Setup logging configuration"""

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value

    # Register the custom SQLServerHandler if an engine is provided
    if engine:
        if os.path.exists(path):
            with open(path, "rt") as f:
                config = yaml.safe_load(f.read())
            config["handlers"]["sql_server"]["engine"] = engine  # 直接傳入 engine
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    return logging
