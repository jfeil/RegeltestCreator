import os.path
import sqlite3
import sys
from typing import List

from bs4 import BeautifulSoup
from appdirs import AppDirs
from sqlalchemy import create_engine

from src.database import db
from src.datatypes import create_rulegroups, create_rules, Rulegroup, Rule


def read_in(file_name):
    with open(file_name, 'r+') as file:
        soup = BeautifulSoup(file, "lxml")
    rulegroups = create_rulegroups(soup.find("gruppen"))
    questions = create_rules(soup("regelsatz"))
    return rulegroups, questions


if __name__ == '__main__':
    args = sys.argv
    read_in(args[1])
    if not db:
        db.fill_database(None, None, None)

