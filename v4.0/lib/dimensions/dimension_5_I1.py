import pandas as pd


def I1(base_main: pd.DataFrame, base_familias: pd.DataFrame) -> pd.DataFrame:
    b_familias = base_familias.copy()
    b_familias["DIM_I1"] = b_familias.apply(lambda row: 0.05 if row["17.1 - Está a menos de 30m de caminhada, ida e volta?"] == "N" else 0, axis=1)

    return pd.merge(base_main, b_familias[["_id", "DIM_I1"]], on="_id", how="left")