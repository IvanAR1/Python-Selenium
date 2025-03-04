import pandas as pd
from framework import FrameworkException
from config.framework import EXCEL_ENGINE
from typing import Dict, Any, Union, List
from libs.path.utils.file import FileContainsExtension, DeleteFile

def OverwriteSheetOnlySheet(file:str, data:dict|list|pd.DataFrame=None, index:bool = False, **kwargs):
    """Save file with one sheet (or csv).

    Args:
        file (str): File path.
        data (dict | list | pd.DataFrame): Data to save.
        index (bool, optional): Write row names (index). Defaults to False.
        **kwargs: some options in df.to_excel|df.to_csv
    """
    df = _process_data(data)
    if FileContainsExtension(file, ".xlsx|.xls"):
        DeleteFile(file)
        writer = pd.ExcelWriter(file, engine=EXCEL_ENGINE)
        df.to_excel(writer, index=index, **kwargs)
        writer.close()
    elif FileContainsExtension(file, ".csv"):
        df.to_csv(file, index=index, **kwargs)

def OverwriteSheetManySheet(file:str, data:Union[Dict[List, Any]], index:bool=False, **kwargs):
    """Save file with many sheets

    Args:
        file (str): File path
        sheets_data (list[dict]): Data sheets.
        index (bool, optional): Write row names (index). Defaults to False.
        **kwargs: some options in df.to_excel.
    """
    DeleteFile(file)
    writer = pd.ExcelWriter(file, engine=EXCEL_ENGINE)
    for sheetName, sheetData in data.items():
        _process_data(sheetData).to_excel(writer, sheetName, index=index, **kwargs)    
    writer.close()
    
def _process_data(data:dict|list|pd.DataFrame) -> pd.DataFrame:
    """Check type of data.

    Private:
        Not uses this function.

    Args:
        data (dict|list|pd.DataFrame): Type data.

    Raises:
        FrameworkException: If data is not dict|list|pd.DataFrame

    Returns:
        DataFrame: pd.DataFrame
    """
    match data:
        case dict():
            return pd.DataFrame.from_dict(data)
        case list():
            return pd.DataFrame(data)
        case _:
            if isinstance(data, pd.DataFrame):
                return data
            raise FrameworkException("Data isn't list or dict")