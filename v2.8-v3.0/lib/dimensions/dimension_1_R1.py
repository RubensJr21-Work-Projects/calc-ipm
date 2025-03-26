from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

# Função para verificar a condição e calcular diferença de meses

#Precisa veriicar se está em branco

def verificar_condicao(row):
    if pd.isna(row['dt_CadUnico']):
        return {"condicao": True, "diff": "Sem cadastro/Não informado"}  # Sugestão para NaN

    if row['dt_CadUnico'] == "":
        return {"condicao": True, "diff": "Sem cadastro/Não informado"}

    # Calculando a diferença em dias
    diff = pd.to_datetime(row['Dt_Coleta']) - pd.to_datetime(row['dt_CadUnico'])

    # Calculando a diferença em anos e verificando se é maior que 2 anos
    diff_value = abs(diff.days) / 365.24

    # Calculando a diferença em anos, meses e dias
    diferenca = relativedelta(row['Dt_Coleta'], row['dt_CadUnico'])

    return {"condicao": diff_value > 2, "diff": f"{diferenca.years} anos, {diferenca.months} meses e {diferenca.days} dias"}



def R1(base_main: pd.DataFrame, base_familias: pd.DataFrame) -> pd.DataFrame:
    
    b_familias = base_familias.copy()

    # Aplicando a função ao DataFrame e expandindo os dicionários em colunas separadas
    b_familias[['condicao', 'Diferença entre Dt_Coleta e dt_CadUnico']] = b_familias.apply(verificar_condicao, axis=1, result_type="expand")
    # Essa coluna estará no DataFrame Main
    b_familias["DIM_R1"] = b_familias["condicao"].apply(lambda x: 0.1 if x else 0)

    # print(b_familias)

    return pd.merge(base_main, b_familias[["_uuid", "DIM_R1"]], on="_uuid", how="left")
