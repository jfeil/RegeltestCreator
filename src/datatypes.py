import logging
import re
import uuid
from datetime import datetime, date
from typing import List, Tuple

import bs4
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from .basic_config import Base, EagerDefault

default_date = datetime(1970, 1, 1)


class Rulegroup(Base):
    __tablename__ = 'rulegroup'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    children = relationship("Question", back_populates="rulegroup", cascade="all, delete-orphan")

    def export(self):
        return f"<GRUPPENNR>\n{self.id:02d}\n</GRUPPENNR>\n<GRUPPENTEXT>\n{self.name}\n</GRUPPENTEXT>\n"

    def __repr__(self):
        return f"Rulegroup(id={self.id!r}, name={self.name!r})"


class MultipleChoice(Base):
    __tablename__ = 'multiplechoice'

    rule_signature = Column(String, ForeignKey("question.signature"), primary_key=True)
    index = Column(Integer, primary_key=True)
    text = Column(String)

    rule = relationship("Question", back_populates="multiple_choice")

    def export(self):
        return f"{'abc'[self.index]} ( ) {self.text}\n"

    def __repr__(self):
        return f"MultipleChoice(rule_signature={self.rule_signature!r}, index={self.index!r}, text={self.text!r})"


"""
<REGELSATZ>
<LNR>
10010
</LNR>
<FRAGE>
Kann diese Antwort einen Sinn ergeben?
</FRAGE>
<MCHOICE>

</MCHOICE>
<ANTWORT>
Weil das ein Beispiel ist, kann hier nichts sinnvolles stehen!
</ANTWORT>
<ERST>
02.10.2003
</ERST>
<AEND>
29.01.2019
</AEND>
<SIGNATUR>
5342851d460a2c99b62255db60461ce6
</SIGNATUR>
</REGELSATZ>

ALTERNATIVE:

<MCHOICE>
a ( ) A, B, C.
b ( ) Hello World.
c ( ) Lorem Ipsum.
</MCHOICE>
<ANTWORT>
c)  Das kann nur Lorem Ipsum sein.
</ANTWORT>


"""


class Question(Base):
    # LNR[0:2] = group_id
    # LNR[2:-1] = rule_id
    __tablename__ = 'question'

    rulegroup = relationship("Rulegroup", back_populates="children")
    multiple_choice = relationship("MultipleChoice", back_populates="rule", cascade="all, delete-orphan")

    group_id = Column(Integer, ForeignKey('rulegroup.id'))
    rule_id = Column(Integer, server_default='SELECT MAX(1, MAX(rule_id)+1) FROM question')
    question = Column(String)
    answer_index = Column(Integer, default=EagerDefault(-1))  # for no multiple choice
    answer_text = Column(String)
    created = Column(Date, default=date.today())
    last_edited = Column(Date, default=date.today())
    signature = Column(String, default=uuid.uuid4().hex, primary_key=True)

    def export(self) -> Tuple[str, str]:
        if self.answer_index != -1:
            answer_text = f"({'abc'[self.answer_index]})  {self.answer_text}"
        else:
            answer_text = self.answer_text
        return (f"<REGELSATZ>\n<LNR>\n{self.group_id:02d}{self.rule_id:03d}\n</LNR>\n<FRAGE>\n{self.question}\n"
                f"</FRAGE>\n<MCHOICE>\n",
                f"</MCHOICE>\n<ANTWORT>\n{answer_text}\n</ANTWORT>\n<ERST>\n{self.created.strftime('%d.%m.%Y')}\n</ERST>\n<AEND>\n"
                f"{self.last_edited.strftime('%d.%m.%Y')}\n</AEND>\n<SIGNATUR>\n{self.signature}\n</SIGNATUR>\n</REGELSATZ>\n")

    def __repr__(self):
        return f"Question(text={self.question!r}, answer={self.answer_index!r}:{self.answer_text!r}" \
               f", rule_id={self.group_id!r} {self.rule_id!r})"


def create_rulegroups(groups: bs4.element.Tag) -> List[Rulegroup]:
    texts = groups.find_all("gruppentext")
    texts = [item.contents[0].strip() for item in texts]
    numbers = groups.find_all("gruppennr")
    numbers = [int(item.contents[0]) for item in numbers]

    return [Rulegroup(id=number, name=text) for text, number in zip(texts, numbers)]


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
        lnr = rule.find("lnr").contents[0].strip()
        group_id = int(lnr[0:2])
        rule_id = int(lnr[2:])
        signature = rule.find("signatur").contents[0].strip()
        if (group_id, rule_id) in rules_index:
            # duplicated questions... wtf
            continue
        else:
            rules_index += [(group_id, rule_id)]
        if signature in signatures:
            # duplicate question... again
            continue
        else:
            signatures += [signature]
        question = rule.find("frage").contents[0].strip()
        mchoice = create_mchoice(rule.find("mchoice").contents[0])
        mchoice = [MultipleChoice(rule_signature=signature, index=i, text=mchoice) for i, mchoice in enumerate(mchoice)]
        answer = rule.find("antwort").contents[0].strip()
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
        created = rule.find("erst").contents[0].strip()
        changed = rule.find("aend").contents[0].strip()
        if created:
            created = datetime.strptime(rule.find("erst").contents[0].strip(), "%d.%m.%Y")
        else:
            created = default_date
        if changed:
            changed = datetime.strptime(rule.find("aend").contents[0].strip(), "%d.%m.%Y")
        else:
            changed = created
        rules += [Question(rule_id=rule_id, group_id=group_id, question=question, answer_index=mchoice_index,
                           answer_text=answer, created=created, last_edited=changed, signature=signature)]
    return rules, multiple_choice
