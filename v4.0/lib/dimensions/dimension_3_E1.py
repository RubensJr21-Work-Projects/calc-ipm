import pandas as pd


def E1(base_main: pd.DataFrame, base_familias: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    # 0. Preparar os dados
    b_familias = base_familias.copy()
    b_membros = base_membros.copy()

    # 1.
    # 1.1 Verificar se M19 - Qual foi o curso mais elevado que frequentou, no qual concluiu pelo menos uma série/ano? != ["EJM", "SUP"] OR M19.1 - E qual foi a última série que foi aprovado? != "M3A"
    ## OBS: EDM Não estava na base de cáluclo enviada pelo Rafael
    ## OBS(Revisão pós reunião): Em conversa com Rafel, ele informou que o EDM não conta
    ##       "Pois quem responder EDM ainda estará estudando, e consequentemente não completou o ensino médio"
    values_for_opt_educacao = ["EJM", "SUP"]
    b_membros["Não concluiu o ensino médio"] = (
        ~b_membros["M19 - Qual foi o curso mais elevado que frequentou, no qual concluiu pelo menos uma série/ano?"].isin(values_for_opt_educacao)
        |
        ~b_membros["M19.1 - E qual foi a última série que foi aprovado?"].fillna("").eq("M3A")
    )
    
    # 1.2 Verificar se 4 <= Idade <= 17
    b_membros["4 <= Idade <= 17"] = b_membros["Idade"].between(4, 17, inclusive="both")

    # 1.3 Verificar se M16 - Frequenta regularmente a escola? (exclusiva para MENOR de 18 anos) == "N" OR M17 - Está em risco de exclusão escolar? (exclusiva para MENOR de 18 anos) == "N" OR M18 - Está matriculado na escola? (exclusiva para MENOR de 18 anos) == "N"
    b_membros["Fora da escola ou em risco"] = (
        b_membros["M16 - Frequenta regularmente a escola? (exclusiva para MENOR de 18 anos)"].fillna("").eq("N")
        |
        b_membros["M17 - Está em risco de exclusão escolar? (exclusiva para MENOR de 18 anos)"].fillna("").eq("S") # Deveria ser S
        |
        b_membros["M18 - Está matriculado na escola? (exclusiva para MENOR de 18 anos)"].fillna("").eq("N")
    )


    # 2. 
    # 2.1 Verificar mesma coisa do 1.1
    # 2.2 Verificar se 18 <= Idade <= 24
    b_membros["18 <= Idade <= 24"] = b_membros["Idade"].between(18, 24, inclusive="both")

    # 2.3 M15 - Está estudando? == "N"
    b_membros["Não está estudando"] = b_membros["M15 - Está estudando?"].fillna("").eq("N")

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

    # 5. Agrupar por "_id" e verificar se pelo menos 1 membro daquela família atendem às condições dos membros 
    resultado_membros = (
        b_membros.groupby("_id")["Atende condições E1"]
        .any() # Retorna True se algum dos membros forem True, senão retorna False
        .reset_index()
        .rename(columns={"Atende condições E1": "Algum membro atende condições E1"}) 
    )

    b_familias = pd.merge(b_familias, resultado_membros, on="_id", how="left")

    b_familias["DIM_E1"] = b_familias["Algum membro atende condições E1"].apply(lambda x: .1 if x else 0)

    return pd.merge(base_main, b_familias[["_id", "DIM_E1"]], on="_id", how="left")