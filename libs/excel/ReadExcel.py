import pandas as pd
from pathlib import Path
from framework import FrameworkException
from config.framework import EXCEL_ENGINE
from libs.path.utils.folder import RecursiveFiles
from libs.path.utils.file import FileContainsExtension, FileNotUsed
from typing import (
    Union, Dict, Tuple, List
    ,Callable
    ,Any, Literal, Hashable
)

def Load(file:str, **kwargs) -> Union[pd.DataFrame, Dict[Any, pd.DataFrame]]:
    """Read an Excel file into a pandas DataFrame.
    
    .. Files support:
    ======== ========
    File     Is support?
    ======== ========
    xls      Yes
    xlsx     Yes
    xlsm     Yes
    xlsb     Yes
    odf      Yes
    ods      Yes
    odt      Yes
    csv      Yes
    ======== ========

    Args:
        file (str): File path
        **kwargs: Some options in pd.read_excel|pd.read_csv function.
    Raises:
        FrameworkException: In case that file not contains accept extension.
    Returns:
        (pd.DataFrame|dict[any, pd.DataFrame]): Dataframe (consult <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html> for better references)
    """
    if FileContainsExtension(file, ".xlsx|.xlsm"):
        return pd.read_excel(file, engine=EXCEL_ENGINE, **kwargs)
    elif FileContainsExtension(file, ".csv"):
        return pd.read_csv(file, engine=EXCEL_ENGINE, **kwargs)
    elif FileContainsExtension(file, [".xls",".xlsb",".odf",".ods",".odt"]):
        return pd.read_excel(file, **kwargs)
    else:
        raise FrameworkException("File is not an Excel or CSV type")

def Manage(
        file:str, 
        manipule_xlsx:Callable[[Hashable, pd.Series, Dict[str, pd.DataFrame], Path], Union[Any, Literal[False]]] = None,
        min_row:int=1,
        max_cols:int = None, 
        **kwargs) \
    -> Union[
        Tuple[dict, Dict[Any, pd.DataFrame]],
        Any,
        Literal[False],
        None
    ]:
    """Manange an Excel file.

    Args:
        file (str): File path
        manipule_xlsx (Callable[[Hashable, pd.Series, Dict[str, pd.DataFrame], Path], Union[Any, Literal[False]]], optional): Manipule file. Defaults to None.
        min_row (int, optional): First row position to read. Defaults to 1.
        max_cols (int, optional): Max cols to read. Defaults to None.
        **kwargs: Some options in pd.read_excel|pd.read_csv function.

    Returns:
        (Tuple[dict, Dict[Any, pd.Dataframe]]): if contains more than 2 sheets
        Any: any returned in manipule_xlsx callback
        Literal[False]: If manipule_xlsx callback is False
        None: If file is empty.
    """
    if FileNotUsed(file):
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

def ManageMultiple(
        folder_path:str,
        manipule_xlsx:Callable[[Hashable, pd.Series, Dict[str, pd.DataFrame], Path], Union[Any, Literal[False]]] = None,
        min_row:int=1, 
        max_cols:int=None, 
        **kwargs
    ) -> List[Path|Any]:
    """Read files in a folder

    Args:
        folder_path (str): Folder path.
        manipule_xlsx (Callable[[Hashable, pd.Series, Dict[str, pd.DataFrame], Path], Union[Any, Literal[False]]], optional): Manipule file. Defaults to None.
        min_row (int, optional): First row position to read. Defaults to 1.
        max_cols (int, optional): Max cols to read. Defaults to None.
        **kwargs: Some options in pd.read_excel|pd.read_csv function.

    Returns:
        List[Path|Any]: List of read files.
    """
    return RecursiveFiles(folder_path, lambda file: Manage(str(file), manipule_xlsx, min_row, max_cols, **kwargs), ".xlsx|.xls|.csv")
        
def ColsInHeader(row:pd.Series, accept_name_cols:list = []) -> List[str]:
    """Check columns names.

    Args:
        row (pd.Series): Pandas row.
        accept_name_cols (list, optional): List of column names. Defaults to [].

    Returns:
        List[str]: A list with column names in file.
    """
    total_accept_cols = []
    for name, _ in row.items():
        if isinstance(name, str):
            columnName = str.replace(name, "\n", " ")
            if columnName in accept_name_cols and columnName not in total_accept_cols:
                total_accept_cols.append(columnName)
    return total_accept_cols
    
def GetValueFromRow(row:pd.Series, *indexes:int|str) -> Any:
    """Get value of row

    Args:
        row (pd.Series): Pandas row.
        *indexes (int|str): Possible column name or position.
    Raises:
        FrameworkException: If value not found.

    Returns:
        Any: Value column.
    """
    for index in indexes:
        if isinstance(index, str):
            data = row.get(index)
        else:
            data = row.iloc[index]
        if data is not None: 
            return data
    raise FrameworkException(f"Values {indexes} not found in row {row}")