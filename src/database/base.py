import os
import sys

sys.path.insert(0, os.getcwd())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from src.utils.custom_error_handlers import ConfigError, DBError
from src.utils.common_logger import logger
from src.settings import load_config
from src.orm_models import db_models


class DBConnector:
    def __init__(self):
        self.__check_config()
        self.__init_db()
        self.__init_session_maker()
        self.__init_tables()

    def __check_config(self):
        # Load parameters from .ENV
        if os.path.isfile("ENV"):
            load_config("ENV")

        self.DB_USER = os.environ.get("DB_USER")
        self.DB_PASSWORD = os.environ.get("DB_PASSWORD")
        self.DB_HOST = os.environ.get("DB_HOST")
        self.DB_PORT = os.environ.get("DB_PORT")
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_DRIVER = os.environ.get("DB_DRIVER")

        # Check required fields exist
        if None in [
            os.environ.get("DB_USER"),
            os.environ.get("DB_PASSWORD"),
            os.environ.get("DB_HOST"),
            os.environ.get("DB_PORT"),
            os.environ.get("DB_NAME"),
        ]:

            logger.error("Could not retrieve DB config")
            raise ConfigError("Could not retrieve DB config")

        # Create connection string
        # self.connection_string = f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}?driver={self.DB_DRIVER}"
        self.connection_string = f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    def __init_db(self):
        """
        Create SQLAlchemy DB connector engine and create database if it does not exist
        """
        self.engine = create_engine(self.connection_string)

        # Create database if not exist
        if not database_exists(self.engine.url):
            try:
                create_database(self.engine.url)
            except Exception as err:
                raise DBError(f"Failed to create database {err}")

    def __init_session_maker(self):
        """
        Create DB session maker
        """
        try:
            self.Session = sessionmaker(bind=self.engine)
        except Exception as err:
            raise DBError(f"Failed to create database session {err}")

    def __init_tables(self):
        for table_model in db_models.ModelOrder.tables:
            table_model.__table__.create(bind=self.engine, checkfirst=True)

    def drop_and_create_tables(self):
        for table_model in reversed(db_models.ModelOrder.tables):
            table_model.__table__.drop(self.engine)
        self.__init_tables()

    def get_session(self):
        """
        Get DB session
        :return: Session
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
