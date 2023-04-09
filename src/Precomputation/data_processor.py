import datetime
from typing import Dict, List
import pandas as pd

def get_open_hours(menu_hours: pd.DataFrame) -> dict:
    """Returns a dictionary of the open hours for each day of the week"""
    open_hr = {}
    for i in range(0,7):
        day = menu_hours[menu_hours['day_of_week'] == i]
        day = day[['start_time_local', 'end_time_local']].values.tolist()
        open_hr[i] = day
    return open_hr

def convert_times(time_tc: datetime.time) -> pd.Timedelta:
    """Returns a pd.Timedelta of the given time"""
    days, remainder = divmod(time_tc.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = f"{int(days)} days {datetime.time(int(hours), int(minutes), int(seconds))}"
    return pd.Timedelta(duration_str)


# function to get the active and inactive hours between the given time range
def get_status_timerange(menu_hours: Dict[str, List],
        store_status_TimeRange_ActInact: pd.DataFrame,
        LASK_HR_DATETIME: str,
        CURRENT_DATETIME_SET: str) -> List:
    """Returns a List of the active and inactive hours between the given time range"""

    sub_status_timerange = store_status_TimeRange_ActInact[
        (store_status_TimeRange_ActInact['end_time'] > LASK_HR_DATETIME) &
        (store_status_TimeRange_ActInact['start_time'] < CURRENT_DATETIME_SET)]


    if not len(sub_status_timerange):
        return [datetime.timedelta(hours=0), datetime.timedelta(hours=0)]

    # print(sub_status_timerange,menu_hours)

    def check_time_in_range(time, weekday):
        if not len(menu_hours[weekday]):
            return False

        for i in range(0, len(menu_hours[weekday])):
            if time >= menu_hours[weekday][i][0] and time <= menu_hours[weekday][i][1]:
                return False
        return True
    # if there is nothing to drop, then return the sub_status_timerange
    if not len(sub_status_timerange[(sub_status_timerange['start_time']
                                    .apply(lambda x: check_time_in_range(x.time(),x.weekday())) &
                                    sub_status_timerange['end_time']
                                    .apply(lambda x: check_time_in_range(x.time(),x.weekday())))]):
        sub_status_timerange = sub_status_timerange.drop(
            sub_status_timerange[(sub_status_timerange['start_time']
                .apply(lambda x: check_time_in_range(x.time(),x.weekday())) &
                sub_status_timerange['end_time']
                .apply(lambda x: check_time_in_range(x.time(),x.weekday())))].index)
    # print(sub_status_timerange)

    sum_active_hours, sum_inactive_hours = sub_status_timerange['active_hours'].sum(), sub_status_timerange['inactive_hours'].sum()

    # calculate the time between sub_status_timerange['start_time'] first row and LASK_HR_DATETIME
    start_extra_time = LASK_HR_DATETIME - sub_status_timerange['start_time'].iloc[0]
    if sub_status_timerange['status'].iloc[0] == 'active':
        sum_active_hours -= start_extra_time
    else:
        sum_inactive_hours -= start_extra_time

    # # calculate the time between CURRENT_DATETIME_SET and
    # sub_status_timerange['end_time'] last row
    end_extra_time = sub_status_timerange['end_time'].iloc[-1] - CURRENT_DATETIME_SET
    if sub_status_timerange['status'].iloc[-1] == 'active':
        sum_active_hours -= end_extra_time
    else:
        sum_inactive_hours -= end_extra_time

    return [sum_active_hours, sum_inactive_hours]
