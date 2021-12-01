import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from appdirs import AppDirs
from basic_config import app_name, app_author, app_version, database_name


Base = declarative_base()


class DatabaseConnector:
    database_engine = None

    def __init__(self):
        dirs = AppDirs(appname=app_name, appauthor=app_author, version=app_version)
        database_path = os.path.join(dirs.user_data_dir, database_name)
        print(dirs.user_data_dir)
        not_exist = False
        if not os.path.isdir(dirs.user_data_dir):
            os.makedirs(dirs.user_data_dir, )
            not_exist = True
        elif not os.path.isfile(database_path):
            not_exist = True

        self.database_engine = create_engine(f"sqlite+pysqlite:///{database_path}", echo=True, future=True)

        if not_exist:
            self._init_database()

    def _init_database(self):
        # Create database based on basis - need to read docu first lol
        pass

    def __bool__(self):
        # check if database is empty :)
        pass

    def fill_database(self, arg_1, arg_2, arg_3):
        # insert processed values into db
        pass


db = DatabaseConnector()
