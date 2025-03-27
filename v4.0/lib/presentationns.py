import tkinter as tk

import pandas as pd
from pandastable import Table


def show_DataFrame(df: pd.DataFrame):

    # Configurar janela gráfica
    root = tk.Tk()
    root.title("DataFrame no pandastable")

    # Criar um frame para a tabela
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    # Exibir o DataFrame
    pt = Table(frame, dataframe=df)
    pt.show()

    root.mainloop()