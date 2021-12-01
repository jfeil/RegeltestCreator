import sys
import sys

from bs4 import BeautifulSoup

from src.database import db
from src.datatypes import create_rulegroups, create_questions_and_mchoice


def read_in(file_name):
    with open(file_name, 'r+') as file:
        soup = BeautifulSoup(file, "lxml")
    rulegroups = create_rulegroups(soup.find("gruppen"))
    questions, mchoice = create_questions_and_mchoice(soup("regelsatz"))
    return rulegroups, questions, mchoice


if __name__ == '__main__':
    args = sys.argv
    if not db:
        datasets = read_in(args[1])
        for dataset in datasets:
            db.fill_database(dataset)
