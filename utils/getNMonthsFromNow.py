import datetime


def getNMonthsFromNow(num):
    current_datetime = datetime.datetime.now()
    three_months_from_now = current_datetime.replace(month=current_datetime.month + num)
    return three_months_from_now
