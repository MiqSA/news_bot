from RPA.Tables import Table
from src.operations.excel_handler import (
    delete_file,
    read_excel_as_table,
    write_data_to_excel
)


EXCEL_PATH = './output/test_news.xlsx'

def test_write_data_to_excel(excel_path = EXCEL_PATH):
    payload = [
        {
            'picture_filename': 'downloaded_image_1.png', 'title': 'Any word',
            'description': 'Stay informed here, any word',
            'date': '', 'count_phrases': 1, 'contain_money': False
        }
        ]
    write_data_to_excel(payload, excel_path)
    table = read_excel_as_table(excel_path)
    assert isinstance(table, Table)
    delete_file(excel_path)

def test_read_excel_as_table(excel_path = EXCEL_PATH):       
    payload = [
        {
            'picture_filename': 'downloaded_image_2.png', 'title': 'Something here',
            'description': 'Stay inform journalism.',
            'date': 'July 30, 2024', 'count_phrases': 0, 'contain_money': False
        }
        ]
    write_data_to_excel(payload, excel_path)
    table = read_excel_as_table(excel_path)
    assert isinstance(table, Table)
    delete_file(excel_path)
