from libs.path.path_utils import AcceptFile, ExistPath
import pandas as pd

def OverwriteSheetOnlySheet(file:str, data:dict|list|pd.DataFrame, index:bool = False, **kwargs):
    df = process_data(data)
    if AcceptFile(file, ".xlsx|.xls"):
        with pd.ExcelWriter(file, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=index, **kwargs)
    elif AcceptFile(file, ".csv"):
        df.to_csv(file, index=index, **kwargs)

def OverwriteSheetManySheet(file:str, sheets_data:dict|list, **kwargs):
    with pd.ExcelWriter(file, mode='a', if_sheet_exists='replace') as writer:
        for sheetName, data in sheets_data.items():
            df = process_data(data)
            df.to_excel(writer, sheet_name=sheetName, index=False, **kwargs)
    
def process_data(data):
    match data:
        case dict():
            return pd.DataFrame.from_dict(data)
        case list():
            return pd.DataFrame(data)
        case _:
            if isinstance(data, pd.DataFrame):
                return data
            raise Exception("Data isn't list or dict")