import numpy as np
from datetime import timedelta, datetime


def add_times(dt, weeks=0, days=0, hours=0, minutes=0, seconds=0, miliseconds=0, microseconds=0):
    """
    function to add times togher

    Keyword arguments:
    dt -- datetime object
    s_to_add -- seconds to add or subtract

    Returns: 
    new_datetime -- datetime object with added or subtracted seconds
    """
    # Add or subtract the timedelta
    new_datetime = dt + timedelta(seconds=seconds,
                                  minutes=minutes,
                                  days=days,
                                  hours=hours,
                                  miliseconds=miliseconds,
                                  microseconds=microseconds,
                                  weeks=weeks
                                  )

    return new_datetime
