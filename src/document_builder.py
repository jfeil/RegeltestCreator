import os.path
import random
from typing import List, Tuple

from PIL import Image
from borb.io.read.types import Decimal
from borb.pdf import Document, Page, PageLayout, SingleColumnLayout, PDF, FixedColumnWidthTable, Paragraph, TableCell, \
    TextField, TextArea

from src.datatypes import Question, MultipleChoice

# PAGE_HEIGHT = defaultPageSize[1]
# PAGE_WIDTH = defaultPageSize[0]
linespacing = 14
min_lines = 3
space_between = 0.2 * linespacing
space_bottom = 0.4 * linespacing
radio_size = 20
ratio_answer = 9 / 10
base_image_size = 70

points_height = 3 * linespacing


def answer_letter(index):
    return "abc"[index]


def create_question(index: int, question: Question, solution: bool, shuffle_mchoice: bool,
                    font_name: str, font_size: int) -> FixedColumnWidthTable:
    def shuffle_mchoice_fun(mchoice, answer_index) -> Tuple[List[MultipleChoice], int]:
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

    is_mchoice = len(question.multiple_choice) != 0
    if not solution and len(question.multiple_choice) != 0:
        row_count = len(question.multiple_choice) + 1
    else:
        row_count = 2
    question_table = FixedColumnWidthTable(number_of_columns=4, number_of_rows=row_count,
                                           column_widths=[Decimal(10), Decimal(80), Decimal(5), Decimal(5)])
    question_table = question_table.add(
        TableCell(Paragraph(f"{index}. {question.question}"), col_span=2)
    )

    if is_mchoice and shuffle_mchoice:
        mchoice, mchoice_index = shuffle_mchoice_fun(question.multiple_choice, question.answer_index)
    else:
        mchoice = question.multiple_choice
        mchoice_index = question.answer_index

    if solution:
        question_table = question_table.add(
            TableCell(Paragraph(f"2"), row_span=row_count)
        ).add(
            TableCell(Paragraph(f"/2"), row_span=row_count)
        )
        question_table = question_table.add(
            TableCell(Paragraph(question.answer_text if not is_mchoice
                                else f"{answer_letter(mchoice_index)}) {mchoice[mchoice_index].text}"),
                      row_span=row_count - 1,
                      col_span=2)
        )
    else:
        question_table = question_table.add(
            TableCell(TextArea(field_name=f"points_{index}"), row_span=row_count)
        ).add(
            TableCell(Paragraph(f"/2"), row_span=row_count)
        )
        if is_mchoice:
            pass
        else:
            question_table = question_table.add(
                TextField(field_name=f"answer_{index}")
            )
    return question_table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))


def create_document(questions: List[Question], filename, title, icon: Image = None,
                    solution_suffix='_LOESUNG', shuffle_mchoice=True, font_name='Helvetica', font_size=9):
    def page_setup(canvas, doc):
        canvas.saveState()
        canvas.setFont(font_name, font_size)
        canvas.restoreState()

    doc_question: Document = Document()
    page_question: Page = Page()
    doc_question.add_page(page_question)
    layout_question: PageLayout = SingleColumnLayout(page_question)

    doc_solution: Document = Document()
    page_solution: Page = Page()
    doc_solution.add_page(page_solution)
    layout_solution: PageLayout = SingleColumnLayout(page_solution)

    # story_solution = [TitleFlowable(title, icon, username="Muster Lösung", max_points=len(questions) * 2)]
    # story_question = [TitleFlowable(title, icon, max_points=len(questions) * 2)]

    for i, question in enumerate(questions):
        random_state = random.getstate()
        layout_question.add(create_question(i + 1, question, solution=False, shuffle_mchoice=shuffle_mchoice,
                                            font_name=font_name, font_size=font_size))
        # story_question.append(question_flow)
        # story_question.append(Spacer(1, 0.1 * inch))
        random.setstate(random_state)
        layout_solution.add(create_question(i + 1, question, solution=True, shuffle_mchoice=shuffle_mchoice,
                                            font_name=font_name, font_size=font_size))
        # story_solution.append(question_flow)
        # story_solution.append(Spacer(1, 0.1 * inch))

    with open(filename, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc_question)

    solution_path = os.path.splitext(filename)
    solution_path = solution_path[0] + solution_suffix + solution_path[1]

    with open(solution_path, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc_solution)
