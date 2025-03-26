import pandas as pd


def N1(base_main: pd.DataFrame, base_familias: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    b_familias = base_familias.copy()
    b_membros = base_membros.copy()

    # perguntas EBIAs

    questionsEBIAs = [
        "opt_Ebia1",
        "opt_Ebia2",
        "opt_Ebia3",
        "opt_Ebia4",
        "opt_Ebia5",
        "opt_Ebia6",
        "opt_Ebia7",
        "opt_Ebia8",
        "opt_Ebia9",
        "opt_Ebia10",
        "opt_Ebia11",
        "opt_Ebia12",
        "opt_Ebia13",
        "opt_Ebia14",
    ]

    # Contando quantos valores são 'S' em cada linha
    b_familias['Soma_EBIA'] = b_familias[questionsEBIAs].apply(lambda x: (x == 'S').sum(), axis=1) # Estava N

    b_membros["0 <= Idade < 18"] = b_membros["Idade"].between(0-1, 18, inclusive="neither")

    # Agrupando por Id_familia e verificando se pelo menos um membro atende à condição
    df_resultado = b_membros.groupby('_uuid')['0 <= Idade < 18'].any().reset_index()

    # Renomeando a coluna final
    df_resultado.rename(columns={'0 <= Idade < 18': 'TemCriançaAdolescente'}, inplace=True)

    # Fazendo o JOIN com base no '_uuid'
    b_familias = pd.merge(b_familias, df_resultado, on='_uuid', how='left')


    b_familias["Test1"] = (
        (b_familias["TemCriançaAdolescente"] == True)
        &
        (b_familias["Soma_EBIA"] > 5)
    )
    b_familias["Test2"] = (
        (b_familias["TemCriançaAdolescente"] == False)
        &
        (b_familias["Soma_EBIA"] > 3)
    )

    b_familias["Test1 or Test2"] = b_familias["Test1"] | b_familias["Test2"]

    b_familias["DIM_N1"] = b_familias.apply(lambda row: 0.2 if row["Test1 or Test2"] else 0, axis=1)

    return pd.merge(base_main, b_familias[["_uuid", "DIM_N1"]], on="_uuid", how="left")