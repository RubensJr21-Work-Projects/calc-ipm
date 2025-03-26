import pandas as pd


def I2(base_main: pd.DataFrame, base_familias: pd.DataFrame) -> pd.DataFrame:

    b_familias = base_familias.copy()

    b_familias["bool_Banheiro_COMP"] = b_familias["21 - Existe banheiro de uso exclusivo, com chuveiro e vaso sanitário, neste domicílio, inclusive os localizados no terreno?*"].fillna('').eq('N')
    
    values_for_opt_Escoamento = ["F", "V", "D", "O"]
    b_familias["opt_Escoamento_COMP"] = b_familias["22 - De que forma é feito o escoamento do banheiro ou sanitário?"].fillna('').isin(values_for_opt_Escoamento)

    b_familias["bool_I2"] = b_familias["bool_Banheiro_COMP"] | b_familias["opt_Escoamento_COMP"]

    b_familias["DIM_I2"] = b_familias["bool_I2"].apply(lambda x: 0.05 if x else 0)

    return pd.merge(base_main, b_familias[["_id", "DIM_I2"]], on="_id", how="left")