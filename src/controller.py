from typing import List, Tuple

from sqlalchemy import func

from .database import db
from .datatypes import Question, MultipleChoice, Rulegroup
from .main_application import MainWindow


def clear_database():
    db.clear_database()


def get_all_rulegroups():
    return db.get_rulegroups()


def get_all_questions():
    return db.get_question_multiplechoice()


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


def get_questions_by_foreignkey(rulegroup_index: int, mchoice: bool = None, randomize: bool = False):
    question_query = db.get_questions_by_foreignkey(rulegroup_index, mchoice, randomize)
    return question_query


def get_multiplechoice_by_foreignkey(question_signature: str):
    return db.get_multiplechoice_by_foreignkey(question_signature)


def get_rulegroup_config() -> List[Tuple[Rulegroup, int, int]]:
    rulegroups = db.get_rulegroups()
    return [(rulegroup,
             db.get_questions_by_foreignkey(rulegroup_id=rulegroup.id, mchoice=False).count(),
             db.get_questions_by_foreignkey(rulegroup_id=rulegroup.id, mchoice=True).count()) for rulegroup in rulegroups]


def fill_database(dataset):
    db.fill_database(dataset)
