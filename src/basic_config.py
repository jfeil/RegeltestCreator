import logging
import sys
from typing import Any

from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

log_level = logging.WARN

display_name = "RegeltestCreator"
app_name = "RegeltestCreator"
app_author = "jfeil"
app_version = "0.1.1"

database_name = "database.db"

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    is_bundled = True
else:
    is_bundled = False


# Source: https://variable-scope.com/posts/setting-eager-defaults-for-sqlalchemy-orm-models
class EagerDefault:
    def __init__(self, value: Any):
        self.value = value


def defaults_included_constructor(instance, **kwds):
    mapper = inspect(instance).mapper
    for column in mapper.columns:
        if column.default is None:
            continue
        default = getattr(column.default, "arg")
        if default is not None:
            if isinstance(default, EagerDefault):
                attr = mapper.get_property_by_column(column)
                kwds.setdefault(attr.key, default.value)
    for attr, value in kwds.items():
        setattr(instance, attr, value)


Base = declarative_base(constructor=defaults_included_constructor)
