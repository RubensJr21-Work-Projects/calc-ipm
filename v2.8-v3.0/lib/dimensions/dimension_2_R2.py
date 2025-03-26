import pandas as pd


def R2(base_main: pd.DataFrame, base_familias: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    # somar colunas da base de membros para obter o total da renda pelos membros
    b_membros = base_membros.copy()
    b_familias = base_familias.copy()
    
    b_membros["STM"] = b_membros[[
        "integer_Aposentadoria_BPC_LOAS",
        "integer_pensao_alimenticia",
        "integer_Outras_Fontes",
        "integer_Remuneracao_mes_passad"
    ]].sum(axis=1)

    df_agrupado_membros = b_membros.groupby('_uuid', as_index=False)['STM'].sum()

    # Fazendo o JOIN com base no '_uuid'
    df_calculado = pd.merge(base_main, df_agrupado_membros, on='_uuid', how='left') # LEFT JOIN para manter todos os ids do df_destino

    # Substituindo NaN por 0 (caso existam IDs sem correspondência)
    df_calculado['STM'] = df_calculado['STM'].fillna(0)

    # print(df_calculado)

    b_familias["STF"] = b_familias[[
        "integer_PBF",
        "integer_Estadual",
        "integer_Municipal"
    ]].sum(axis=1)

    df_agrupado_familias = b_familias.groupby('_uuid', as_index=False)['STF'].sum()

    # Fazendo o JOIN com base no '_uuid'
    df_calculado = pd.merge(df_calculado, df_agrupado_familias, on='_uuid', how='left') # LEFT JOIN para manter todos os ids do df_destino

    # Substituindo NaN por 0 (caso existam IDs sem correspondência)
    df_calculado['STF'] = df_calculado['STF'].fillna(0)

    def calcular_percapta(row):
        return (row['STM']+row['STF'])/row["Total de Membros"]

    df_calculado['DIM_R2'] = df_calculado.apply(lambda row: 0.1 if calcular_percapta(row) < 670.60 else 0, axis=1)
    
    return pd.merge(base_main, df_calculado[["_uuid", "DIM_R2"]], on="_uuid", how="left")