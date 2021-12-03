from typing import List

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


class QuestionFlowable(Flowable):
    canv: Canvas

    def __init__(self, question_index: int, question: Question, mchoice: List[MultipleChoice], fontName='Helvetica',
                 fontSize=9, solution: bool = False, x=0, y=0, width=4 / 5 * PAGE_WIDTH):
        super().__init__()

        def answer_letter(index):
            return "abc"[index]

        self.question_index = question_index
        self.question = question
        self.mchoice = mchoice
        self.solution = solution

        self.paragraph_style = ParagraphStyle('DefaultStyle', fontName=fontName, fontSize=fontSize)

        self.x = x
        self.y = y
        self.width = width

        self.question_text = f"{self.question_index}. {self.question.question}"

        if self.question.answer_index == -1:
            self.answer_text = self.question.answer_text
        else:
            answer_letter = answer_letter(self.question.answer_index)
            self.answer_text = f"{answer_letter}) {self.question.answer_text}"

        lines_question = len(simpleSplit(self.question_text, fontName, fontSize, self.width))
        self.lines_answer = len(simpleSplit(self.answer_text, fontName, fontSize, 9 / 10 * self.width))

        logging.debug(question_index, lines_question, self.lines_answer)

        self.height_answer = max(self.lines_answer, min_lines) * linespacing
        self.height_question = lines_question * linespacing
        self.height = self.height_answer + space_between + self.height_question + space_bottom

    def draw(self):
        question = Paragraph(self.question_text, self.paragraph_style)
        question.wrapOn(self.canv, self.width, self.height)
        question.drawOn(self.canv, self.x, space_between + self.height_answer + space_bottom)

        if self.solution:
            solution = Paragraph(self.answer_text, self.paragraph_style)
            solution.wrapOn(self.canv, 9 / 10 * self.width, self.height)
            solution.drawOn(self.canv, self.x + 4 * mm,
                            self.y + space_bottom + max(min_lines - self.lines_answer, 0) * linespacing)
        elif not self.solution and self.question.answer_index != -1:
            radio_group = f"Question_{self.question_index}"
            radio_size = 20
            radio_1 = self.canv.acroForm.radio("test1", relative=True, size=radio_size, name=radio_group, x=self.x,
                                               y=self.y + space_bottom + max(min_lines - self.lines_answer,
                                                                             0) * linespacing)
            solution = Paragraph("Radio button 1", self.paragraph_style)
            solution.wrapOn(self.canv, 9 / 10 * self.width, self.height)
            solution.drawOn(self.canv, self.x + 4 * mm,
                            self.y + space_bottom + max(min_lines - self.lines_answer, 0) * linespacing)

            radio_2 = self.canv.acroForm.radio("test2", relative=True, size=radio_size, name=radio_group, x=self.x,
                                               y=self.y + space_bottom + max(min_lines - self.lines_answer,
                                                                             0) * linespacing + radio_size)
            solution = Paragraph("Radio button 2", self.paragraph_style)
            solution.wrapOn(self.canv, 9 / 10 * self.width, self.height)
            solution.drawOn(self.canv, self.x + 4 * mm,
                            self.y + radio_size + space_bottom + max(min_lines - self.lines_answer, 0) * linespacing)

        elif not self.solution and self.question.answer_index == -1:
            # FieldFlags are:
            # 1 << 1: required
            # 1 << 12: MultiLine
            self.canv.acroForm.textfieldRelative(x=self.x + 4 * mm, y=self.y + space_bottom, width=9 / 10 * self.width,
                                                 height=self.height_answer, fontName=self.paragraph_style.fontName,
                                                 fontSize=self.paragraph_style.fontSize, maxlen=None,
                                                 fieldFlags=(1 << 1) + (1 << 12))


def go():
    doc = SimpleDocTemplate("phello.pdf")
    Story = [Spacer(1, 2 * inch)]
