import calendar
from config.framework import FORMAT_DATE
from datetime import datetime, timedelta, date

def add_global(date_:str|datetime, format_:str = FORMAT_DATE, **kwargs) -> datetime:
    """Add specific type of date/time to datetime using timedelta.

    Args:
        date_ (str | datetime): Datetime current.
        format_ (str, optional): Specific a format. Defaults to config.framework.FORMAT_DATE.
        **kwargs: Additional keyword arguments to timedelta.

    Returns:
        datetime: Datetime formated.
    """
    if isinstance(date_, str):
        date_ = datetime.strptime(date_, format_)
    return date_ + timedelta(**kwargs)

def add_seconds(date_:str|datetime, format_:str=FORMAT_DATE, seconds:float=0) -> datetime:
    """Add seconds to datetime.

    Args:
        date_ (str | datetime): Datetime current. 
        format_ (str, optional): Specific a format. Defaults to config.framework.FORMAT_DATE.
        seconds (float, optional): Seconds to add. Defaults to 0.

    Returns:
        datetime: Datetime formated
    """
    return add_global(date_, format_, seconds=seconds)

def add_minutes_and_hours(date_:str|datetime, format_:str=FORMAT_DATE, minutes:float=0, hours:float = 0) -> datetime:
    """Add minutes and/or hours to datetime.

    Args:
        date_ (str | datetime): Datetime current.
        format_ (str, optional): Specific a format. Defaults to config.framework.FORMAT_DATE.
        minutes (float, optional): Add minutes to date. Defaults to 0. 
        hours (float, optional): Hours to add. Defaults to 0.

    Returns:
        datetime: Datetime formated.
    """
    return add_global(date_, format_, minutes=minutes, hours=hours)

def add_days(date_:str|datetime, format_:str=FORMAT_DATE, days:float = 0) -> datetime:
    """Add days to datetime.

    Args:
        date_ (str | datetime): Datetime current.
        format_ (str, optional): Specific a format. Defaults to config.framework.FORMAT_DATE.
        days (float, optional): Days to add. Defaults to 0.

    Returns:
        datetime: Datetime formated.
    """
    return add_global(date_, format_, days=days)

def add_weeks(date_:datetime, format_:str=FORMAT_DATE, weeks:int=0) -> datetime:
    """Add weeks to datetime.

    Args:
        date_ (datetime): Datetime current.
        format_ (str, optional): Specific a format. Defaults to config.framework.FORMAT_DATE.
        weeks (int, optional): Weeks to add. Defaults to 0.

    Returns:
        datetime: Datetime formated.
    """
    return add_global(date_, format_, weeks=weeks)

def add_months(date_:datetime, months:int) -> datetime:
    """Add months to Datetime. In this case, timedelta is not used.

    Args:
        date_ (datetime): Date current.
        months (int): Months to add.

    Returns:
        datetime: Datetime formated.
    """
    months_count = date_.month + months

    # Calculate the year
    year = date_.year + int(months_count / 12)

    # Calculate the month
    month = (months_count % 12)
    if month == 0:
        month = 12

    # Calculate the day
    day = date_.day

    last_day_of_month = calendar.monthrange(year, month)[1]
    if day > last_day_of_month:
        day = last_day_of_month
    new_date = date(year, month, day)
    return new_date

def add_years(date_:datetime, years:int) -> datetime:
    """Add years to datetime. In this case, timedelta is not used.

    Args:
        date_ (datetime): Date current.
        years (int): Years to add.

    Returns:
        datetime: Datetime formated.
    """
    return date_.replace(year = date_.year + years)