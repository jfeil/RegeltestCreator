import logging
import os
from typing import List, Union, Tuple

from appdirs import AppDirs
from sqlalchemy import create_engine, inspect, func, select
from sqlalchemy.orm import Session

from .basic_config import app_name, app_author, database_name, Base
from .datatypes import Rulegroup, Question, MultipleChoice


class DatabaseConnector:
    engine = None

    def __init__(self):
        dirs = AppDirs(appname=app_name, appauthor=app_author)
        database_path = os.path.join(dirs.user_data_dir, database_name)
        logging.debug(dirs.user_data_dir)
        self.initialized = True
        if not os.path.isdir(dirs.user_data_dir):
            os.makedirs(dirs.user_data_dir, )
            self.initialized = False
        elif not os.path.isfile(database_path):
            self.initialized = False
        self.engine = create_engine(f"sqlite+pysqlite:///{database_path}?check_same_thread=False", future=True)
        if not inspect(self.engine).has_table(Rulegroup.__tablename__) or \
                not inspect(self.engine).has_table(Question.__tablename__) or \
                not inspect(self.engine).has_table(MultipleChoice.__tablename__):
            self.clear_database()

        if not self.initialized:
            self._init_database()

        self.session = Session(self.engine)

    def _init_database(self):
        # Create database based on basis - need to read docu first lol
        Base.metadata.create_all(self.engine)

    def __bool__(self):
        # check if database is empty :)
        return self.initialized

    def abort(self):
        self.session.rollback()

    def close_connection(self):
        self.session.close()

    def clear_database(self):
        Base.metadata.drop_all(self.engine)
        self.initialized = False

    def get_rulegroups(self):
        rulegroups = self.session.query(Rulegroup)
        return rulegroups

    def add_rulegroup(self, rulegroup):
        self.session.add(rulegroup)
        self.session.commit()

    def get_question_multiplechoice(self):
        return_dict = []
        for question in self.session.query(Question):
            return_dict += [(question, self.session.query(MultipleChoice).where(MultipleChoice.rule == question).all())]
        return return_dict

    def update_question_set(self, question: Question):
        self.session.add(question)
        self.session.commit()
        signature = question.signature
        return signature

    def get_question(self, signature: str):
        question = self.session.query(Question).where(Question.signature == signature).first()
        return question

    def get_rulegroup(self, rulegroup_index: int):
        rulegroup = self.session.query(Rulegroup).where(Rulegroup.id == rulegroup_index).first()
        return rulegroup

    def get_questions_by_foreignkey(self, rulegroup_id: int, mchoice=None, randomize: bool = False):
        questions = self.session.query(Question).where(Question.group_id == rulegroup_id)
        if mchoice is not None:
            if mchoice:
                questions = questions.where(Question.answer_index != -1)
            else:
                questions = questions.where(Question.answer_index == -1)
        if randomize:
            questions = questions.order_by(func.random())
        return questions.all()

    def get_multiplechoice_by_foreignkey(self, question_signature: str):
        mchoice = self.session.query(MultipleChoice).where(MultipleChoice.rule_signature == question_signature).all()
        return mchoice

    def fill_database(self, dataset: List[Union[Rulegroup, Question, MultipleChoice]]):
        # insert processed values into db
        if not self.initialized:
            self._init_database()

        self.session.add_all(dataset)
        self.session.commit()

    def delete(self, item: Union[Rulegroup, Question]):
        self.session.delete(item)
        self.session.commit()

    def get_new_question_id(self, rulegroup_index: int):
        stmt = select(Question.rule_id).where(Question.group_id.like(rulegroup_index))
        return_val = max(self.session.execute(stmt))[0] + 1
        return return_val

    def get_new_rulegroup_id(self):
        stmt = select(Rulegroup.id)
        values = self.session.execute(stmt).fetchall()
        if values:
            return_val = max(values)[0] + 1
        else:
            return_val = 1
        return return_val

    def get_rulegroup_config(self) -> List[Tuple[Rulegroup, int, int]]:
        rulegroups = self.get_rulegroups()
        return [(rulegroup,
                 len(self.get_questions_by_foreignkey(rulegroup_id=rulegroup.id, mchoice=False)),
                 len(self.get_questions_by_foreignkey(rulegroup_id=rulegroup.id, mchoice=True))) for rulegroup in
                rulegroups]


db = DatabaseConnector()
