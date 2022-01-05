import json
import logging
import pathlib
import platform
import sys
from typing import Any, Tuple, Union

import requests
from packaging import version
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

log_level = logging.WARN

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    is_bundled = True
else:
    is_bundled = False

display_name = "RegeltestCreator"
app_name = "RegeltestCreator"
app_author = "jfeil"
app_version = "0.2.2"

api_url = "https://api.github.com/repos/jfeil/RegeltestCreator/releases"

if not is_bundled:
    app_version = f"{app_version}dev"
app_version = version.parse(app_version)

database_name = "database.db"


def check_for_update() -> Union[None, Tuple[str, str, str, str]]:  # new_version, description, url, download_url
    latest_release = json.loads(requests.get(api_url).text)[0]
    if version.parse(latest_release['tag_name']) > app_version:
        download_url = None
        if not app_version.is_devrelease:
            current_platform = platform.system()
            fileending = {'Darwin': ['.app', '.zip'],
                          'Windows': ['.exe'],
                          'Linux': []}[current_platform]
            for asset in latest_release['assets']:
                if fileending == pathlib.Path(asset['browser_download_url']).suffixes:
                    download_url = asset['browser_download_url']
        else:
            download_url = latest_release['zipball_url']
        return latest_release['tag_name'], latest_release['body'], latest_release['html_url'], download_url
    else:
        return None


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
