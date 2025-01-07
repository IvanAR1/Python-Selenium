import pandas as pd
from typing import Callable
from libs.path.path_utils import AcceptFile, ExistPath, RecursiveFiles

def Load(file:str) -> pd.DataFrame:
    if AcceptFile(file, ".xls|.xlsx"):
        return pd.read_excel(file)
    elif AcceptFile(file, ".csv"):
        return pd.read_csv(file)
    else:
        raise Exception("File isn't an Excel or CSV type")

def Manage(file:str, manipule_xlsx:Callable, min_row:int=1):
    df = Load(file)
    if not df.empty:
        dx = df.iloc[min_row-1:]
        value_return = None
        for index, row in dx.iterrows():
            value_return = manipule_xlsx(index, row, {"dx":dx, "df":df})
            if value_return is False:
                return False
        return value_return

def ManageMultiple(path:str, manipule_xlsx:Callable, min_row:int=1):
    if ExistPath(path):
        RecursiveFiles(path, lambda file: Manage(file, manipule_xlsx, min_row), ".xlsx|.xls|.csv")
        
def AcceptCols(row:pd.Series, accept_name_cols:list = []) -> list:
    total_accept_cols = []
    for name, _ in row.items():
        if isinstance(name, str):
            columnName = str.replace(name, "\n", " ")
            if columnName in accept_name_cols and columnName not in total_accept_cols:
                total_accept_cols.append(columnName)
    return total_accept_cols
    
def GetValueFromRow(index:int, row:pd.Series):
    try:
        return row[index].value
    except:
        return None