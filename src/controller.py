from typing import List

from .database import db
from .datatypes import Question, MultipleChoice
from .main_application import MainWindow


def clear_database():
    db.clear_database()


def populate_tabwidget(mainwindow: MainWindow):
    mainwindow.create_ruletabs(db.get_rulegroups())


def populate_questions(mainwindow: MainWindow):
    mainwindow.initialize_questions()


def update_question_set(question: Question, mchoice: List[MultipleChoice]):
    db.update_question_set(question, mchoice)


def get_question(signature: str):
    return db.get_question_by_primarykey(signature)


def get_rulegroup(rulegroup_index: int):
    return db.get_rulegroup_by_primarykey(rulegroup_index)


def get_questions_by_foreignkey(rulegroup_index: int):
    return db.get_questions_by_foreignkey(rulegroup_index)


def get_multiplechoice_by_foreignkey(question_signature: str):
    return db.get_multiplechoice_by_foreignkey(question_signature)


def fill_database(dataset):
    db.fill_database(dataset)
