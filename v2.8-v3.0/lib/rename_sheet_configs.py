from typing import TypedDict


class Config_Rename_Columns(TypedDict):
    Base_Familias: dict[str, str]
    Base_Membros: dict[str, str]

class Sheet_Configs_Type_Field(TypedDict):
    columns: list[str]
    order: list[str]

class Sheet_Configs_Type(TypedDict):
    BASE_Familias: Sheet_Configs_Type_Field
    BASE_Membros: Sheet_Configs_Type_Field

def rename_sheet_configs(rename_config: Config_Rename_Columns, sheet_configs: Sheet_Configs_Type) -> Sheet_Configs_Type:
    def rename(sheet: Sheet_Configs_Type_Field, columns_name_from_to: dict[str, str]):    
        for old_name, new_name in columns_name_from_to.items():
            index_in_columns = sheet["columns"].index(old_name)
            index_in_order = sheet["order"].index(old_name)
            sheet["columns"][index_in_columns] = new_name
            sheet["order"][index_in_order] = new_name
    if "Base_Familias" in rename_config and "BASE_Familias" in sheet_configs:
        rename(sheet_configs["BASE_Familias"], rename_config["Base_Familias"])
    if "Base_Membros" in rename_config and "BASE_Membros" in sheet_configs:
        rename(sheet_configs["BASE_Membros"], rename_config["Base_Membros"])
    return sheet_configs