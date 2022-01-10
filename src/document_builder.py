import os.path
import random
from typing import List, Tuple

from PIL import Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable, SimpleDocTemplate, Spacer, Paragraph
from reportlab.rl_config import defaultPageSize

from src.datatypes import Question, MultipleChoice

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
linespacing = 14
min_lines = 3
space_between = 0.2 * linespacing
space_bottom = 0.4 * linespacing
radio_size = 20
ratio_answer = 9 / 10
base_image_size = 70

points_height = 3 * linespacing


class QuestionFlowable(Flowable):
    canv: Canvas

    def __init__(self, question_index: int, question: Question, mchoice: List[MultipleChoice], fontName='Helvetica',
                 fontSize=9, solution: bool = False, shuffle_mchoice=True, display_points=True, x=0, y=0,
                 width=4 / 5 * PAGE_WIDTH):
        super().__init__()

        def shuffle_mchoice_fun(mchoice, answer_index):
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
            mchoice, self.answer_index = shuffle_mchoice_fun(mchoice, self.answer_index)

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

        self.height_question = lines_question * linespacing
        self.height = sum(self.height_answer) + space_between + self.height_question + space_bottom

    def draw(self):
        question = Paragraph(self.question_text, self.paragraph_style)
        question.wrapOn(self.canv, self.width - 10, self.height)
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


class TitleFlowable(Flowable):
    canv: Canvas

    def __init__(self, title_line, title_icon, username="", fontName='Helvetica', image_scalefactor=1, titleSize=14,
                 nameSize=10, x=0, y=0, width=4 / 5 * PAGE_WIDTH, max_points=30):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = 100
        self.paragraph_style = ParagraphStyle('DefaultStyle', fontName=fontName, fontSize=nameSize, alignment=0)
        self.title_style = ParagraphStyle('DefaultStyle', fontName=fontName, fontSize=titleSize, alignment=1)
        self.title_icon = title_icon
        self.title_line = title_line
        self.max_points = max_points
        self.username = username
        if title_icon:
            self.image_size = Image.open(title_icon).size
            image_size = Image.open(title_icon).size
            ratio = image_size[0] / image_size[1]
            self.image_size = (image_scalefactor * base_image_size * ratio, image_scalefactor * base_image_size / ratio)

    def draw(self):
        if self.title_icon:
            self.canv.drawImage(self.title_icon, self.x, 30, width=self.image_size[0], height=self.image_size[1],
                                mask='auto')
        question = Paragraph(self.title_line, self.title_style)
        question.wrapOn(self.canv, 2 / 3 * self.width, self.height)
        question.drawOn(self.canv, self.x + 1 / 6 * self.width, 60)

        question = Paragraph("Name:", self.paragraph_style)
        question.wrapOn(self.canv, 2 / 10 * self.width, self.height)
        question.drawOn(self.canv, 6 / 10 * self.width - 10, 20)

        x_username = 6 / 10 * self.width + 30
        y_username = 20
        height_username = linespacing
        width_username = 2 / 10 * self.width
        if self.username != "":
            question = Paragraph(self.username, self.paragraph_style)
            question.wrapOn(self.canv, width_username, height_username)
            question.drawOn(self.canv, x_username, y_username)
        else:
            self.canv.acroForm.textfieldRelative(x=x_username, y=y_username, height=height_username,
                                                 width=width_username, value=self.username,
                                                 fontName=self.paragraph_style.fontName,
                                                 fontSize=self.paragraph_style.fontSize)
        self.canv.acroForm.textfieldRelative(x=6 / 10 * self.width + 40 + 2 / 10 * self.width, y=20, height=linespacing,
                                             width=1 / 15 * self.width, value=f"/{self.max_points}",
                                             fontName=self.paragraph_style.fontName,
                                             fontSize=self.paragraph_style.fontSize)


def create_document(question_set: List[Tuple[Question, List[MultipleChoice]]], filename, title, icon_path=None,
                    solution_suffix='_LOESUNG', shuffle_mchoice=True, font_name='Helvetica', font_size=9):
    def page_setup(canvas, doc):
        canvas.saveState()
        canvas.setFont(font_name, font_size)
        canvas.restoreState()

    doc_question = SimpleDocTemplate(filename)

    solution_path = os.path.splitext(filename)
    solution_path = solution_path[0] + solution_suffix + solution_path[1]

    doc_solution = SimpleDocTemplate(solution_path)

    story_solution = [TitleFlowable(title, icon_path, username="Muster Lösung", max_points=len(question_set) * 2)]
    story_question = [TitleFlowable(title, icon_path, max_points=len(question_set) * 2)]

    for i, (question, mchoice) in enumerate(question_set):
        random_state = random.getstate()
        question_flow = QuestionFlowable(i + 1, question, mchoice, font_name, font_size, solution=False,
                                         shuffle_mchoice=shuffle_mchoice, width=doc_question.width)
        story_question.append(question_flow)
        story_question.append(Spacer(1, 0.1 * inch))
        random.setstate(random_state)
        question_flow = QuestionFlowable(i + 1, question, mchoice, font_name, font_size, solution=True,
                                         shuffle_mchoice=shuffle_mchoice, width=doc_solution.width)
        story_solution.append(question_flow)
        story_solution.append(Spacer(1, 0.1 * inch))

    doc_question.build(story_question, onFirstPage=page_setup, onLaterPages=page_setup)
    doc_solution.build(story_solution, onFirstPage=page_setup, onLaterPages=page_setup)
