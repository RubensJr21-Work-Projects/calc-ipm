import pandas as pd


def I4(base_main: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    b_membros = base_membros.copy()

    # Criando a coluna booleana que verifica se o Valor é 'Não'
    b_membros['M6 - Tem acesso à internet? == Não'] = b_membros['M6 - Tem acesso à internet?'].fillna('').eq('Não')  # True se for 'Não', False caso contrário

    # Agrupando por Id_familia e verificando se todos os membros têm 'Não'
    df_resultado = b_membros.groupby('_id', as_index=False)['M6 - Tem acesso à internet? == Não'].all().reset_index()

    # Renomeando a coluna final
    df_resultado.rename(columns={'M6 - Tem acesso à internet? == Não': 'Todos_membros_N'}, inplace=True)

    df_resultado['DIM_I4'] = df_resultado['Todos_membros_N'].apply(lambda x: 0.05 if x else 0)

    return pd.merge(base_main, df_resultado[["_id", "DIM_I4"]], on="_id", how="left")