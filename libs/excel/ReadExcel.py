import pandas as pd
from typing import Callable, Sequence
from config.framework import EXCEL_ENGINE
from libs.path.path_utils import AcceptFile, ExistPath, RecursiveFiles

def Load(file:str, **kwargs):
    if AcceptFile(file, ".xls|.xlsx"):
        return pd.read_excel(file, engine=EXCEL_ENGINE, **kwargs)
    elif AcceptFile(file, ".csv"):
        return pd.read_csv(file, engine=EXCEL_ENGINE, **kwargs)
    else:
        raise Exception("File isn't an Excel or CSV type")

def Manage(file:str, manipule_xlsx:Callable = None, min_row:int=1, max_cols:int = None, **kwargs):
    df = Load(file, **kwargs)
    if isinstance(df, dict):
        dx={}
        for index, dataFrame in df.items():
            df[index] = dataFrame.iloc[:, :max_cols]
            dx[index] = dataFrame.iloc[min_row-1:]
        return dx, df
    df = df.iloc[:, :max_cols]
    if not df.empty:
        dx = df.iloc[min_row-1:]
        if isinstance(manipule_xlsx, Callable):
            value_return = None
            for index, row in dx.iterrows():
                excel = {"dx":dx, "df":df}
                returned_call = manipule_xlsx(index, row, excel, file)
                if returned_call is False:
                    return (False, value_return)[value_return is not None]
                if returned_call is not None:
                    value_return = returned_call
            return value_return
        else:
            return dx, df

def ManageMultiple(path:str, manipule_xlsx:Callable, min_row:int=1, max_cols:int=None, **kwargs):
    if ExistPath(path):
        RecursiveFiles(path, lambda file: Manage(file, manipule_xlsx, min_row, max_cols, **kwargs), ".xlsx|.xls|.csv")
        
def ColsInHeader(row:pd.Series, accept_name_cols:list = []) -> list:
    total_accept_cols = []
    for name, _ in row.items():
        if isinstance(name, str):
            columnName = str.replace(name, "\n", " ")
            if columnName in accept_name_cols and columnName not in total_accept_cols:
                total_accept_cols.append(columnName)
    return total_accept_cols
    
def GetValueFromRow(row:pd.Series, index:int|str):
    try:
        return row[index]
    except:
        return None