import logging
import os
import sys
from typing import List, Union, Tuple

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from appdirs import AppDirs
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from src.basic_config import app_name, app_author, database_name, Base, is_bundled
from src.datatypes import QuestionGroup, Question, MultipleChoice


class DatabaseConnector:
    engine = None

    def __init__(self):
        self.dirs = AppDirs(appname=app_name, appauthor=app_author)
        database_path = os.path.join(self.dirs.user_data_dir, database_name)
        logging.debug(self.dirs.user_data_dir)
        self.initialized = True
        if not os.path.isdir(self.dirs.user_data_dir):
            os.makedirs(self.dirs.user_data_dir)
            self.initialized = False
        elif not os.path.isfile(database_path):
            self.initialized = False
        database_path = f"sqlite+pysqlite:///{database_path}"
        self.engine = create_engine(f"{database_path}?check_same_thread=False", future=True)
        if is_bundled:
            base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        else:
            base_path = os.path.curdir
        self.alembic_cfg = Config(os.path.join(base_path, 'alembic.ini'))
        self.alembic_cfg.set_main_option('sqlalchemy.url', database_path)
        self.alembic_cfg.set_main_option('script_location', os.path.join(base_path, 'alembic'))

        if not self.initialized:
            self.initialized = True
            self._init_database()

        self.session = Session(self.engine)
        with self.engine.connect() as conn:
            context = MigrationContext.configure(conn)
            current_rev = context.get_current_revision()
            if not current_rev:
                # no revision available -> created before migration was introduced
                command.stamp(self.alembic_cfg, "440180672239")
        command.upgrade(self.alembic_cfg, "head")

    def _init_database(self):
        # Create database based on basis and stamp with alembic for future migrations
        Base.metadata.create_all(self.engine)

        command.stamp(self.alembic_cfg, "head")

    def __bool__(self):
        # check if database is empty :)
        return self.initialized

    def abort(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def close_connection(self):
        self.session.close()

    def clear_database(self):
        Base.metadata.drop_all(self.engine)
        self.initialized = False

    def get_rulegroups(self):
        rulegroups = self.session.query(QuestionGroup).all()
        return rulegroups

    def add_rulegroup(self, rulegroup):
        self.session.add(rulegroup)
        self.session.commit()

    def get_question_multiplechoice(self):
        return_dict = []
        for question in self.session.query(Question):
            return_dict += [
                (question, self.session.query(MultipleChoice).where(MultipleChoice.question == question).all())]
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
        rulegroup = self.session.query(QuestionGroup).where(QuestionGroup.id == rulegroup_index).first()
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
        mchoice = self.session.query(MultipleChoice).where(
            MultipleChoice.question_signature == question_signature).all()
        return mchoice

    def fill_database(self, dataset: List[Union[QuestionGroup, Question, MultipleChoice]]):
        # insert processed values into db
        if not self.initialized:
            self._init_database()

        self.session.add_all(dataset)
        self.session.commit()

    def delete(self, item: Union[QuestionGroup, Question]):
        self.session.delete(item)
        self.session.commit()

    def get_new_question_id(self, rulegroup_index: int):
        stmt = select(Question.question_id).where(Question.group_id.like(rulegroup_index))
        return_val = max(self.session.execute(stmt))[0] + 1
        return return_val

    def get_new_rulegroup_id(self):
        stmt = select(QuestionGroup.id)
        values = self.session.execute(stmt).fetchall()
        if values:
            return_val = max(values)[0] + 1
        else:
            return_val = 1
        return return_val

    def get_rulegroup_config(self) -> List[Tuple[QuestionGroup, int, int]]:
        rulegroups = self.get_rulegroups()
        return [(rulegroup,
                 len(self.get_questions_by_foreignkey(rulegroup_id=rulegroup.id, mchoice=False)),
                 len(self.get_questions_by_foreignkey(rulegroup_id=rulegroup.id, mchoice=True))) for rulegroup in
                rulegroups]


db = DatabaseConnector()
