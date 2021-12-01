import logging

from sqlalchemy.orm import declarative_base

log_level = logging.DEBUG

app_name = "OmicronEditor"
app_author = "jfeil"
app_version = "0.0.1"

database_name = "database.db"
Base = declarative_base()
