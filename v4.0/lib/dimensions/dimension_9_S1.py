import pandas as pd


def S1(base_main: pd.DataFrame, base_familias: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    # 0. Preparar os dados
    b_familias = base_familias.copy()
    b_membros = base_membros.copy()

    # 1. Verificar se M12 != "" AND se M12.1 == "Não"
    b_membros["Tem doente grave sem SUS"] = (
        ~b_membros["M12 - Tem alguma das doenças abaixo?"].fillna("").eq("")
        &
        b_membros["M12.1 - Se sim, está em acompanhamento médico (rede privada ou SUS)?"].fillna("").eq("Não")
    )

    # 2. Verificar se 1 <= Idade <=17 AND M11 == "Não"
    b_membros["É criança sem vacina"] = (
        b_membros["Idade"].between(1, 17, inclusive="both")
        &
        b_membros["M11 - Recebeu todas as vacinas do Calendário Nacional de Vacinação do Sistema Único de Saúde?"].fillna("").eq("Não")
    )

    # 3. Verificar se 31 == "Não"
    # Na versão v4.0 do questionário o valor deixa de ser apenas "Não" para ser "Não, uma ou mais gestantes não tem o acompanhamento pré-natal"
    resposta_a_ser_verificada = "Não, uma ou mais gestantes não tem o acompanhamento pré-natal"
    b_familias["Tem gestante sem SUS"] = b_familias["31 - Todas as gestantes estão tendo acompanhamento pré-natal?"].fillna("").eq(resposta_a_ser_verificada)

    # 4. Verificar se M13 != "" AND M13.4 == "Sim, e não possuo o equipamento necessário" (Tem PCD e Não possui Tecnologia assistiva)
    b_membros["Tem PCD e não possui Tecnologia assistiva"] = (
        ~b_membros["M13 - O morador tem alguma deficiência e/ou transtorno que limite as suas atividades habituais (como trabalhar, ir à escola, brincar, etc.) ?"].fillna("").eq("")
        &
        b_membros["M13.4 - Em função dessa deficiência e/ou transtorno precisa de alguma tecnologia assistiva (cadeira de rodas, muleta, prótese, pranchas de comunicação, ou outro recurso ou aparelho) para realizar suas atividades cotidianas?"].fillna("").eq("Sim, e não possuo o equipamento necessário")
    )

    b_membros["Atende condições S1"] = (
        b_membros["Tem doente grave sem SUS"]
        |
        b_membros["É criança sem vacina"]
        |
        b_membros["Tem PCD e não possui Tecnologia assistiva"]
    )

    # 5. Agrupar por "_id" e verificar se pelo menos 1 membro daquela família atendem às condições dos membros
    resultado_membros = (
        b_membros.groupby("_id")["Atende condições S1"]
        .any() # Retorna True se algum dos membros forem True, senão retorna False
        .reset_index()
        .rename(columns={"Atende condições S1": "Algum membro atende condições S1"})
    )

    b_familias = pd.merge(b_familias, resultado_membros, on="_id", how="left")

    b_familias["DIM_S1_Comp"] = (
        b_familias["Tem gestante sem SUS"]
        |
        b_familias["Algum membro atende condições S1"]
    )

    b_familias["DIM_S1"] = b_familias["DIM_S1_Comp"].apply(lambda x: 0.2 if x else 0)

    return pd.merge(base_main, b_familias[["_id", "DIM_S1"]], on="_id", how="left")