from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

# Função para verificar a condição e calcular diferença de meses

#Precisa veriicar se está em branco

def verificar_condicao(row):
    if pd.isna(row['27.1 - Data da última atualização do CadÚnico']):
        return {"condicao": True, "diff": "Sem cadastro/Não informado"}  # Sugestão para NaN

    if row['27.1 - Data da última atualização do CadÚnico'] == "":
        return {"condicao": True, "diff": "Sem cadastro/Não informado"}

    # Calculando a diferença em dias
    diff = pd.to_datetime(row['2 - Data da entrevista']) - pd.to_datetime(row['27.1 - Data da última atualização do CadÚnico'])

    # Calculando a diferença em anos e verificando se é maior que 2 anos
    diff_value = abs(diff.days) / 365.24

    # Calculando a diferença em anos, meses e dias
    diferenca = relativedelta(row['2 - Data da entrevista'], row['27.1 - Data da última atualização do CadÚnico'])

    return {"condicao": diff_value > 2, "diff": f"{diferenca.years} anos, {diferenca.months} meses e {diferenca.days} dias"}



def R1(base_main: pd.DataFrame, base_familias: pd.DataFrame) -> pd.DataFrame:
    
    b_familias = base_familias.copy()
    b_main = base_main

    # Aplicando a função ao DataFrame e expandindo os dicionários em colunas separadas
    b_familias[['condicao', 'Diferença entre 2 - Data da entrevista e 27.1 - Data da última atualização do CadÚnico']] = b_familias.apply(verificar_condicao, axis=1, result_type="expand")
    # Essa coluna estará no DataFrame Main
    b_familias["DIM_R1"] = b_familias["condicao"].apply(lambda x: 0.1 if x else 0)

    print(b_familias)

    return pd.merge(b_main, b_familias[["_id", "DIM_R1"]], on="_id", how="left")
