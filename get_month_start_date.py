import calendar
import datetime


def get_month_start_date_and_end_date(year, month):
    """
    Returns the start date and end date of the month in the format
    (start_date, end_date) where both start_date and end_date are datetime.date objects
    """
    # get the first day of the month
    start_date = datetime.date(year, month, 1)
    # get the last day of the month
    end_date = start_date + datetime.timedelta(calendar.monthrange(year, month)[1] - 1)
    diff = end_date - start_date
    print(diff.days)
    return start_date.day,start_date.month,start_date.year, diff.days

print(get_month_start_date_and_end_date(2021, 2))