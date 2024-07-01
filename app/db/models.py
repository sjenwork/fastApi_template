from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func


Base = declarative_base()


class Log(Base):
    __tablename__ = "my_test_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String)
    name = Column(String)
    level = Column(String)
    message = Column(String)


class WebOpteLog(Base):
    __tablename__ = "WebOpteLog"
    WOL_id = Column(Integer, primary_key=True, autoincrement=True)
    CreateDate = Column(DateTime, default=func.getdate())
    AccId = Column(String(15), nullable=False)
    OperateClass = Column(String(1), nullable=False)
    LogMessage = Column(String(4000), nullable=False)
    FunctionName = Column(String(255), default="")
    Hash = Column(String(255), nullable=False)
