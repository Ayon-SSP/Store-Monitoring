import datetime
import json
import pandas as pd
import data as smData
import data_processor as dataProc

def compute():
    """This function is used to compute the uptime and downtime for each store for the last hour, last 24 hours and last 7 days"""
    # CURRENT_UTCTIME = datetime.datetime.utcnow()
    CURRENT_DATETIME_SET = datetime.datetime.strptime('2023-01-25 20:00:00.000000+00:00', '%Y-%m-%d %H:%M:%S.%f%z')
    LASK_HR_DATETIME = CURRENT_DATETIME_SET - datetime.timedelta(hours=1)
    LASK_24HR_DATETIME = CURRENT_DATETIME_SET - datetime.timedelta(hours=24)
    LASK_7DAYS_DATETIME = CURRENT_DATETIME_SET - datetime.timedelta(days=7)

    # store_ids = smData.get_store_ids()
    # store_ids = store_ids['store_id'].values.tolist()
    store_ids = [2248475475305181449, 955537157727089805, 514003066631838188, 8444136742823051302, 5793938162326382521, 3820046627859013224, 5606755809537460723, 8827394301297670844, 7832590722878413297]

    for store_id in store_ids:
        # print(store_id)

        curRes = smData.Data(store_id)

        menu_hours_curData = dataProc.get_open_hours(curRes.menu_hours)
        store_status_TimeRange_ActInact = curRes.store_status_TimeRange_actInact
        # print(menu_hours_curData) # open hours for each day of the week
        # print(store_status_TimeRange_ActInact) # active and inactive time ranges for each day of the week

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


"""
report_status.json
{"queue": ["36e10e77-3f6f-499d-a5c0-b8eaa128c6af", "f960350f-89d8-4f86-94a3-63698aa06d82", "7b665ab6-ab34-40eb-9a6b-b01e9d8174d4"], "36e10e77-3f6f-499d-a5c0-b8eaa128c6af": {"status": "Running"}, "f960350f-89d8-4f86-94a3-63698aa06d82": {"status": "Running"}, "7b665ab6-ab34-40eb-9a6b-b01e9d8174d4": {"status": "Running"}}
"""

# ⚠️ Need to work on this to make it effective
while True:
    with open('report_status.json', 'r') as f:
        reports_json = json.load(f)
    if reports_json['queue'] and reports_json[reports_json['queue'][0]]['status'] == 'Running':
        report_id = reports_json['queue'][0]
        compute()
        smData.get_store_report_file(report_id)
        reports_json[report_id]['status'] = 'Complete'

        with open('report_status.json', 'w') as f:
            json.dump(reports_json, f)