from datetime import datetime, timedelta, date
import dateutil
import calendar

def add_seconds(date:str, format:str, seconds:float) -> datetime:
    return datetime.strptime(date, format) + timedelta(seconds=seconds)

def add_minutes_and_hours(date:str, format:str, minutes:float=0, hours:float = 0) -> datetime:
    return datetime.strptime(date, format) + timedelta(minutes=minutes, hours=hours)

def add_days(date:str, format:str, days:float) -> datetime:
    return datetime.strptime(date, format) + timedelta(days=days)

def add_weeks(dateFrom:datetime, weeks:int) -> datetime:
    return dateFrom + timedelta(weeks=weeks)

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