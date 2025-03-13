import warnings
from typing import Literal
from dateutil import parser
from datetime import datetime

def convert_str_to_date(date_:str, fuzzy=False, **kwargs) -> datetime|Literal[False]:
    """Convert str to date

    Args:
        date_ (str): Datetime str current.
        fuzzy (bool, optional): Whether to allow fuzzy parsing, allowing for string like "Today is January 1, 2047 at 8:21:00AM". Defaults to False.
        **kwargs: Additional keyword arguments to dateutil.parser.parse.

    Returns:
        datetime|Literal[False]: Datetime. False in case of Exception. 
    """
    try: 
        return parser.parse(date_, fuzzy=fuzzy, **kwargs)
    except (parser.ParserError, OverflowError, Exception) as e:
        warnings.simplefilter("all", UserWarning)
        warnings.warn(
            f"An error occurred when parse from string to datetime: {repr(e), e}"
            ,category=UserWarning
            ,stacklevel=1
        )
        warnings.simplefilter("default", UserWarning)
        return False