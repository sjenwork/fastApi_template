import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from urllib.parse import quote
import importlib

Base = declarative_base()


class PostgresConnection:
    def __init__(self, dotenv_path=None, user=None, password=None, database=None, host=None, port=None):
        # 如果提供了 dotenv_path，則載入該路徑下的 .env 檔案；否則，載入預設路徑下的 .env 檔案
        if dotenv_path:
            load_dotenv(dotenv_path=dotenv_path)
            self.env_path = dotenv_path
        else:
            default_dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", ".env")
            load_dotenv(dotenv_path=default_dotenv_path)
            self.env_path = default_dotenv_path

        self.print_env_sources()
        # 使用初始化引數覆蓋 .env 檔案中的預設值
        self.user = user or self.get_config("POSTGRES_USER")
        # self.password = password or self.get_config("POSTGRES_PASSWORD")
        self.password = quote(password or self.get_config("POSTGRES_PASSWORD"))
        self.database = database or self.get_config("POSTGRES_DB")
        self.host = host or self.get_config("POSTGRES_HOST")
        self.port = port or self.get_config("POSTGRES_PORT")

        self.engine = None
        self.SessionLocal = None

        # 列印載入的 .env 檔案路徑和環境變數
        self.print_env_variables()

        # 建立 SQLAlchemy 引擎和會話
        self.create_engine_and_session()

    def get_config(self, key):
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Configuration for {key} not found. Ensure .env file or environment variable is set.")
        return value

    def create_engine_and_session(self):
        DATABASE_URL = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

        # 建立 SQLAlchemy 引擎，包含連線池
        self.engine = create_engine(
            DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800, pool_pre_ping=True
        )

        # 建立會話工廠
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    def create_tables(self):
        try:
            Base.metadata.create_all(self.engine, checkfirst=True)
        except SQLAlchemyError as e:
            print(f"Error creating tables: {e}")

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def print_env_sources(self):
        print(f"Loaded environment variables from: {self.env_path}")

    def print_env_variables(self):
        print(f"POSTGRES_USER: {self.user}")
        # print(f"POSTGRES_PASSWORD: {self.password}")
        print(f"POSTGRES_DB: {self.database}")
        print(f"POSTGRES_HOST: {self.host}")
        print(f"POSTGRES_PORT: {self.port}")

    def insert_gdf(self, gdf, model_class, geom_col="geometry"):
        session = self.SessionLocal()
        try:
            for _, row in gdf.iterrows():
                geom_wkt = row["geometry"].wkt  # 獲取幾何資料的 WKT 表示
                data = model_class(
                    **{col: row[col] for col in gdf.columns if col != geom_col}, geom=f"SRID=4326;{geom_wkt}"
                )  # 假設 SRID 為 4326
                session.add(data)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def load_model(self, model_path, model_class_name):
        spec = importlib.util.spec_from_file_location(model_class_name, model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, model_class_name)

    def delete_row(self, model_class, filters):
        session = self.SessionLocal()
        try:
            query = session.query(model_class)
            for attr, value in filters.items():
                query = query.filter(getattr(model_class, attr) == value)
            rows_deleted = query.delete(synchronize_session=False)
            session.commit()
            print(f"{rows_deleted} row(s) deleted successfully.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting data: {e}")
        finally:
            session.close()


class SQLServerConnection:
    def __init__(self, dotenv_path=None, user=None, password=None, database=None, host=None, port=None):
        # 如果提供了 dotenv_path，則載入該路徑下的 .env 檔案；否則，載入預設路徑下的 .env 檔案
        if dotenv_path:
            load_dotenv(dotenv_path=dotenv_path)
            self.env_path = dotenv_path
        else:
            default_dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", ".env")

            load_dotenv(dotenv_path=default_dotenv_path)
            self.env_path = default_dotenv_path

        self.print_env_sources()
        # 使用初始化引數覆蓋 .env 檔案中的預設值
        self.user = user or self.get_config("SQLSERVER_USER")
        self.password = quote(password or self.get_config("SQLSERVER_PASSWORD"))
        self.database = database or self.get_config("SQLSERVER_DB")
        self.host = host or self.get_config("SQLSERVER_HOST")
        self.port = port or self.get_config("SQLSERVER_PORT")

        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()

        # 列印載入的 .env 檔案路徑和環境變數
        self.print_env_variables()

        # 建立 SQLAlchemy 引擎和會話
        self.create_engine_and_session()

    def get_config(self, key):
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Configuration for {key} not found. Ensure .env file or environment variable is set.")
        return value

    def create_engine_and_session(self):
        DATABASE_URL = (
            f"mssql+pymssql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8"
        )
        # 建立 SQLAlchemy 引擎，包含連線池
        self.engine = create_engine(
            DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800, pool_pre_ping=True
        )

        # 建立會話工廠
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    def create_tables(self):
        try:
            self.Base.metadata.create_all(self.engine, checkfirst=True)
        except SQLAlchemyError as e:
            print(f"Error creating tables: {e}")

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def print_env_sources(self):
        if not os.path.exists(self.env_path):
            print(f".env file ({self.env_path}) not found")
        else:
            print(f"Loaded environment variables from: {self.env_path}")

    def print_env_variables(self):
        print(f"SQLSERVER_USER: {self.user}")
        print(f"SQLSERVER_DB: {self.database}")
        print(f"SQLSERVER_HOST: {self.host}")
        print(f"SQLSERVER_PORT: {self.port}")

    def test_connection(self):
        try:
            with self.engine.connect() as connection:
                result = connection.execute("SELECT 1")
                print("Database connection successful.")
        except SQLAlchemyError as e:
            print(f"Database connection failed: {e}")

    def load_model(self, model_path, model_class_name):
        spec = importlib.util.spec_from_file_location(model_class_name, model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, model_class_name)

    def delete_row(self, model_class, filters):
        session = self.SessionLocal()
        try:
            query = session.query(model_class)
            for attr, value in filters.items():
                query = query.filter(getattr(model_class, attr) == value)
            rows_deleted = query.delete(synchronize_session=False)
            session.commit()
            print(f"{rows_deleted} row(s) deleted successfully.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error deleting data: {e}")
        finally:
            session.close()
