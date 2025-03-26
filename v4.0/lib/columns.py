from lib.core import ValidFileExcel
from lib.rename_sheet_configs import Config_Rename_Columns, Sheet_Configs_Type


def rename_columns(excel_files: list[ValidFileExcel], rename_config: Config_Rename_Columns) -> list[ValidFileExcel]:    
    for excel_file in excel_files:
        if "Base_Familias" in rename_config:
            excel_file["Base_Familias"].rename(columns=rename_config["Base_Familias"], inplace=True)
        if "Base_Membros" in rename_config:
            excel_file["Base_Membros"].rename(columns=rename_config["Base_Membros"], inplace=True)
    return excel_files

def reorder_columns(excel_files: list[ValidFileExcel], sheet_configs: Sheet_Configs_Type) -> list[ValidFileExcel]:
    def reorder_by_file(file: ValidFileExcel, configs: Sheet_Configs_Type):
        column_order_BF = configs["BASE_Familias"]["order"]
        column_order_BM = configs["BASE_Membros"]["order"]

        file["Base_Familias"] = file["Base_Familias"].reindex(columns=column_order_BF)
        file["Base_Membros"] = file["Base_Membros"].reindex(columns=column_order_BM)
    for excel_file in excel_files:
        reorder_by_file(excel_file, sheet_configs)
    return excel_files
    # end for excel_file in excel_files
# end def reorder_columns

def check_columns_excel_file(excel_file: ValidFileExcel, sheet_configs: Sheet_Configs_Type) -> bool:
    def check_columns(sheet_name: str) -> bool:
        if sheet_name in sheet_configs:
            base_familias = sheet_configs[sheet_name]
            columns = base_familias["columns"]

            df = excel_file[sheet_name]

            # Verifica colunas ausentes
            missing_columns = [col for col in columns if col not in df.columns]

            if missing_columns:
                # https://stackoverflow.com/a/24065533
                raise ValueError(f"{excel_file['file']} ({sheet_name}): {', '.join(missing_columns)} estão faltando")
            else:
                return True
        return False
    # end def check_columns

    return check_columns("Base_Familias") and check_columns("Base_Membros")
# end def check_columns_excel_file