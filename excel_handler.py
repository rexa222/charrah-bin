import tempfile
from os import close, unlink
from collections import defaultdict

import xlsxwriter
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from config import GENERAL_INFO_TITLES, MAIN_DATA_TITLE_ROW


def get_default_cell_format(workbook: xlsxwriter.Workbook) -> Format:
    cells_format = workbook.add_format()
    cells_format.set_align('center')
    cells_format.set_align('vcenter')

    return cells_format


def set_xlsx_print_format(worksheet: Worksheet):
    worksheet.set_landscape()
    worksheet.set_paper(9)
    worksheet.center_horizontally()
    worksheet.fit_to_pages(1, 1)
    worksheet.set_margins(0, 0, 0.5, 0)


def write_excel(general_info: list[str], main_data_rows: [list[list[str]]]) -> str:
    fd, path = tempfile.mkstemp(suffix='.xlsx')
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet('Report')
    worksheet.right_to_left()
    worksheet.set_default_row(23)

    cells_format = get_default_cell_format(workbook)

    column_length_dict: dict[int, int] = defaultdict(int)
    column_length_dict.update(
        {
            i: len(main_data_title)
            for i, main_data_title in enumerate(MAIN_DATA_TITLE_ROW)
        }
    )

    general_info_title_col = len(MAIN_DATA_TITLE_ROW) + 3
    general_info_col = general_info_title_col + 1

    column_length_dict[general_info_col] = max([len(info) for info in general_info])
    column_length_dict[general_info_title_col] = max([len(title) for title in GENERAL_INFO_TITLES])

    for i, main_data_title in enumerate(MAIN_DATA_TITLE_ROW):
        column_length_dict[i] = len(main_data_title)
    
    general_info_table = {
        'data': list(zip(GENERAL_INFO_TITLES, general_info)),
        'header_row': False,
        'first_column': True,
        'style': 'Table Style Medium 11'
    }
    worksheet.add_table(
        first_row=0,
        last_row=len(general_info) - 1,
        first_col=general_info_col,
        last_col=general_info_title_col,
        options=general_info_table
    )

    main_data_table = {
        'data': main_data_rows,
        'autofilter': False,
        'columns': [{'header': title} for title in MAIN_DATA_TITLE_ROW],
        'style': 'Table Style Medium 13'
    }
    worksheet.add_table(
        first_row=0,
        last_row=len(main_data_rows),
        first_col=0,
        last_col=len(MAIN_DATA_TITLE_ROW) - 1,
        options=main_data_table
    )

    for column_index, column_length in column_length_dict.items():
        worksheet.set_column(column_index, column_index, column_length + 1, cells_format)

    set_xlsx_print_format(worksheet)
    workbook.close()
    close(fd)
    
    return path


def remove_file(path: str) -> None:
    unlink(path)
