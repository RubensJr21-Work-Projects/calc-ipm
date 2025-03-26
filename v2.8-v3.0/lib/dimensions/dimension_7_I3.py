import pandas as pd


def I3(base_main: pd.DataFrame, base_familias: pd.DataFrame) -> pd.DataFrame:
    b_familias = base_familias.copy()

    b_familias["Test1"] = (
        b_familias["opt_Energia"]
        .fillna('')
        .isin(["G", "V", "O"])
    )

    b_familias["Test2"] = (
        (
            b_familias["opt_Energia"]
            .fillna('')
            .isin(["M", "C", "S"])
        )
        &
        (
            b_familias["opt_EnergiaRede"]
            .fillna('')
            .isin(["H", "O"])
        )
    )
    
    b_familias["Test3"] = (
       (
        b_familias["opt_EnergiaCozinha"]
        .fillna('')
        .isin(["G", "B", "E"])
    )
        &
        (
        b_familias["opt_EnergiaEscassez"]
        .fillna('')
        .isin(["S", "A"])
    )
    )

    b_familias["Test4"] = (
        b_familias["opt_EnergiaCozinha"]
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

    return pd.merge(base_main, b_familias[["_uuid", "DIM_I3"]], on="_uuid", how="left")