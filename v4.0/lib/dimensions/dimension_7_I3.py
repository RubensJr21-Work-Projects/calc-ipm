import pandas as pd


def I3(base_main: pd.DataFrame, base_familias: pd.DataFrame) -> pd.DataFrame:
    b_familias = base_familias.copy()

    b_familias["Test1"] = (
        b_familias["18 - Qual é a forma de iluminação utilizada no seu domicílio?"]
        .fillna('')
        .isin(["G", "V", "O"])
    )

    b_familias["Test2"] = (
        (
            b_familias["18 - Qual é a forma de iluminação utilizada no seu domicílio?"]
            .fillna('')
            .isin(["M", "C", "S"])
        )
        &
        (
            b_familias["19 - Com que frequência a energia elétrica, proveniente de rede geral, está habitualmente disponível para este domicílio?"]
            .fillna('')
            .isin(["H", "O"])
        )
    )
    
    b_familias["Test3"] = (
       (
        b_familias["20 - Como são preparadas as refeições?*"]
        .fillna('')
        .isin(["G", "B", "E"])
    )
        &
        (
        b_familias["20.1 - A família é obrigada a utilizar outros combustíveis para preparar as refeições durante o mês por falta de dinheiro?"]
        .fillna('')
        .isin(["S", "A"])
    )
    )

    b_familias["Test4"] = (
        b_familias["20 - Como são preparadas as refeições?*"]
        .fillna('')
        .isin(["X", "O"])
    )

    b_familias["DIM_I3_Comp"] = (
        b_familias["Test1"]
        |
        b_familias["Test2"]
        |
        b_familias["Test3"]
        |
        b_familias["Test4"]
    )

    b_familias["DIM_I3"] = b_familias["DIM_I3_Comp"].apply(lambda x: 0.05 if x else 0)

    return pd.merge(base_main, b_familias[["_id", "DIM_I3"]], on="_id", how="left")