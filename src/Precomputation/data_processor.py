
import datetime
from typing import Dict, List
import pandas as pd
import data as smData


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
def get_status_timerange(menu_hours: Dict[str, List], store_status_TimeRange_ActInact: pd.DataFrame, LASK_HR_DATETIME: str, CURRENT_DATETIME_SET: str) -> List:
    """Returns a List of the active and inactive hours between the given time range"""


    # get the active_hours where the start_time just after '2023-01-25 22:00:00.000000+00:00' and end_time just after '2023-01-25 23:00:00.000000+00:00'
    sub_status_timerange = store_status_TimeRange_ActInact[(store_status_TimeRange_ActInact['end_time'] > LASK_HR_DATETIME) & (store_status_TimeRange_ActInact['start_time'] < CURRENT_DATETIME_SET)]
    if not len(sub_status_timerange):
        return [datetime.timedelta(hours=0), datetime.timedelta(hours=0)]


    # ⚠️ Need to work on this part
    # menu_hours =
    # {0: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 1: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 2: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 3: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 4: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 5: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 6: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]]}
    # get the sum of all the time difference list of list 2 values in the menu_hours_curData eg : [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]] = 22:59:59 hours and 59 minutes and 59 seconds store this time by appending it to the list
    # menu_hours_curData = []
    # for i in range(0, 7):
    #     menuTotalTime = datetime.timedelta(0)
    #     for j in range(0, len(menu_hours[i])):
    #         t1, t2 = menu_hours[i][j][0], menu_hours[i][j][1]
    #         menuTotalTime += datetime.datetime.combine(datetime.date.today(), t2)-datetime.datetime.combine(datetime.date.today(), t1)
    #     menu_hours_curData.append(convert_times(menuTotalTime))
    # print(menu_hours_curData)

    # remove the rows where the time range is not in between the menu hours : Dict[str, List] =
    # menu_hours_curData =
    # {0: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 1: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 2: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 3: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 4: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 5: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
    # 6: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]]}
    # where the key is the weekday and the value is the list of time ranges for that day

    # sub_status_timerange = sub_status_timerange[sub_status_timerange['start_time'].apply(lambda x: x.time() in menu_hours[x.weekday()]) & sub_status_timerange['end_time'].apply(lambda x: x.time() in menu_hours[x.weekday()])]

    sum_active_hours, sum_inactive_hours = sub_status_timerange['active_hours'].sum(), sub_status_timerange['inactive_hours'].sum()

    # calculate the time between sub_status_timerange['start_time'] first row and LASK_HR_DATETIME
    start_extra_time = LASK_HR_DATETIME - sub_status_timerange['start_time'].iloc[0]
    if sub_status_timerange['status'].iloc[0] == 'active':
        sum_active_hours -= start_extra_time
    else:
        sum_inactive_hours -= start_extra_time


    # # calculate the time between CURRENT_DATETIME_SET and sub_status_timerange['end_time'] last row
    end_extra_time = sub_status_timerange['end_time'].iloc[-1] - CURRENT_DATETIME_SET
    if sub_status_timerange['status'].iloc[-1] == 'active':
        sum_active_hours -= end_extra_time
    else:
        sum_inactive_hours -= end_extra_time

    return [sum_active_hours, sum_inactive_hours]