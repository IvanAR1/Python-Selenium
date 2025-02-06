import dateutil
import calendar
from config.framework import FORMAT_DATE
from datetime import datetime, timedelta, date

def add_global(date_:str|datetime, format_ = FORMAT_DATE, **kwargs):
    if isinstance(date_, str):
        date_ = datetime.strptime(date_, format_)
    return date_ + timedelta(**kwargs)

def add_seconds(date_:str|datetime, format_:str=FORMAT_DATE, seconds:float=0) -> datetime:
    return add_global(date_, format_, seconds=seconds)

def add_minutes_and_hours(date_:str|datetime, format_:str=FORMAT_DATE, minutes:float=0, hours:float = 0) -> datetime:
    return add_global(date_, format_, minutes=minutes, hours=hours)

def add_days(date_:str|datetime, format_:str=FORMAT_DATE, days:float = 0) -> datetime:
    return add_global(date_, format_, days=days)

def add_weeks(date_:datetime, format:str=FORMAT_DATE, weeks:int=0) -> datetime:
    return add_global(date_, format_=format, weeks=weeks)

def add_months(dateFrom:datetime, months:int) -> datetime:
    months_count = dateFrom.month + months

    # Calculate the year
    year = dateFrom.year + int(months_count / 12)

    # Calculate the month
    month = (months_count % 12)
    if month == 0:
        month = 12

    # Calculate the day
    day = dateFrom.day

    last_day_of_month = calendar.monthrange(year, month)[1]
    if day > last_day_of_month:
        day = last_day_of_month
    new_date = date(year, month, day)
    return new_date

def add_years(dateFrom:datetime, years:int) -> datetime:
    return dateFrom.replace(year = dateFrom.year + years)

def convert_str_date(date:str, fuzzy=False):
    try: 
        return dateutil.parser.parse(date, fuzzy=fuzzy)
    except:
        return False