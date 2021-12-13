import logging

from sqlalchemy.orm import declarative_base

log_level = logging.WARN

display_name = "Regeltest-Creator"
app_name = "OmicronEditor"
app_author = "jfeil"
app_version = "0.0.3"

database_name = "database.db"
Base = declarative_base()
