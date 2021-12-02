from typing import List

from reportlab.lib.units import inch, mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable, SimpleDocTemplate, Spacer, Frame, Paragraph
from reportlab.lib.utils import simpleSplit
from reportlab.rl_config import defaultPageSize

from src.datatypes import Question, MultipleChoice

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]


class QuestionFlowable(Flowable):
    canv: Canvas

    def __init__(self, question_index: int, question: Question, mchoice: List[MultipleChoice], fontName, fontSize,
                 solution: bool = False, x=0, y=0, width=4 / 5 * PAGE_WIDTH, height=30 * mm):
        super().__init__()

        self.linespacing = 14

        self.question_index = question_index
        self.question = question
        self.mchoice = mchoice
        self.solution = solution
        self.x = x
        self.y = y
        self.width = width

        lines_question = simpleSplit(f"{self.question_index}. {self.question.question}", fontName, fontSize + 1,
                                     0.93 * self.width)
        lines_answer = simpleSplit(self.question.answer_text, fontName, fontSize, 0.83 * 9 / 10 * self.width)

        print(len(lines_answer))

        self.height_answer = max(len(lines_answer), 2) * self.linespacing
        self.height_question = len(lines_question) * self.linespacing
        self.height = self.height_answer + 0.2 * self.linespacing + self.height_question + 0.4 * self.linespacing

    def draw(self):
        question = Paragraph(f"{self.question_index}. {self.question.question}")
        question.wrapOn(self.canv, self.width, self.height)
        question.drawOn(self.canv, self.x, 0.2 * self.linespacing + self.height_answer + 0.4 * self.linespacing)

        if self.solution:
            solution = Paragraph(f"{self.question.answer_text}")
            solution.wrapOn(self.canv, 9 / 10 * self.width, self.height)
            solution.drawOn(self.canv, self.x + 4 * mm, self.y + 0.3 * self.linespacing)
        else:
            self.canv.acroForm.textfieldRelative(x=self.x + 4 * mm, y=self.y + 0.3 * self.linespacing,
                                                 width=9 / 10 * self.width, height=self.height_answer)


def go():
    doc = SimpleDocTemplate("phello.pdf")
    Story = [Spacer(1, 2 * inch)]