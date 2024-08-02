from RPA.Excel.Files import Files
import os
from src.logger import Log


excel = Files()
log_f = Log().main(__name__)


def read_excel_as_table(excel_path):
    try:
        excel.open_workbook(excel_path)
        return excel.read_worksheet_as_table(header=True)
    finally:
        excel.close_workbook()


def write_data_to_excel(data, excel_path, sheet_name='Sheet1'):
    try:
        excel.open_workbook(excel_path)
        excel.append_rows_to_worksheet(data, sheet_name, header=True)
    except FileNotFoundError:
        excel.create_workbook(excel_path)
        excel.create_worksheet(name=sheet_name,content=data,header=True)
        log_f.info(f"New excel created! {excel_path}")  
    finally:
        excel.save_workbook()
        excel.close_workbook()

def delete_file(filename):
    try:
        file_path = os.path.join(filename)
        if os.path.isfile(file_path):
            os.remove(file_path)        
    except Exception as err:
        log_f.exception("Error while deleting file.", exc_info=err)