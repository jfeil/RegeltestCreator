import logging
import re
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple

import bs4


@dataclass
class Rulegroup:
    text: str
    number: int


@dataclass
class MultipleChoice:
    pass


"""
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


@dataclass
class Rule:
    # LNR[0:2] = group_id
    # LNR[2:-1] = rule_id
    group_id: int
    rule_id: int
    question: str
    multiple_choice: List[MultipleChoice]
    answer: Tuple[int, str]  # in case of multiple choice, this designates the correct answer
    created: datetime
    last_edited: datetime
    signature: str


def create_rulegroups(groups: bs4.element.Tag) -> List[Rulegroup]:
    texts = groups.find_all("gruppentext")
    texts = [item.contents[0].strip() for item in texts]
    numbers = groups.find_all("gruppennr")
    numbers = [int(item.contents[0]) for item in numbers]

    return [Rulegroup(text, number) for text, number in zip(texts, numbers)]


def create_mchoice(mchoice):
    if not mchoice:
        # empty -> no mchoice question
        return []
    mchoice_cleaned = mchoice.strip().split("\n")
    if len(mchoice_cleaned) == 1 and len(mchoice_cleaned[0]) <= 1:
        # bullshit input..
        return []

    assert len(mchoice_cleaned) == 3, f"More than three possible answers?! Wtf.. '{mchoice}' v. '{mchoice_cleaned}'"
    # removes the a/b/c () in front :)
    return [re.sub(r"^[abc] *\(.*\) *", "", i) for i in mchoice_cleaned]


def create_rules(rules_xml):
    rules = []
    for rule in rules_xml:
        lnr = rule.find("lnr").contents[0].strip()
        group_id = lnr[0:2]
        rule_id = lnr[2:-1]
        question = rule.find("frage").contents[0].strip()
        mchoice = create_mchoice(rule.find("mchoice").contents[0])
        answer = rule.find("antwort").contents[0].strip()
        if not mchoice:
            mchoice_index = 0
        else:
            if re.match(r"\(a\)", answer):
                mchoice_index = 1
            elif re.match(r"\(b\)", answer):
                mchoice_index = 2
            elif re.match(r"\(c\)", answer):
                mchoice_index = 3
            else:
                logging.warning(f"{question} is multiple choice, but has no answer candidate.. choice is ignored")
                mchoice_index = 0
                mchoice = []
        if mchoice_index > 0:
            answer = re.sub(r"^ *\([abc] *\) *", "", answer)
        created = rule.find("erst").contents[0].strip()
        changed = rule.find("aend").contents[0].strip()
        if created:
            created = datetime.strptime(rule.find("erst").contents[0].strip(), "%d.%m.%Y")
        if changed:
            changed = datetime.strptime(rule.find("aend").contents[0].strip(), "%d.%m.%Y")
        signature = rule.find("signatur").contents[0].strip()
        rules += [Rule(rule_id=rule_id, group_id=group_id, question=question, multiple_choice=mchoice,
                       answer=(mchoice_index, answer), created=created, last_edited=changed, signature=signature)]
    return rules
