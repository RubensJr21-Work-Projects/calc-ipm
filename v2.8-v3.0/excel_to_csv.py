import os

from lib.clean_main import CLEAN_MAIN
from lib.columns import rename_columns, reorder_columns
from lib.core import ValidFileExcel
from lib.dimensions import E1, E2, I1, I2, I3, I4, N1, R1, R2, S1
from lib.file_and_folder_functions import (check_excel_files,
                                           get_dfs_from_valid_struct_files,
                                           get_files_from_project_folder,
                                           save_final_files_to_csv)
from lib.ipm_total import IPM_TOTAL
from lib.main_functions import (
    FinalDataFrameGroup, create_main_from_excel_files_with_columns_valids)
from lib.rename_sheet_configs import (Config_Rename_Columns,
                                      Sheet_Configs_Type, rename_sheet_configs)


def main():
    # pre-processamento

    # Caminho da pasta do projeto
    project_folder = os.path.dirname(os.path.abspath(__file__))

    input_folder = os.path.join(project_folder, "input")
    output_folder = os.path.join(project_folder, "output")
    
    # Cria a pasta de saída, se não existir
    os.makedirs(output_folder, exist_ok=True)

    files = get_files_from_project_folder(input_folder)

    if len(files) <= 0:
        print(f"Pasta de input {input_folder} está vazia")
        return 0

    rename_config: Config_Rename_Columns = {
        "Base_Membros": {
            "_submission__uuid": "_uuid"
        },
        "Base_Familias": {}
    }

    sheet_configs: Sheet_Configs_Type = {
        "BASE_Familias": {
            "columns": ["Txt_IdFamlia","Dt_Coleta","bool_Agua30min","opt_Energia","opt_EnergiaRede","opt_EnergiaCozinha","opt_EnergiaEscassez","bool_Banheiro","opt_Escoamento","dt_CadUnico","integer_PBF","integer_Estadual","integer_Municipal","opt_gestantes","opt_Ebia1","opt_Ebia2","opt_Ebia3","opt_Ebia4","opt_Ebia5","opt_Ebia6","opt_Ebia7","opt_Ebia8","opt_Ebia9","opt_Ebia10","opt_Ebia11","opt_Ebia12","opt_Ebia13","opt_Ebia14","username","_uuid"],  # Colunas para manter
            "order": ["_uuid","Txt_IdFamlia","username","Dt_Coleta","bool_Agua30min","opt_Energia","opt_EnergiaRede","opt_EnergiaCozinha","opt_EnergiaEscassez","bool_Banheiro","opt_Escoamento","dt_CadUnico","integer_PBF","integer_Estadual","integer_Municipal","opt_gestantes","opt_Ebia1","opt_Ebia2","opt_Ebia3","opt_Ebia4","opt_Ebia5","opt_Ebia6","opt_Ebia7","opt_Ebia8","opt_Ebia9","opt_Ebia10","opt_Ebia11","opt_Ebia12","opt_Ebia13","opt_Ebia14"]    # Ordem desejada
        },
        "BASE_Membros": {
            "columns": ["Txt_IdMorador","txt_Nome","dt_Nascimento","bool_Responsavel","opt_Raca","bool_internet","bool_vacinas","opt_doencas","bool_acomp_SUS","opt_Deficiencias","opt_tec_assistiva","bool_Esta_estudando","bool_Frequenta_escola","bool_exclusao_escolar","bool_Matriculado_escola","opt_educacao","opt_educacao_Grad","integer_Aposentadoria_BPC_LOAS","integer_pensao_alimenticia","integer_Outras_Fontes","integer_Remuneracao_mes_passad","_submission__uuid"],  # Colunas para manter
            "order": ["_submission__uuid","Txt_IdMorador","txt_Nome","dt_Nascimento","bool_Responsavel","opt_Raca","bool_internet","bool_vacinas","opt_doencas","bool_acomp_SUS","opt_Deficiencias","opt_tec_assistiva","bool_Esta_estudando","bool_Frequenta_escola","bool_exclusao_escolar","bool_Matriculado_escola","opt_educacao","opt_educacao_Grad","integer_Aposentadoria_BPC_LOAS","integer_pensao_alimenticia","integer_Outras_Fontes","integer_Remuneracao_mes_passad"]    # Ordem desejada
        }
    }

    # obter arquivos válidos
    # irá receber uma lista de arquivos da pasta do projeto
    excel_files = get_dfs_from_valid_struct_files(files, input_folder, sheet_configs)

    if len(excel_files) <= 0:
        print(f"Não foi possível obter os DataFrames, pois as configurações de todos os arquivos excel eram inválidos")
        return 0

    excel_files_reordered_columns = reorder_columns(excel_files, sheet_configs)
    
    excel_files_renamed_columns = rename_columns(excel_files_reordered_columns, rename_config)
    
    sheet_configs = rename_sheet_configs(rename_config, sheet_configs)

    # Fim do pré-processamento

    # Inicio do processamento

    excel_files_with_columns_valids: list[ValidFileExcel] = check_excel_files(excel_files_renamed_columns, sheet_configs)

    finals_data: list[FinalDataFrameGroup] = create_main_from_excel_files_with_columns_valids(excel_files_with_columns_valids, sheet_configs)

    # Converter todos os DataFrames para CSV 
    # excel_to_csv(project_folder)

    for final_data in finals_data:
        base_familia = final_data["Base_Familias"]
        base_membros = final_data["Base_Membros"]
        main_data = final_data["Main"]
        
        main_data = R1(main_data, base_familia)

        main_data = R2(main_data, base_familia, base_membros)

        main_data = E1(main_data, base_familia, base_membros)
        
        main_data = E2(main_data, base_membros)

        main_data = I1(main_data, base_familia)

        main_data = I2(main_data, base_familia)

        main_data = I3(main_data, base_familia)

        main_data = I4(main_data, base_membros)

        main_data = S1(main_data, base_familia, base_membros)

        main_data = N1(main_data, base_familia, base_membros)

        main_data = IPM_TOTAL(main_data)

        main_data = CLEAN_MAIN(main_data)
        # print(main_data)

        base_familia.rename(columns={"_uuid": "ID Aplicação do Formulário"}, inplace=True)
        base_membros.rename(columns={"_uuid": "ID Aplicação do Formulário"}, inplace=True)
        main_data.rename(columns={"_uuid": "ID Aplicação do Formulário"}, inplace=True)

        final_data["Main"] = main_data
    
    save_final_files_to_csv(project_folder, finals_data)

    # Fim do processamento
    return 0

if __name__ == "__main__":
    main()