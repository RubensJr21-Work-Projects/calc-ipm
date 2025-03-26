import os

import pandas as pd

from lib.columns import check_columns_excel_file
from lib.core import ValidFileExcel
from lib.main_functions import FinalDataFrameGroup
from lib.rename_sheet_configs import Sheet_Configs_Type


def get_dfs_from_valid_struct_files(files: list[str], input_folder: str, sheet_configs: Sheet_Configs_Type) -> list[ValidFileExcel]:

    def validate_excel(input_path: str, base_filename: str, file: str, configs: Sheet_Configs_Type) -> ValidFileExcel:
        sheets = pd.read_excel(input_path, sheet_name=None)
        # Verifica se as planilhas necessárias estão presentes
        if "BASE_Familias" not in sheets or "BASE_Membros" not in sheets:
            raise ValueError(f"{file}: 'BASE_Familias' ou 'BASE_Membros' ausente.")
        else:
            fml_columns = configs["BASE_Familias"]["columns"]
            mbr_columns = configs["BASE_Membros"]["columns"]
            return {
                "Base_Familias": sheets["BASE_Familias"][fml_columns],
                "Base_Membros": sheets["BASE_Membros"][mbr_columns],
                "base_filename": base_filename,
                "file": file
            }

    valid_files: list[ValidFileExcel] = []
    
    for file in files:
        if file.endswith(('.xls', '.xlsx')):
            input_path = os.path.join(input_folder, file)
            base_filename = os.path.splitext(file)[0]
            
            try:
                sheets_file = validate_excel(input_path, base_filename, file, sheet_configs)
                valid_files.append(sheets_file)
            except ValueError as ve:
                print(repr(ve))
                continue

    return valid_files

def check_excel_files(excel_files: list[ValidFileExcel], sheet_configs: Sheet_Configs_Type) -> list[ValidFileExcel]:
    excel_files_with_columns_valids: list[ValidFileExcel] = []

    for excel_file in excel_files:
        try:
            check_columns_excel_file(excel_file, sheet_configs)
            excel_files_with_columns_valids.append(excel_file)
        except ValueError as ve:
            print(repr(ve))
            continue
    # end for excel_file in excel_files
    return excel_files_with_columns_valids
# end def check_excel_files

import os


def get_files_from_project_folder(input_folder: str) -> list[str]:
    return os.listdir(input_folder)

def save_final_files_to_csv(project_folder: str, final_files: list[FinalDataFrameGroup]):
    output_folder = os.path.join(project_folder, "output")
    for excel_file in final_files:
        base_filename = excel_file["base_filename"]
        for sheet_name in ["Base_Familias", "Base_Membros", "Main"]:
            output_csv_path: str = os.path.join(output_folder, f"{base_filename}_{sheet_name}.csv")
            # excel_file[sheet_name].to_csv(output_csv_path, index=False, sep=";", decimal=",", float_format = "%.2f")
            excel_file[sheet_name].to_csv(output_csv_path, index=False, sep=",", decimal=".", float_format = "%.2f")
            print(f"Arquivo Criado: {output_csv_path}")