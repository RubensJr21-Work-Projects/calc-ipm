import pandas as pd


def N1(base_main: pd.DataFrame, base_familias: pd.DataFrame, base_membros: pd.DataFrame) -> pd.DataFrame:
    b_familias = base_familias.copy()
    b_membros = base_membros.copy()

    # perguntas EBIAs

    questionsEBIAs = [
        "32 - Nos últimos 3 meses os alimentos acabaram antes que os moradores deste domicílio tivessem dinheiro para comprar mais comida?",
        "33 - Nos últimos 3 meses houve preocupação de que os alimentos acabassem antes de poder comprar ou receber mais comida?",
        "34 - Nos últimos 3 meses, ficaram sem dinheiro para ter uma alimentação saudável e variada?",
        "35 - Nos últimos 3 meses, comeram apenas alguns poucos tipos de alimentos que ainda tinham, porque o dinheiro acabou?",
        "36 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, deixou de fazer alguma refeição?",
        "37 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, comeu menos do que achou que devia?",
        "38 - Nos últimos 3 meses, algum adulto da família, por falta de dinheiro, sentiu fome, mas não comeu?",
        "39 - Nos últimos 3 meses, algum adulto da família, fez apenas uma refeição ao dia ou ficou um dia inteiro sem comer?",
        "40 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, deixou de ter uma alimentação saudável e variada?",
        "41 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, alguma vez, não comeu quantidade suficiente de comida?",
        "42 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, foi diminuída a quantidade de alimentos das refeições?",
        "43 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, deixou de fazer alguma refeição?",
        "44 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, sentiu fome, mas não comeu?",
        "45 - Nos últimos 3 meses, algum menor de 18 anos da família, por falta de dinheiro, fez apenas uma refeição ao dia ou ficou sem comer por um dia inteiro?",
    ]

    # Contando quantos valores são 'Sim' em cada linha
    b_familias['Soma_EBIA'] = b_familias[questionsEBIAs].apply(lambda x: (x == 'Sim').sum(), axis=1) # Estava N

    b_membros["0 <= Idade < 18"] = b_membros["Idade"].between(0, 18, inclusive="left")

    # Agrupando por Id_familia e verificando se pelo menos um membro atende à condição
    df_resultado = b_membros.groupby('_id')['0 <= Idade < 18'].any().reset_index()

    # Renomeando a coluna final
    df_resultado.rename(columns={'0 <= Idade < 18': 'TemCriançaAdolescente'}, inplace=True)

    # Fazendo o JOIN com base no '_id'
    b_familias = pd.merge(b_familias, df_resultado, on='_id', how='left')


    b_familias["Test1"] = (
        (b_familias["TemCriançaAdolescente"] == True)
        &
        (b_familias["Soma_EBIA"] > 5)
    )
    b_familias["Test2"] = (
        (b_familias["TemCriançaAdolescente"] == False)
        &
        (b_familias["Soma_EBIA"] > 3)
    )

    b_familias["Test1 or Test2"] = b_familias["Test1"] | b_familias["Test2"]

    b_familias["DIM_N1"] = b_familias.apply(lambda row: 0.2 if row["Test1 or Test2"] else 0, axis=1)

    return pd.merge(base_main, b_familias[["_id", "DIM_N1"]], on="_id", how="left")