# code by Ben James on stackoverflow (http://stackoverflow.com/questions/
# 304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar)

import datetime


def iso_year_start(iso_year):
    """The gregorian calendar date of the first day of the given ISO year"""
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    """Gregorian calendar date for the given ISO year, week and day"""
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)