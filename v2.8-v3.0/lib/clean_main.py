import pandas as pd


def CLEAN_MAIN(base_main_with_total: pd.DataFrame) -> pd.DataFrame:
    # Exclui todas as colunas que não serão utilizadas
    columns_to_keep = [
        "_uuid",
        "Analista aplicador",
        "Data de Aplicação",
        "ID",
        "DIM_R1",
        "DIM_R2",
        "DIM_E1",
        "DIM_E2",
        "DIM_I1",
        "DIM_I2",
        "DIM_I3",
        "DIM_I4",
        "DIM_S1",
        "DIM_N1",
        "IPM TOTAL",
    ]
    return base_main_with_total[columns_to_keep]