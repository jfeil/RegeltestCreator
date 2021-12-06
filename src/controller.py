from .database import db
from .main_application import MainWindow


def populate_tabwidget(mainwindow: MainWindow):
    mainwindow.create_ruletabs(db.get_rulegroups())


def populate_questions(mainwindow: MainWindow):
    for rulegroup in db.get_rulegroups():
        mainwindow.insert_question(rulegroup, db.get_questions(rulegroup))
