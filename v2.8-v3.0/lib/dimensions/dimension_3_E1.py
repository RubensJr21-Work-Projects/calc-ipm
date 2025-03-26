import pandas as pd


def E1(base_main: pd.DataFrame, base_familias: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    # 0. Preparar os dados
    b_familias = base_familias.copy()
    b_membros = base_membros.copy()

    # 1.
    # 1.1 Verificar se opt_educacao != ["EJM", "SUP"] OR opt_educacao_Grad != "M3A"
    ## OBS: EDM Não estava na base de cáluclo enviada pelo Rafael
    ## OBS(Revisão pós reunião): Em conversa com Rafel, ele informou que o EDM não conta
    ##       "Pois quem responder EDM ainda estará estudando, e consequentemente não completou o ensino médio"
    values_for_opt_educacao = ["EJM", "SUP"]
    b_membros["Não concluiu o ensino médio"] = (
        ~b_membros["opt_educacao"].isin(values_for_opt_educacao)
        |
        ~b_membros["opt_educacao_Grad"].fillna("").eq("M3A")
    )
    
    # 1.2 Verificar se 4 <= Idade <= 17
    b_membros["4 <= Idade <= 17"] = b_membros["Idade"].between(4, 17, inclusive="both")

    # 1.3 Verificar se bool_Frequenta_escola == "N" OR bool_exclusao_escolar == "N" OR bool_Matriculado_escola == "N"
    b_membros["Fora da escola ou em risco"] = (
        b_membros["bool_Frequenta_escola"].fillna("").eq("N")
        |
        b_membros["bool_exclusao_escolar"].fillna("").eq("S") # Deveria ser S
        |
        b_membros["bool_Matriculado_escola"].fillna("").eq("N")
    )


    # 2. 
    # 2.1 Verificar mesma coisa do 1.1
    # 2.2 Verificar se 18 <= Idade <= 24
    b_membros["18 <= Idade <= 24"] = b_membros["Idade"].between(18, 24, inclusive="both")

    # 2.3 bool_Esta_estudando == "N"
    b_membros["Não está estudando"] = b_membros["bool_Esta_estudando"].fillna("").eq("N")

    b_membros["Test_1"] = (
        b_membros["Não concluiu o ensino médio"]
        &
        b_membros["4 <= Idade <= 17"]
        &
        b_membros["Fora da escola ou em risco"]
    )

    b_membros["Test_2"] = (
        b_membros["Não concluiu o ensino médio"]
        &
        b_membros["18 <= Idade <= 24"]
        &
        b_membros["Não está estudando"]
    )

    b_membros["Atende condições E1"] = (
        b_membros["Test_1"]
        |
        b_membros["Test_2"]
    )

    # 5. Agrupar por "_uuid" e verificar se pelo menos 1 membro daquela família atendem às condições dos membros 
    resultado_membros = (
        b_membros.groupby("_uuid")["Atende condições E1"]
        .any() # Retorna True se algum dos membros forem True, senão retorna False
        .reset_index()
        .rename(columns={"Atende condições E1": "Algum membro atende condições E1"}) 
    )

    b_familias = pd.merge(b_familias, resultado_membros, on="_uuid", how="left")

    b_familias["DIM_E1"] = b_familias["Algum membro atende condições E1"].apply(lambda x: .1 if x else 0)

    return pd.merge(base_main, b_familias[["_uuid", "DIM_E1"]], on="_uuid", how="left")