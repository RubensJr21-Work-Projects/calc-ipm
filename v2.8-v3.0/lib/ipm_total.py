import pandas as pd


def IPM_TOTAL(base_main_with_dimensions: pd.DataFrame) -> pd.DataFrame:
    # Somar todas as colunas de Dimensão
    prefix = "DIM_"
    base_main_with_dimensions["IPM TOTAL"] = base_main_with_dimensions[[col for col in base_main_with_dimensions.columns if col.startswith(prefix)]].sum(axis=1)
    return base_main_with_dimensions