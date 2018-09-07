import holidays

def make_holidays(days):
    """ something stopped working """
    us_holidays = list() # holidays.UnitedStates()

    def assign_holiday(row):
        if row.name in us_holidays or row.weekday == 6:
            return "Holiday, Sunday"
        if row.weekday == 5:
            return "Saturday"
        else:
            return "Working Day"

    return days.apply(lambda x: assign_holiday(x), axis = 1)

