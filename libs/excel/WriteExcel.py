import pandas as pd
from framework import FrameworkException
from libs.path.utils.file import FileContainsExtension

def OverwriteSheetOnlySheet(file:str, data:dict|list|pd.DataFrame, index:bool = False, **kwargs):
    """Save file with one sheet (or csv).

    Args:
        file (str): File path.
        data (dict | list | pd.DataFrame): Data to save.
        index (bool, optional): Write row names (index). Defaults to False.
        **kwargs: some options in df.to_excel|df.to_csv
    """
    df = _process_data(data)
    if FileContainsExtension(file, ".xlsx|.xls"):
        with pd.ExcelWriter(file, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=index, **kwargs)
    elif FileContainsExtension(file, ".csv"):
        df.to_csv(file, index=index, **kwargs)

def OverwriteSheetManySheet(file:str, sheets_data:dict|list, **kwargs):
    """Save file with many sheets

    Args:
        file (str): File path
        sheets_data (dict | list): Data sheets.
        **kwargs: some options in df.to_excel.
    """
    with pd.ExcelWriter(file, mode='a', if_sheet_exists='replace') as writer:
        for sheetName, data in sheets_data.items():
            df = _process_data(data)
            df.to_excel(writer, sheet_name=sheetName, index=False, **kwargs)
    
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