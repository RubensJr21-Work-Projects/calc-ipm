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
            "_submission__id": "_id"
        },
        "Base_Familias": {}
    }

    sheet_configs: Sheet_Configs_Type = {
        "BASE_Familias": {
            "columns": ["1 - Id da Família","2 - Data da entrevista","17.1 - Está a menos de 30m de caminhada, ida e volta?","18 - Qual é a forma de iluminação utilizada no seu domicílio?","19 - Com que frequência a energia elétrica, proveniente de rede geral, está habitualmente disponível para este domicílio?","20 - Como são preparadas as refeições?*","20.1 - A família é obrigada a utilizar outros combustíveis para preparar as refeições durante o mês por falta de dinheiro?","21 - Existe banheiro de uso exclusivo, com chuveiro e vaso sanitário, neste domicílio, inclusive os localizados no terreno?*","22 - De que forma é feito o escoamento do banheiro ou sanitário?","27.1 - Data da última atualização do CadÚnico","28 - Total recebido do Bolsa Família","29 - Total recebido do programa de transferência de renda estadual","30 - Total recebido de programa de transferência de renda municipal","31 - Todas as gestantes estão tendo acompanhamento pré-natal?","32 - Nos últimos 3 meses os alimentos acabaram antes que os moradores deste domicílio tivessem dinheiro para comprar mais comida?","33 - Nos últimos 3 meses houve preocupação de que os alimentos acabassem antes de poder comprar ou receber mais comida?","34 - Nos últimos 3 meses, ficaram sem dinheiro para ter uma alimentação saudável e variada?","35 - Nos últimos 3 meses, comeram apenas alguns poucos tipos de alimentos que ainda tinham, porque o dinheiro acabou?","36 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, deixou de fazer alguma refeição?","37 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, comeu menos do que achou que devia?","38 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, sentiu fome, mas não comeu?","39 - Nos últimos 3 meses, algum adulto da família, fez apenas uma refeição ao dia ou ficou um dia inteiro sem comer?","40 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, deixou de ter uma alimentação saudável e variada?","41 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, alguma vez, não comeu quantidade suficiente de comida?","42 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, foi diminuída a quantidade de alimentos das refeições?","43 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, deixou de fazer alguma refeição?","44 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, sentiu fome, mas não comeu?","45 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, fez apenas uma refeição ao dia ou ficou sem comer por um dia inteiro?","_submitted_by","_id"],  # Colunas para manter
            "order": ["_id","1 - Id da Família","_submitted_by","2 - Data da entrevista","17.1 - Está a menos de 30m de caminhada, ida e volta?","18 - Qual é a forma de iluminação utilizada no seu domicílio?","19 - Com que frequência a energia elétrica, proveniente de rede geral, está habitualmente disponível para este domicílio?","20 - Como são preparadas as refeições?*","20.1 - A família é obrigada a utilizar outros combustíveis para preparar as refeições durante o mês por falta de dinheiro?","21 - Existe banheiro de uso exclusivo, com chuveiro e vaso sanitário, neste domicílio, inclusive os localizados no terreno?*","22 - De que forma é feito o escoamento do banheiro ou sanitário?","27.1 - Data da última atualização do CadÚnico","28 - Total recebido do Bolsa Família","29 - Total recebido do programa de transferência de renda estadual","30 - Total recebido de programa de transferência de renda municipal","31 - Todas as gestantes estão tendo acompanhamento pré-natal?","32 - Nos últimos 3 meses os alimentos acabaram antes que os moradores deste domicílio tivessem dinheiro para comprar mais comida?","33 - Nos últimos 3 meses houve preocupação de que os alimentos acabassem antes de poder comprar ou receber mais comida?","34 - Nos últimos 3 meses, ficaram sem dinheiro para ter uma alimentação saudável e variada?","35 - Nos últimos 3 meses, comeram apenas alguns poucos tipos de alimentos que ainda tinham, porque o dinheiro acabou?","36 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, deixou de fazer alguma refeição?","37 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, comeu menos do que achou que devia?","38 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, sentiu fome, mas não comeu?","39 - Nos últimos 3 meses, algum adulto da família, fez apenas uma refeição ao dia ou ficou um dia inteiro sem comer?","40 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, deixou de ter uma alimentação saudável e variada?","41 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, alguma vez, não comeu quantidade suficiente de comida?","42 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, foi diminuída a quantidade de alimentos das refeições?","43 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, deixou de fazer alguma refeição?","44 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, sentiu fome, mas não comeu?","45 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, fez apenas uma refeição ao dia ou ficou sem comer por um dia inteiro?"]    # Ordem desejada
        },
        "BASE_Membros": {
            "columns": ["M0 - ID do Morador","M1 - Nome","M2 - Data de nascimento","M3 - Responsável pela família?","M4 - Cor ou raça","M6 - Tem acesso à internet?","M11 - Recebeu todas as vacinas do Calendário Nacional de Vacinação do Sistema Único de Saúde?","M12 - Tem alguma das doenças abaixo?","M12.1 - Se sim, está em acompanhamento médico (rede privada ou SUS)?","M13 - O morador tem alguma deficiência e/ou transtorno que limite as suas atividades habituais (como trabalhar, ir à escola, brincar, etc.) ?","M13.4 - Em função dessa deficiência e/ou transtorno precisa de alguma tecnologia assistiva (cadeira de rodas, muleta, prótese, pranchas de comunicação, ou outro recurso ou aparelho) para realizar suas atividades cotidianas?","M15 - Está estudando?","M16 - Frequenta regularmente a escola? (exclusiva para MENOR de 18 anos)","M17 - Está em risco de exclusão escolar? (exclusiva para MENOR de 18 anos)","M18 - Está matriculado na escola? (exclusiva para MENOR de 18 anos)","M19 - Qual foi o curso mais elevado que frequentou, no qual concluiu pelo menos uma série/ano?","M19.1 - E qual foi a última série que foi aprovado?","M20 - Quanto recebe, normalmente, por mês de aposentadoria, aposentadoria rural, pensão ou BPC/LOAS","M21 - Quanto recebe, normalmente, por mês de pensão alimentícia","M23 - Quanto recebe, normalmente, por mês de outras fontes de remuneração exceto bolsa família ou similares (inclui aluguel social)","M25 - Quanto recebe, normalmente, por mês como remuneração de trabalho?","_submission__id"],  # Colunas para manter
            "order": ["_submission__id","M0 - ID do Morador","M1 - Nome","M2 - Data de nascimento","M3 - Responsável pela família?","M4 - Cor ou raça","M6 - Tem acesso à internet?","M11 - Recebeu todas as vacinas do Calendário Nacional de Vacinação do Sistema Único de Saúde?","M12 - Tem alguma das doenças abaixo?","M12.1 - Se sim, está em acompanhamento médico (rede privada ou SUS)?","M13 - O morador tem alguma deficiência e/ou transtorno que limite as suas atividades habituais (como trabalhar, ir à escola, brincar, etc.) ?","M13.4 - Em função dessa deficiência e/ou transtorno precisa de alguma tecnologia assistiva (cadeira de rodas, muleta, prótese, pranchas de comunicação, ou outro recurso ou aparelho) para realizar suas atividades cotidianas?","M15 - Está estudando?","M16 - Frequenta regularmente a escola? (exclusiva para MENOR de 18 anos)","M17 - Está em risco de exclusão escolar? (exclusiva para MENOR de 18 anos)","M18 - Está matriculado na escola? (exclusiva para MENOR de 18 anos)","M19 - Qual foi o curso mais elevado que frequentou, no qual concluiu pelo menos uma série/ano?","M19.1 - E qual foi a última série que foi aprovado?","M20 - Quanto recebe, normalmente, por mês de aposentadoria, aposentadoria rural, pensão ou BPC/LOAS","M21 - Quanto recebe, normalmente, por mês de pensão alimentícia","M23 - Quanto recebe, normalmente, por mês de outras fontes de remuneração exceto bolsa família ou similares (inclui aluguel social)","M25 - Quanto recebe, normalmente, por mês como remuneração de trabalho?"]    # Ordem desejada
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
        print(main_data)

        print("Vou calulcar DIM_R1")
        main_data = R1(main_data, base_familia)
        print(main_data)
        print("DIM_R1 Calculada")

        print("Vou calulcar DIM_R2")
        main_data = R2(main_data, base_familia, base_membros)
        print(main_data)
        print("DIM_R2 Calculada")

        print("Vou calulcar DIM_E1")        
        main_data = E1(main_data, base_familia, base_membros)
        print(main_data)
        print("DIM_E1 Calculada")

        print("Vou calulcar DIM_E2")        
        main_data = E2(main_data, base_membros)
        print(main_data)
        print("DIM_E2 Calculada")        

        print("Vou calulcar DIM_I1")        
        main_data = I1(main_data, base_familia)
        print(main_data)
        print("DIM_I1 Calculada")        


        print("Vou calulcar DIM_I2")
        main_data = I2(main_data, base_familia)
        print(main_data)
        print("DIM_I2 Calculada")

        print("Vou calulcar DIM_I3")
        main_data = I3(main_data, base_familia)
        print(main_data)
        print("DIM_I3 Calculada")

        print("Vou calulcar DIM_I4")
        main_data = I4(main_data, base_membros)
        print(main_data)
        print("DIM_I4 Calculada")

        print("Vou calulcar DIM_S1")
        main_data = S1(main_data, base_familia, base_membros)
        print(main_data)
        print("DIM_S1 Calculada")

        print("Vou calulcar DIM_N1")
        main_data = N1(main_data, base_familia, base_membros)
        print(main_data)
        print("DIM_N1 Calculada")


        main_data = IPM_TOTAL(main_data)

        main_data = CLEAN_MAIN(main_data)

        base_familia.rename(columns={"_id": "ID Aplicação do Formulário"}, inplace=True)
        base_membros.rename(columns={"_id": "ID Aplicação do Formulário"}, inplace=True)
        main_data.rename(columns={"_id": "ID Aplicação do Formulário"}, inplace=True)

        final_data["Main"] = main_data

    # TODO: Trocar nome da coluna que identifica o a aplicação do formulário 
    save_final_files_to_csv(project_folder, finals_data)

    # Fim do processamento
    return 0

if __name__ == "__main__":
    main()