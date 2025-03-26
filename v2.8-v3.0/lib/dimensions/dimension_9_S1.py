import pandas as pd


def S1(base_main: pd.DataFrame, base_familias: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    # 0. Preparar os dados
    b_familias = base_familias.copy()
    b_membros = base_membros.copy()

    # 1. Verificar se opt_doencas != "" AND se bool_acomp_SUS == "N"
    b_membros["Tem doente grave sem SUS"] = (
        ~b_membros["opt_doencas"].fillna("").eq("")
        &
        b_membros["bool_acomp_SUS"].fillna("").eq("N")
    )

    # 2. Verificar se 1 <= Idade <=17 AND bool_vacinas == "N"
    b_membros["É criança sem vacina"] = (
        b_membros["Idade"].between(1, 17, inclusive="both")
        &
        b_membros["bool_vacinas"].fillna("").eq("N")
    )

    # 3. Verificar se opt_gestantes == "N"
    b_familias["Tem gestante sem SUS"] = b_familias["opt_gestantes"].fillna("").eq("N") # opt_gestantes

    # 4. Verificar se opt_Deficiencias != "" AND opt_tec_assistiva == "V" (Tem PCD e Não possui Tecnologia assistiva)
    b_membros["Tem PCD e não possui Tecnologia assistiva"] = (
        ~b_membros["opt_Deficiencias"].fillna("").eq("")
        &
        b_membros["opt_tec_assistiva"].fillna("").eq("V")
    )

    b_membros["Atende condições S1"] = (
        b_membros["Tem doente grave sem SUS"]
        |
        b_membros["É criança sem vacina"]
        |
        b_membros["Tem PCD e não possui Tecnologia assistiva"]
    )

    # 5. Agrupar por "_uuid" e verificar se pelo menos 1 membro daquela família atendem às condições dos membros
    resultado_membros = (
        b_membros.groupby("_uuid")["Atende condições S1"]
        .any() # Retorna True se algum dos membros forem True, senão retorna False
        .reset_index()
        .rename(columns={"Atende condições S1": "Algum membro atende condições S1"})
    )

    b_familias = pd.merge(b_familias, resultado_membros, on="_uuid", how="left")

    b_familias["DIM_S1_Comp"] = (
        b_familias["Tem gestante sem SUS"]
        |
        b_familias["Algum membro atende condições S1"]
    )

    b_familias["DIM_S1"] = b_familias["DIM_S1_Comp"].apply(lambda x: 0.2 if x else 0)

    return pd.merge(base_main, b_familias[["_uuid", "DIM_S1"]], on="_uuid", how="left")