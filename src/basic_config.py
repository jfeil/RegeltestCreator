import json
import logging
import os
import pathlib
import platform
import sys
from typing import Any, Tuple, Optional

import requests
from appdirs import AppDirs
from packaging import version
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

from .__version__ import __version__

log_level = logging.WARN
current_platform = platform.system()
VERSION_INFO = Optional[Tuple[str, str, str, str]]

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    is_bundled = True
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
else:
    is_bundled = False
    base_path = os.path.curdir

display_name = "RegeltestCreator"
app_name = "RegeltestCreator"
app_author = "jfeil"
app_dirs = AppDirs(appname=app_name, appauthor=app_author)

app_version = __version__
if not is_bundled and "dev" not in __version__:
    app_version += "dev"
app_version = version.parse(app_version)

api_url = "https://api.github.com/repos/jfeil/RegeltestCreator/releases"
dev_release = "?per_page=1"
stable_release = "/latest"

database_name = "database.db"


class EagerDefault:
    def __init__(self, value: Any):
        self.value = value


def check_for_update() -> Tuple[VERSION_INFO, VERSION_INFO]:  # new_version, description, url, download_url
    def check(cur_version, release_info):
        if not release_info:
            return None
        if version.parse(release_info['tag_name']) <= cur_version:
            return None
        fileendings = {'Darwin': ['.app', '.zip'],
                       'Windows': ['.exe'],
                       'Linux': []}
        download_urls = {}
        for asset in release_info['assets']:
            if set(fileendings['Darwin']) <= set(pathlib.Path(asset['browser_download_url']).suffixes):
                download_urls['Darwin'] = asset['browser_download_url']
            elif set(fileendings['Windows']) <= set(pathlib.Path(asset['browser_download_url']).suffixes):
                download_urls['Windows'] = asset['browser_download_url']
            else:
                download_urls['Linux'] = asset['browser_download_url']
        download_url = download_urls[current_platform]
        return release_info['tag_name'], release_info['body'], release_info['html_url'], download_url

    latest_dev_release = None
    latest_release = None
    try:
        latest_dev_release = json.loads(requests.get(api_url + dev_release).text)[0]
        latest_release = json.loads(requests.get(api_url + stable_release).text)
    except:
        pass
    return check(app_version, latest_release), check(app_version, latest_dev_release)


# Source: https://variable-scope.com/posts/setting-eager-defaults-for-sqlalchemy-orm-models
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
