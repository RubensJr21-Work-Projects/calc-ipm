import pandas as pd


def E2(base_main: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    # 0. Preparar os dados
    b_membros = base_membros.copy()

    # 1. Verificar se Idade >= 25
    b_membros["Idade >= 25"] = b_membros["Idade"] >= 25

    # 2. Verificar se 'M19 - Qual foi o curso mais elevado que frequentou, no qual concluiu pelo menos uma série/ano?' não está na lista ["EJF", "EJM", "SUP"]
    ## OBS: EDM Não estava na base de cáluclo enviada pelo Rafael
    values_for_opt_educacao = [
        # "EDM", # Deve ser desconsiderado
        "EJF", # Estava faltando (Revisão dia 27/02/2025)
        "EJM",
        "SUP"
    ]
    b_membros["Não concluiu o ensino médio"] = ~b_membros["M19 - Qual foi o curso mais elevado que frequentou, no qual concluiu pelo menos uma série/ano?"].fillna('').isin(values_for_opt_educacao)

    # 3. Verificar M19.1 - E qual foi a última série que foi aprovado? não está na lista ["1G8", "F9A", "M1A", "M2A", "M3A"]
    values_for_opt_educacao_Grad = ["1G8", "F9A", "M1A", "M2A", "M3A"]
    b_membros["Não concluiu o ensino fundamental"] = ~b_membros["M19.1 - E qual foi a última série que foi aprovado?"].fillna('').isin(values_for_opt_educacao_Grad)

    # 4. Cria uma nova coluna testando aquele membro atende a todas as verificações
    b_membros["É adulto e não concluiu o ensino fundamental"] = (
        b_membros["Idade >= 25"]
        &
        b_membros["Não concluiu o ensino médio"]
        &
        b_membros["Não concluiu o ensino fundamental"]
    )

    # 5. Agrupar por "_id" e verificar se todos os membros daquela família atendem à condição
    resultado = (
        b_membros.groupby("_id")["É adulto e não concluiu o ensino fundamental"]
        .all()  # Retorna True se TODOS os membros forem True, senão retorna False
        .reset_index()
        .rename(columns={"É adulto e não concluiu o ensino fundamental": "Todos os membros adultos não concluíram o ensino fundamental"})
    )

    resultado["DIM_E2"] = resultado.apply(lambda row: 0.1 if row["Todos os membros adultos não concluíram o ensino fundamental"] else 0, axis=1)

    return pd.merge(base_main, resultado[["_id", "DIM_E2"]], on="_id", how="left")