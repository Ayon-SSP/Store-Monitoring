import datetime
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from Configuration import *
import Configuration as config


engine = create_engine(config.db_connection_string)
engine

def get_store_ids():
    store_ids = pd.read_sql_query('''
                        SELECT distinct store_id
                        FROM store_status;
                    '''
                    , engine)
    return store_ids

def get_store_report_file(report_id):
    """ copy csv query from the store_report table """
    conn = None
    try:
        # read database configuration
        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            host = config.hostname,
            dbname = config.database,
            user = config.username,
            password = config.pwd,
            port = config.port_id
        )
        # create a new cursor
        cur = conn.cursor()
        sql_command = r"""
            \copy store_report TO '/root/anyc/AllRepos/SSM_Backend/src/res/res.csv' DELIMITER ',' CSV HEADER;
        """


        # execute the copy statement
        # cur.execute("COPY store_report TO '/root/anyc/AllRepos/SSM_Backend/src/res/resl.csv' DELIMITER ',' CSV HEADER;")
        # cur.execute('''\copy store_report TO "/root/anyc/AllRepos/SSM_Backend/src/res/resl.csv" DELIMITER "," CSV HEADER;''')
        cur.execute(sql_command)

        # cur.execute(r"\COPY store_report TO '/root/anyc/AllRepos/SSM_Backend/src/res/resl.csv' DELIMITER ',' CSV HEADER;")
        # cur.execute("copy store_report TO '/root/anyc/AllRepos/SSM_Backend/src/res/{}.csv' DELIMITER ',' CSV HEADER;".format('small'))
        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def store_report_insert(
    store_id,
    uptime_last_hour,
    uptime_last_day,
    update_last_week,
    downtime_last_hour,
    downtime_last_day,
    downtime_last_week):
    """ Insert a new store report into the store_report table """

    insert_script = '''
        INSERT INTO store_report (store_id, uptime_last_hour, uptime_last_day, update_last_week, downtime_last_hour, downtime_last_day, downtime_last_week)
        VALUES (%s,%s,%s,%s,%s,%s,%s);
    '''

    insert_value = (store_id,
                    uptime_last_hour,
                    uptime_last_day,
                    update_last_week,
                    downtime_last_hour,
                    downtime_last_day,
                    downtime_last_week)
    conn = None
    try:
        # read database configuration
        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            host = config.hostname,
            dbname = config.database,
            user = config.username,
            password = config.pwd,
            port = config.port_id
        )
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(insert_script,insert_value)

        # commit the changes to the database
        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
        return True


class Data:
    def __init__(self, store_id, date_time_now_local = '2023-01-25 0:0:0.000000'):
        self.store_id = store_id
        self.date_time_now_local = date_time_now_local
        self.store_ids = self.get_store_ids()
        self.store_timezone = self.get_store_timezone()
        self.menu_hours = self.get_menu_hours()
        self.store_status = self.get_store_status()
        self.store_status_TimeRange_actInact = self.store_status_time_range_actIact()


    def get_store_ids(self):
        store_ids = pd.read_sql_query('''
                            SELECT distinct store_id
                            FROM store_status;
                        '''
                        , engine)
        return store_ids

    def get_store_timezone(self):
        store_timezone = pd.read_sql_query('''
                                SELECT timezone_str
                                FROM store_timezone
                                WHERE store_id = {};
                            '''
                            .format(self.store_id), engine)

        timezone_str = store_timezone['timezone_str'][0] if len(store_timezone) > 0 else 'America/Chicago'
        return timezone_str

    def get_menu_hours(self):
        menu_hours = pd.read_sql_query('''
                            SELECT day_of_week, start_time_local, end_time_local
                            FROM menu_hours
                            WHERE store_id = {}
                            ORDER by day_of_week, start_time_local;
                        '''
                        .format(self.store_id), engine)
        return menu_hours

    def get_store_status_UTC(self):
        store_status = pd.read_sql_query('''
                            SELECT status, timestamp_utc
                            FROM store_status
                            WHERE store_id = {}
                            ORDER BY timestamp_utc;
                        '''
                        .format(self.store_id), engine)
        return store_status

    def get_store_status(self):
        store_status = pd.read_sql_query('''
                            select status, timestamp_utc::timestamp at time zone '{}' as timestamp_local
                            from store_status
                            WHERE store_id = {}
                            order by timestamp_local;
                        '''
                        .format(self.store_timezone,self.store_id), engine)
        return store_status

    def store_status_time_range_actIact(self):
        store_status_TimeRange = self.store_status
        store_status_TimeRange['start_time'] = store_status_TimeRange['timestamp_local'].shift(1)
        store_status_TimeRange['end_time'] = store_status_TimeRange['timestamp_local']
        store_status_TimeRange['active_hours'] = store_status_TimeRange.apply(lambda x: x['end_time'] - x['start_time'] if x['status'] == 'active' else datetime.timedelta(hours=0), axis=1)
        store_status_TimeRange['inactive_hours'] = store_status_TimeRange.apply(lambda x: x['end_time'] - x['start_time'] if x['status'] == 'inactive' else datetime.timedelta(hours=0), axis=1)
        return store_status_TimeRange

    def get_data(self):
        return self.store_id, self.store_timezone, self.menu_hours, self.store_status, self.store_status_TimeRange_actInact
