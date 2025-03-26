from typing import TypedDict

import pandas as pd


class ValidFileExcel(TypedDict):
    Base_Familias: pd.DataFrame
    Base_Membros: pd.DataFrame
    base_filename: str
    file: str