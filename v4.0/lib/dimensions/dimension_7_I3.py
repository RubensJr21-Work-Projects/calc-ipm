import pandas as pd


def I3(base_main: pd.DataFrame, base_familias: pd.DataFrame) -> pd.DataFrame:
    b_familias = base_familias.copy()

    b_familias["Test1"] = (
        b_familias["18 - Qual é a forma de iluminação utilizada no seu domicílio?"]
        .fillna('')
        .isin([
            "Óleo, querosene ou gás",
            "Vela",
            "Outra forma"
        ])
    )

    b_familias["Test2"] = (
        (
            b_familias["18 - Qual é a forma de iluminação utilizada no seu domicílio?"]
            .fillna('')
            .isin([
                "Elétrica com medidor próprio",
                "Elétrica com medidor comunitário",
                "Elétrica sem medidor"
            ])
        )
        &
        (
            b_familias["19 - Com que frequência a energia elétrica, proveniente de rede geral, está habitualmente disponível para este domicílio?"]
            .fillna('')
            .isin([
                "Diária, por algumas horas",
                "Outra frequência" # Olhando no formulário do Kobo v4.0 ao invés de "Outra forma" é "Outra frequência"
            ])
        )
    )
    
    b_familias["Test3"] = (
       (
        b_familias["20 - Como são preparadas as refeições?*"]
        .fillna('')
        .isin([
            "Fogão, com gás encanado", # verificado no arquivo "Especificação técnica questionário_V4.0 - formato XLSX" enviado pelo drive
            "Fogão, com gás de botijão",
            "Equipamentos elétricos  (Forno, Microondas, Fogão, Chapa, AirFryer etc)"
        ])
    )
        &
        (
        b_familias["20.1 - A família é obrigada a utilizar outros combustíveis para preparar as refeições durante o mês por falta de dinheiro?"]
        .fillna('')
        .isin([
            "Sim, todo mês acontece",
            "Sim, em alguns meses acontece"
        ])
    )
    )

    b_familias["Test4"] = (
        b_familias["20 - Como são preparadas as refeições?*"]
        .fillna('')
        .isin([
            "Fogão a lenha rudimentar ou improvisado",
            "Outro (Fogareiro, fogueira, usa combustíveis como álcool, querosene, diesel, papelão, plástico etc.)" # Opção "Outra forma" não consta no formulário v4.0. Única opção que pode se assemelhar: "Outro (Fogareiro, fogueira, usa combustíveis como álcool, querosene, diesel, papelão, plástico etc.)" => confirmado no arquivo "Especificação técnica questionário_V4.0 - formato XLSX" enviado pelo drive
        ])
    )

    b_familias["DIM_I3_Comp"] = (
        b_familias["Test1"]
        |
        b_familias["Test2"]
        |
        b_familias["Test3"]
        |
        b_familias["Test4"]
    )

    b_familias["DIM_I3"] = b_familias["DIM_I3_Comp"].apply(lambda x: 0.05 if x else 0)

    return pd.merge(base_main, b_familias[["_id", "DIM_I3"]], on="_id", how="left")