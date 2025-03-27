from typing import TypedDict

import pandas as pd
from dateutil.relativedelta import relativedelta
from lib.core import ValidFileExcel
from lib.rename_sheet_configs import Sheet_Configs_Type


class FinalDataFrameGroup(TypedDict):
    Base_Familias: pd.DataFrame
    Base_Membros: pd.DataFrame
    Main: pd.DataFrame
    base_filename: str
    file: str

def generate_main(base_familias: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    """
    Cria o DataFrame para a planilha 'Main' com base em BASE_Familias e BASE_Membros.
    
    :param base_familias: DataFrame da planilha BASE_Familias.
    :param base_membros: DataFrame da planilha BASE_Membros.
    :return: DataFrame consolidado para a planilha 'Main'.
    """
    # Seleção e renomeação de colunas principais
    
    main_data = base_familias[["_id", "_submitted_by", "2 - Data da entrevista", "1 - Id da Família"]].copy()
    main_data.rename(
        columns={
            "_submitted_by": "Analista aplicador",
            "2 - Data da entrevista": "Data de Aplicação",
            "1 - Id da Família": "ID",
        },
        inplace=True,
    )

    # Para adicionar uma nova coluna, basta criar df["nome da nova coluna"] = 0 (valor inicial ou já passando uma lista com os valores desejados)
    # Para remover uma coluna, basta inserir del df["coluna a ser removida"]
    # Para excluir uma linha, basta fazer o seguinte: df2 = df.drop([4]) (sendo que 4 é o índice da linha que deseja que seja excluída) 
    # Para exclir várias linhas, basta fazer a mesma coisa com uma linha, porém passando as outras linhas também: df2 = df.drop([4,5,6,7])
    #   Para não precisar criar 2 DataFrames podemos passar o parâmetro inplace=True: df.drop([4,5,6,7], inplace=True). O resultado será que as linhas serão removidades no próprio DataFrame
    #   Necessário verificar quais métodos podem ter esse parâmetro
    # Para retornar linhas de 1 a 5: df[1:5]
    # Para fazer fatiamento com rótulos: 
    #   - é necessário dar rótulos para os dados
    #   - é como dar nomes para as linhas
    #   dicionario = {
    #       'País': ["Brasil", "Uruguai", "Canadá"],
    #       'Ano': [1958, 1930, 1966]
    #       'Titulos': [5, 2, 1]
    #   }
    #   
    #   df = pd.DataFrame(dicionario, index=["a","b","c"])
    #   # Mostra df completo
    #   print(df, '\n')
    #   # Mostra apenas linhas de índices a até b
    #   print(df['a':'b'])
    # 
    # Para realizar indexação com método .loc(), retornando linhas e colunas específicas apenas por meio dos seus rótulos
    #   # Linha b, colunas de País e Ano
    #   print(df.loc['b', ['País', 'Ano']])
    #   # Linhas de a a b, coluna de ano
    #   print(df.loc([: 'd', 'Ano']))
    # 

    # Exemplos de cálculos para novas colunas
    # Total de membros na família
    if "_id" in base_membros.columns:
        family_member_count = base_membros.groupby("_id").size()
        main_data["Total de Membros"] = main_data["_id"].map(family_member_count).fillna(0).astype(int)

    # Calcula idade dos membros
    base_membros["Idade"] = base_membros.apply(
        lambda row: relativedelta(row["2 - Data da entrevista"], row["M2 - Data de nascimento"]).years,
        axis=1
    ).astype(int)

    return main_data

def create_main_from_excel_files_with_columns_valids(excel_files_with_columns_valids: list[ValidFileExcel], sheet_configs: Sheet_Configs_Type) -> list[FinalDataFrameGroup]:
    def process_by_file(excel_file: ValidFileExcel, configs: Sheet_Configs_Type) -> FinalDataFrameGroup:
        # Adiciona coluna com a Data de Aplicação do formulário
        excel_file["Base_Membros"] = pd.merge(excel_file["Base_Membros"], excel_file["Base_Familias"][["_id", "2 - Data da entrevista"]], on="_id", how="left")
        return {
            "Base_Familias": excel_file["Base_Familias"],
            "Base_Membros": excel_file["Base_Membros"],
            "Main": generate_main(excel_file["Base_Familias"], excel_file["Base_Membros"]),
            "base_filename": excel_file["base_filename"],
            "file": excel_file["file"]
        }
    # end def process_by_file
    consolidatedData: list[FinalDataFrameGroup] = []
    for excel_file in excel_files_with_columns_valids:
        consolidatedData.append(process_by_file(excel_file, sheet_configs))
    return consolidatedData
# end def create_main_from_excel_files_with_columns_valids