import datetime
import pandas as pd
import data as smData
import data_processor as dataProc

CURRENT_DATETIME_SET = datetime.datetime.strptime('2023-01-25 20:00:00.000000+00:00', '%Y-%m-%d %H:%M:%S.%f%z')
LASK_HR_DATETIME = CURRENT_DATETIME_SET - datetime.timedelta(hours=1)
LASK_24HR_DATETIME = CURRENT_DATETIME_SET - datetime.timedelta(hours=24)
LASK_7DAYS_DATETIME = CURRENT_DATETIME_SET - datetime.timedelta(days=7)

# store_ids = smData.get_store_ids()
# store_ids = store_ids['store_id'].values.tolist()

store_ids = [2248475475305181449, 955537157727089805, 514003066631838188, 8444136742823051302, 5793938162326382521, 3820046627859013224, 5606755809537460723, 8827394301297670844, 7832590722878413297]

"""
store_ids = 7832590722878413297

menu_hours_curData =
{0: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
1: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
2: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
3: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
4: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
5: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]],
6: [[datetime.time(0, 0), datetime.time(1, 0)], [datetime.time(7, 0), datetime.time(23, 59, 59)]]}

store_status_TimeRange_ActInact =
    status                  timestamp_local                       start_time                         end_time            active_hours          inactive_hours
0    inactive 2023-01-18 05:09:50.541419+00:00                              NaT 2023-01-18 05:09:50.541419+00:00                       0                     NaT
1    inactive 2023-01-18 06:10:07.117301+00:00 2023-01-18 05:09:50.541419+00:00 2023-01-18 06:10:07.117301+00:00                       0  0 days 01:00:16.575882
2    inactive 2023-01-18 07:08:06.892883+00:00 2023-01-18 06:10:07.117301+00:00 2023-01-18 07:08:06.892883+00:00                       0  0 days 00:57:59.775582
3    inactive 2023-01-18 08:01:20.661140+00:00 2023-01-18 07:08:06.892883+00:00 2023-01-18 08:01:20.661140+00:00                       0  0 days 00:53:13.768257
4    inactive 2023-01-18 09:09:04.075382+00:00 2023-01-18 08:01:20.661140+00:00 2023-01-18 09:09:04.075382+00:00                       0  0 days 01:07:43.414242
..        ...                              ...                              ...                              ...                     ...                     ...
240    active 2023-01-25 21:06:05.179555+00:00 2023-01-25 21:00:44.204098+00:00 2023-01-25 21:06:05.179555+00:00  0 days 00:05:20.975457                       0
241    active 2023-01-25 22:01:19.496218+00:00 2023-01-25 21:06:05.179555+00:00 2023-01-25 22:01:19.496218+00:00  0 days 00:55:14.316663                       0
242    active 2023-01-25 22:06:45.790348+00:00 2023-01-25 22:01:19.496218+00:00 2023-01-25 22:06:45.790348+00:00  0 days 00:05:26.294130                       0
243    active 2023-01-25 23:00:54.239712+00:00 2023-01-25 22:06:45.790348+00:00 2023-01-25 23:00:54.239712+00:00  0 days 00:54:08.449364                       0
244    active 2023-01-25 23:03:17.170336+00:00 2023-01-25 23:00:54.239712+00:00 2023-01-25 23:03:17.170336+00:00  0 days 00:02:22.930624                       0
"""

for store_id in store_ids:
    print(store_id)

    curRes = smData.Data(store_id)

    menu_hours_curData = dataProc.get_open_hours(curRes.menu_hours)
    store_status_TimeRange_ActInact = curRes.store_status_TimeRange_actInact

    # print(menu_hours_curData) # open hours for each day of the week
    # print(store_status_TimeRange_ActInact) # active and inactive time ranges for each day of the week


    # get the current active hours for the store_status_TimeRange_ActInact between the current time and the last 24 hours and also the active and inactive hours should be in range of the menu_hours_curData where weak is given
    # store_status_TimeRange_ActInact = dataProc.get_current_active_hours_(menu_hours_curData, store_status_TimeRange_ActInact, CURRENT_DATETIME_SET)
    # get_status_timerange = dataProc.get_current_active_hours(menu_hours_curData, store_status_TimeRange_ActInact, CURRENT_DATETIME_SET)
    last_hr_status = dataProc.get_status_timerange(menu_hours_curData, store_status_TimeRange_ActInact, LASK_HR_DATETIME, CURRENT_DATETIME_SET)
    last_day_status = dataProc.get_status_timerange(menu_hours_curData, store_status_TimeRange_ActInact, LASK_24HR_DATETIME, CURRENT_DATETIME_SET)
    last_week_status = dataProc.get_status_timerange(menu_hours_curData, store_status_TimeRange_ActInact, LASK_7DAYS_DATETIME, CURRENT_DATETIME_SET)
    uptime_last_hour, downtime_last_hour = last_hr_status
    uptime_last_day, downtime_last_day = last_day_status
    update_last_week, downtime_last_week = last_week_status

    # Take this example 7832590722878413297 for proper understanding
    # print(uptime_last_hour, downtime_last_hour)
    # print(uptime_last_day, downtime_last_day)
    # print(update_last_week, downtime_last_week)

    res = smData.store_report_insert(store_id,
                                    uptime_last_hour.total_seconds() / 60.0,
                                    uptime_last_day.total_seconds() / 3600.0,
                                    update_last_week.total_seconds() / 3600.0,
                                    downtime_last_hour.total_seconds() / 60.0,
                                    downtime_last_day.total_seconds() / 3600.0,
                                    downtime_last_week.total_seconds() / 3600.0)
    if res:
        print(store_id, "Inserted successfully")
    else:
        print(store_id, "Insertion failed")
