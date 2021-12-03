from typing import List
import random

from reportlab.lib.units import inch, mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable, SimpleDocTemplate, Spacer, Frame, Paragraph
from reportlab.lib.utils import simpleSplit
from reportlab.rl_config import defaultPageSize

from src.datatypes import Question, MultipleChoice

PAGE_HEIGHT = defaultPageSize[1];
PAGE_WIDTH = defaultPageSize[0]
linespacing = 14
min_lines = 3
space_between = 0.2 * linespacing
space_bottom = 0.4 * linespacing
radio_size = 20
ratio_answer = 9 / 10

points_height = 3 * linespacing


class QuestionFlowable(Flowable):
    canv: Canvas

    def __init__(self, question_index: int, question: Question, mchoice: List[MultipleChoice], fontName='Helvetica',
                 fontSize=9, solution: bool = False, shuffle_mchoice=True, display_points=True, x=0, y=0,
                 width=4 / 5 * PAGE_WIDTH):
        super().__init__()

        def shuffle_mchoice(mchoice, answer_index):
            old_indices = [choice.index for choice in mchoice]
            new_indices = list(range(len(old_indices)))
            random.shuffle(new_indices)
            # pos in old list
            old_pos = old_indices.index(answer_index)
            new_answer_index = new_indices[old_pos]

            random_mchoice = []

            for i, choice in enumerate(mchoice):
                random_mchoice += [MultipleChoice(index=new_indices[i], text=choice.text)]

            return sorted(random_mchoice, key=lambda x: x.index), new_answer_index

        def answer_letter(index):
            return "abc"[index]

        self.question_index = question_index
        self.question = question
        self.answer_index = self.question.answer_index

        if shuffle_mchoice and self.answer_index != -1:
            mchoice, self.answer_index = shuffle_mchoice(mchoice, self.answer_index)

        self.mchoice = [f"{answer_letter(m.index)}) {m.text}" for m in mchoice]
        self.solution = solution

        self.paragraph_style = ParagraphStyle('DefaultStyle', fontName=fontName, fontSize=fontSize)

        self.x = x
        self.y = y
        self.width = width

        self.question_text = f"{self.question_index}. {self.question.question}"

        if self.answer_index == -1:
            self.answer_text = self.question.answer_text
        else:
            answer_letter = answer_letter(self.answer_index)
            self.answer_text = f"{answer_letter}) {self.question.answer_text}"

        lines_question = len(simpleSplit(self.question_text, fontName, fontSize, self.width))
        self.lines_answer = len(simpleSplit(self.answer_text, fontName, fontSize, ratio_answer * self.width))

        if self.answer_index == -1:
            self.height_answer = [max(self.lines_answer, min_lines) * linespacing]
        else:
            self.height_answer = [
                max(len(simpleSplit(a, fontName, fontSize, ratio_answer * self.width)) * linespacing, 1.1 * radio_size)
                for a in self.mchoice]

        logging.debug(question_index, lines_question, self.lines_answer)

        self.height_question = lines_question * linespacing
        self.height = sum(self.height_answer) + space_between + self.height_question + space_bottom

    def draw(self):
        question = Paragraph(self.question_text, self.paragraph_style)
        question.wrapOn(self.canv, self.width, self.height)
        question.drawOn(self.canv, self.x, space_between + sum(self.height_answer) + space_bottom)

        if self.solution:
            solution = Paragraph(self.answer_text, self.paragraph_style)
            solution.wrapOn(self.canv, ratio_answer * self.width, self.height)
            solution.drawOn(self.canv, self.x + 4 * mm,
                            self.y + space_bottom + max(min_lines - self.lines_answer, 0) * linespacing)
        elif not self.solution:
            if self.answer_index != -1:
                def create_radio(index, text, x, y, height):
                    radio_group = f"Question_{self.question_index}"
                    self.canv.acroForm.radio(f"radio{index}", relative=True, size=radio_size, name=radio_group, x=x,
                                             y=y - 0.75 * radio_size + 0.5 * height)
                    solution = Paragraph(text, self.paragraph_style)
                    solution.wrapOn(self.canv, ratio_answer * self.width, self.height)
                    solution.drawOn(self.canv, x + 1.25 * radio_size, y)

                height_sum = sum(self.height_answer) + space_bottom
                for index, (height, choice) in enumerate(zip(self.height_answer, self.mchoice)):
                    height_sum -= height
                    create_radio(index, choice, self.x, height_sum, height)

            #             radio_2 = self.canv.acroForm.radio("radio2", relative=True, size=radio_size, name=radio_group, x=self.x, y=self.y + space_bottom + max(min_lines - self.lines_answer, 0) * linespacing + radio_size)
            #             solution = Paragraph("Radio button 2", self.paragraph_style)
            #             solution.wrapOn(self.canv, ratio_answer*self.width, self.height)
            #             solution.drawOn(self.canv, self.x+4*mm, self.y + radio_size + space_bottom + max(min_lines - self.lines_answer, 0) * linespacing)

            #             radio_3 = self.canv.acroForm.radio("radio3", relative=True, size=radio_size, name=radio_group, x=self.x, y=self.y + space_bottom + max(min_lines - self.lines_answer, 0) * linespacing)
            #             solution = Paragraph("Radio button 1", self.paragraph_style)
            #             solution.wrapOn(self.canv, ratio_answer*self.width, self.height)
            #             solution.drawOn(self.canv, self.x+4*mm, self.y + space_bottom + max(min_lines - self.lines_answer, 0) * linespacing)

            else:
                # FieldFlags are:
                # 1 << 1: required
                # 1 << 12: MultiLine
                self.canv.acroForm.textfieldRelative(x=self.x + 4 * mm, y=self.y + space_bottom,
                                                     width=ratio_answer * self.width, height=sum(self.height_answer),
                                                     fontName=self.paragraph_style.fontName,
                                                     fontSize=self.paragraph_style.fontSize, maxlen=None,
                                                     fieldFlags=(1 << 1) + (1 << 12))
            self.canv.acroForm.textfieldRelative(x=self.width, y=self.height - points_height, height=points_height,
                                                 width=points_height, value="/2",
                                                 fontName=self.paragraph_style.fontName,
                                                 fontSize=self.paragraph_style.fontSize, maxlen=3)


def go():
    doc = SimpleDocTemplate("phello.pdf")
    Story = [Spacer(1, 2 * inch)]
