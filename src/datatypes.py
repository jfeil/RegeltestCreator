import logging
import re
import uuid
from collections import namedtuple
from datetime import datetime, date
from enum import Enum, auto, IntEnum
from typing import List, Tuple, Dict

import bs4
from sqlalchemy import Column, Integer, String, ForeignKey, Date, BLOB, DateTime, Boolean
from sqlalchemy.orm import relationship

from src.basic_config import Base, EagerDefault

default_date = datetime(1970, 1, 1)


class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Integer)
    y = Column(Integer)
    width = Column(Integer)


class RegeltestDesign(Base):
    __tablename__ = 'regeltest_design'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    icon_position_id = Column(Integer, ForeignKey('position.id'))
    icon_position = relationship("Position", foreign_keys=[icon_position_id],
                                 single_parent=True, cascade="all, delete-orphan", uselist=False)

    title_position_id = Column(Integer, ForeignKey('position.id'))
    title_position = relationship("Position", foreign_keys=[title_position_id],
                                  single_parent=True, cascade="all, delete-orphan", uselist=False)
    title_fontsize = Column(Integer)

    description_position_id = Column(Integer, ForeignKey('position.id'))
    description_position = relationship("Position", foreign_keys=[description_position_id],
                                        single_parent=True, cascade="all, delete-orphan", uselist=False)
    description_fontsize = Column(Integer)

    namefield_position_id = Column(Integer, ForeignKey('position.id'))
    namefield_position = relationship("Position", foreign_keys=[namefield_position_id],
                                      single_parent=True, cascade="all, delete-orphan", uselist=False)
    namefield_fontsize = Column(Integer)

    question_fontsize = Column(Integer)
    question_points_fontsize = Column(Integer)

    regeltests = relationship("Regeltest", back_populates="design")


class RegeltestQuestion(Base):
    __tablename__ = 'regeltest_question'
    id = Column(Integer, primary_key=True, autoincrement=True)

    regeltest_id = Column(String, ForeignKey('regeltest.id'))
    regeltest = relationship("Regeltest", back_populates="selected_questions")
    question_id = Column(Integer, ForeignKey('question.signature'))
    question = relationship("Question", back_populates="regeltest_questions")

    available_points = Column(Integer)
    is_multiple_choice = Column(Boolean)


class RegeltestIcon(Base):
    __tablename__ = 'regeltest_icon'
    id = Column(Integer, primary_key=True, autoincrement=True)
    icon = Column(BLOB, unique=True)
    regeltests = relationship("Regeltest", back_populates="icon")


class Regeltest(Base):
    __tablename__ = 'regeltest'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, default=(lambda: uuid.uuid4().hex))
    title = Column(String)
    description = Column(String)

    icon_id = Column(Integer, ForeignKey('regeltest_icon.id'))
    icon = relationship("RegeltestIcon", back_populates="regeltests")

    design_id = Column(Integer, ForeignKey('regeltest_design.id'))
    design = relationship("RegeltestDesign", back_populates="regeltests")

    selected_questions = relationship("RegeltestQuestion", back_populates='regeltest')

    created = Column(DateTime, default=datetime.now)


class Statistics(Base):
    __tablename__ = 'statistics'

    question_signature = Column(String, ForeignKey("question.signature"), primary_key=True)
    question = relationship("Question", back_populates="statistics")

    # more like consecutive_solved_count...
    continous_solved_count = Column(Integer, default=0)
    level = Column(Integer, default=0)
    correct_solved = Column(Integer, default=0)
    wrong_solved = Column(Integer, default=0)
    last_tested = Column(DateTime, default=None)


class QuestionGroup(Base):
    __tablename__ = 'question_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    children = relationship("Question", back_populates="question_group", cascade="all, delete-orphan")

    def export(self):
        return f"<GRUPPENNR>\n{self.id:02d}\n</GRUPPENNR>\n<GRUPPENTEXT>\n{self.name}\n</GRUPPENTEXT>\n"

    def __repr__(self):
        return f"QuestionGroup(id={self.id!r}, name={self.name!r})"


class MultipleChoice(Base):
    __tablename__ = 'multiple_choice'

    question_signature = Column(String, ForeignKey("question.signature"), primary_key=True)
    index = Column(Integer, primary_key=True)
    text = Column(String)

    question = relationship("Question", back_populates="multiple_choice")

    def export(self):
        return f"{'abc'[self.index]} ( ) {self.text}\n"

    def __repr__(self):
        return f"MultipleChoice(question_signature={self.question_signature!r}, index={self.index!r}, text={self.text!r})"


class SelfTestMode(IntEnum):
    level = 0
    random = 1
    prioritize_new = 2

    def __str__(self):
        if self == SelfTestMode.random:
            return "Zufällig"
        elif self == SelfTestMode.level:
            return "6-Level"
        elif self == SelfTestMode.prioritize_new:
            return "Seltener gefragte Fragen priorisieren"
        else:
            raise ValueError("Invalid Mode")


class FilterOption(Enum):
    smaller_equal = auto()
    smaller = auto()
    larger_equal = auto()
    larger = auto()
    equal = auto()
    contains = auto()

    def __str__(self):
        if self == FilterOption.smaller_equal:
            return 'kleiner/gleich als'
        elif self == FilterOption.smaller:
            return 'kleiner als'
        elif self == FilterOption.larger:
            return 'größer als'
        elif self == FilterOption.larger_equal:
            return 'größer/gleich als'
        elif self == FilterOption.equal:
            return 'gleich'
        elif self == FilterOption.contains:
            return 'beinhaltet'


class Question(Base):
    __tablename__ = 'question'

    QuestionValues = namedtuple('QuestionValues', ['table_value', 'table_tooltip', 'table_checkbox'],
                                defaults=[None, None])
    QuestionParameters = namedtuple('QuestionParameters', ['table_header', 'filter_options', 'datatype'])

    question_group = relationship("QuestionGroup", back_populates="children")
    multiple_choice = relationship("MultipleChoice", back_populates="question", cascade="all, delete-orphan")
    regeltest_questions = relationship("RegeltestQuestion", back_populates="question")
    statistics = relationship("Statistics", back_populates="question", cascade="all, delete-orphan", uselist=False)

    group_id = Column(Integer, ForeignKey('question_group.id'))
    question_id = Column(Integer, default=-1)
    question = Column(String)
    answer_index = Column(Integer, default=EagerDefault(-1))  # for no multiple choice
    answer_text = Column(String)
    created = Column(Date, default=date.today)
    last_edited = Column(Date, default=date.today)
    signature = Column(String, default=(lambda: uuid.uuid4().hex), primary_key=True)

    parameters = {
        'group_id': QuestionParameters(table_header="Fragengruppe", filter_options=None, datatype=int),
        'question_id': QuestionParameters(table_header="Regelnummer", filter_options=(FilterOption.equal,),
                                          datatype=int),
        'question': QuestionParameters(table_header="Frage",
                                       filter_options=(FilterOption.contains, FilterOption.equal), datatype=str),
        'multiple_choice': QuestionParameters(table_header="Multiple choice", filter_options=(FilterOption.equal,),
                                              datatype=bool),
        'answer_index': QuestionParameters(table_header="Multiple choice Antwort",
                                           filter_options=(FilterOption.equal,), datatype=int),
        'answer_text': QuestionParameters(table_header="Antwort",
                                          filter_options=(FilterOption.contains, FilterOption.equal), datatype=str),
        'created': QuestionParameters(table_header="Erstelldatum",
                                      filter_options=(FilterOption.smaller_equal, FilterOption.smaller,
                                                      FilterOption.larger, FilterOption.larger_equal),
                                      datatype=date),
        'last_edited': QuestionParameters(table_header="Änderungsdatum",
                                          filter_options=(FilterOption.smaller_equal, FilterOption.smaller,
                                                          FilterOption.larger, FilterOption.larger_equal),
                                          datatype=date),
        'signature': QuestionParameters(table_header="Signatur",
                                        filter_options=(FilterOption.contains, FilterOption.equal), datatype=str),
        'last_tested': QuestionParameters(table_header="Zuletzt getestet",
                                          filter_options=(FilterOption.smaller_equal, FilterOption.smaller,
                                                          FilterOption.larger, FilterOption.larger_equal),
                                          datatype=datetime),
        'positive_tests': QuestionParameters(table_header="Korrekt beantwortet",
                                             filter_options=(FilterOption.smaller_equal, FilterOption.smaller,
                                                             FilterOption.larger, FilterOption.larger_equal),
                                             datatype=int),
        'negative_tests': QuestionParameters(table_header="Inkorrekt beantwortet",
                                             filter_options=(FilterOption.smaller_equal, FilterOption.smaller,
                                                             FilterOption.larger, FilterOption.larger_equal),
                                             datatype=int),
        'streak': QuestionParameters(table_header="In Folge korrekt beantwortet",
                                     filter_options=(FilterOption.smaller_equal, FilterOption.smaller,
                                                     FilterOption.larger, FilterOption.larger_equal),
                                     datatype=int),

        'regeltest_count': QuestionParameters(table_header="Regeltestverwendungen",
                                              filter_options=(FilterOption.smaller_equal, FilterOption.smaller,
                                                              FilterOption.larger, FilterOption.larger_equal,
                                                              FilterOption.equal), datatype=int),
    }  # type: Dict[str, QuestionParameters]

    # noinspection PyArgumentList
    def values(self, key) -> QuestionValues:
        return {
            'group_id': Question.QuestionValues(table_value=self.group_id),
            'question_id': Question.QuestionValues(table_value=self.question_id),
            'question': Question.QuestionValues(table_value=self.question, table_tooltip=self.question),
            'multiple_choice': Question.QuestionValues(
                table_value={-1: None, 0: 'A', 1: 'B', 2: 'C'}[self.answer_index],
                table_tooltip=None,
                table_checkbox=2 * (self.answer_index != -1)),
            'answer_index': Question.QuestionValues(table_value=self.answer_index),
            'answer_text': Question.QuestionValues(table_value=self.answer_text, table_tooltip=self.answer_text),
            'created': Question.QuestionValues(table_value=self.created),
            'last_edited': Question.QuestionValues(table_value=self.last_edited),
            'signature': Question.QuestionValues(table_value=self.signature),
            'last_tested': Question.QuestionValues(table_value=self._statistics('last_tested')),
            'positive_tests': Question.QuestionValues(table_value=self._statistics('positive_tests')),
            'negative_tests': Question.QuestionValues(table_value=self._statistics('negative_tests')),
            'streak': Question.QuestionValues(table_value=self._statistics('streak')),
            'regeltest_count': Question.QuestionValues(table_value=len(self.regeltest_questions))
        }[key]

    def _statistics(self, key):
        if not self.statistics:
            if key == 'last_tested':
                return None
            else:
                return 0
        if key == 'last_tested':
            return self.statistics.last_tested
        elif key == 'positive_tests':
            return self.statistics.correct_solved
        elif key == 'negative_tests':
            return self.statistics.wrong_solved
        elif key == 'streak':
            return self.statistics.continous_solved_count

    def export(self) -> Tuple[str, str]:
        if self.answer_index != -1:
            answer_text = f"({'abc'[self.answer_index]})  {self.answer_text}"
        else:
            answer_text = self.answer_text
        return (f"<REGELSATZ>\n<LNR>\n{self.group_id:02d}{self.question_id:03d}\n</LNR>\n<FRAGE>\n{self.question}\n"
                f"</FRAGE>\n<MCHOICE>\n",
                f"</MCHOICE>\n<ANTWORT>\n{answer_text}\n</ANTWORT>\n<ERST>\n{self.created.strftime('%d.%m.%Y')}\n"
                f"</ERST>\n<AEND>\n "
                f"{self.last_edited.strftime('%d.%m.%Y')}\n</AEND>\n<SIGNATUR>\n{self.signature}\n</SIGNATUR>\n"
                f"</REGELSATZ>\n")

    def __repr__(self):
        return f"Question(text={self.question!r}, answer={self.answer_index!r}:{self.answer_text!r}" \
               f", question_id={self.group_id!r} {self.question_id!r})"


def create_question_groups(groups: bs4.element.Tag) -> List[QuestionGroup]:
    texts = groups.find_all("GRUPPENTEXT")
    texts = [item.contents[0].strip() for item in texts]
    numbers = groups.find_all("GRUPPENNR")
    numbers = [int(item.contents[0]) for item in numbers]

    return [QuestionGroup(id=number, name=text) for text, number in zip(texts, numbers)]


def create_questions_and_mchoice(rules_xml):
    def create_mchoice(mchoice_):
        if not mchoice_:
            # empty -> no mchoice question
            return []
        mchoice_cleaned = mchoice_.strip().split("\n")
        if len(mchoice_cleaned) == 1 and len(mchoice_cleaned[0]) <= 1:
            # bullshit input..
            return []

        assert len(
            mchoice_cleaned) == 3, f"More than three possible answers?! Wtf.. '{mchoice_}' v. '{mchoice_cleaned}'"
        # removes the a/b/c () in front :)
        return [re.sub(r"^[abc] *\( *\) *", "", i) for i in mchoice_cleaned]

    rules_index = []
    signatures = []
    rules = []
    multiple_choice = []
    for rule in rules_xml:
        lnr = rule.find("LNR").contents[0].strip()
        group_id = int(lnr[0:2])
        question_id = int(lnr[2:])
        signature = rule.find("SIGNATUR").contents[0].strip()
        if (group_id, question_id) in rules_index:
            # duplicated questions... wtf
            continue
        else:
            rules_index += [(group_id, question_id)]
        if signature in signatures:
            # duplicate question... again
            continue
        else:
            signatures += [signature]
        question = rule.find("FRAGE").contents[0].strip()
        mchoice = create_mchoice(rule.find("MCHOICE").contents[0])
        mchoice = [MultipleChoice(question_signature=signature, index=i, text=mchoice) for i, mchoice in
                   enumerate(mchoice)]
        answer = rule.find("ANTWORT").contents[0].strip()
        if not mchoice:
            mchoice_index = -1
        else:
            if re.match(r" *\(*a\)* *", answer):
                mchoice_index = 0
            elif re.match(r" *\(*b\)* *", answer):
                mchoice_index = 1
            elif re.match(r" *\(*c\)* *", answer):
                mchoice_index = 2
            else:
                logging.info(f"{question} is multiple choice, but has no answer candidate.. choice is ignored")
                mchoice_index = -1
                mchoice = []
        multiple_choice += mchoice
        if mchoice_index >= 0:
            answer = re.sub(r"^ *\(*[abc] *\)* *", "", answer)
        created = rule.find("ERST").contents[0].strip()
        changed = rule.find("AEND").contents[0].strip()
        if created:
            created = datetime.strptime(rule.find("ERST").contents[0].strip(), "%d.%m.%Y")
        else:
            created = default_date
        if changed:
            changed = datetime.strptime(rule.find("AEND").contents[0].strip(), "%d.%m.%Y")
            if changed < created:
                changed = created
        else:
            changed = created
        rules += [Question(question_id=question_id, group_id=group_id, question=question, answer_index=mchoice_index,
                           answer_text=answer, created=created, last_edited=changed, signature=signature)]
    return rules, multiple_choice
