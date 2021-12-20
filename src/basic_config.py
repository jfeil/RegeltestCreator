import logging

from sqlalchemy.orm import declarative_base

log_level = logging.WARN

display_name = "RegeltestCreator"
app_name = "RegeltestCreator"
app_author = "jfeil"
app_version = "0.1.1"

database_name = "database.db"
Base = declarative_base()
