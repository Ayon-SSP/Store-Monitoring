CREATE DATABASE store_monitoring;


DROP TABLE store_status;
DROP TABLE store_business_hours;
DROP TABLE store_timezone;

TRUNCATE store_status;

CREATE TABLE IF NOT EXISTS store_status (
    store_id BIGINT NOT NULL,
    status VARCHAR(10) NOT NULL,
    timestamp_utc TIMESTAMP NOT NULL
    -- PRIMARY KEY (store_id, timestamp_utc)
);


INSERT INTO store_status (store_id, status, timestamp_utc)
VALUES
(841954000000000000, 'active', '2023-01-22 12:09:39.388884+00')


CREATE TABLE IF NOT EXISTS menu_hours (
    store_id BIGINT NOT NULL,
    day_of_week INTEGER NOT NULL,
    start_time_local TIME NOT NULL,
    end_time_local TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS store_timezone (
    store_id BIGINT NOT NULL,
    timezone_str VARCHAR(50) NOT NULL,
    PRIMARY KEY (store_id)
);





SELECT *
FROM store_status
WHERE status = 'active'
LIMIT 5;

SELECT * FROM store_status WHERE status = 'active' LIMIT 5;

select count(*) from store_status where status = 'active';

-- to get all the stores that are with store_id = 1217505942626861817
select * from store_status where store_id = 1217505942626861817;

-- to get all the stores that are with store_id = 1217505942626861817 and status = 'active'
select * from store_status where store_id = 1217505942626861817 and status = 'active';



-- to get all the stores that are with store_id = 1472400125885919118 from menu_hours table
select * from menu_hours where store_id = 1472400125885919118;
-- now sort by dat of week and start time
select * from menu_hours where store_id = 1472400125885919118 order by day_of_week, start_time_local;


select status, timestamp_utc from store_status where store_id = 8444136742823051302 order by timestamp_utc desc limit 1;

-- display the status and timestamp_utc + 5 hours from store_status table for store_id = 8444136742823051302 and sort by timestamp_utc timestamp_utc + 5 hours
select status, timestamp_utc + interval '5 hours' as timestamp_utc_plus_5 from store_status where store_id = 8444136742823051302 order by timestamp_utc_plus_5;
-- Now above query with 1 hour 30 minutes interval
select status, timestamp_utc + interval '1 hour 30 minutes' as timestamp_utc_plus_1_30 from store_status where store_id = 8444136742823051302 order by timestamp_utc_plus_1_30;


-- and now show only the data of date 2021-01-19
select status, timestamp_utc + interval '5 hours' as timestamp_utc_plus_5 from store_status where store_id = 8444136742823051302 and timestamp_utc + interval '5 hours' >= '2021-01-19 00:00:00' and timestamp_utc + interval '5 hours' < '2021-01-20 00:00:00' order by timestamp_utc_plus_5;
-- Now the interval is 1 hour 30 minutes
select status, timestamp_utc + interval '1 hour 30 minutes' as timestamp_utc_plus_1_30 from store_status where store_id = 8444136742823051302 and timestamp_utc + interval '1 hour 30 minutes' >= '2021-01-19 00:00:00' and timestamp_utc + interval '1 hour 30 minutes' < '2021-01-20 00:00:00' order by timestamp_utc_plus_1_30;
-- Now take the interval's from the store_timezone with eg: timezone_str = 'America/New_York'


-- display all the unique store_id from store_status table
select distinct store_id from store_status;


select status, timestamp_utc + interval '5 hours' as timestamp_local
from store_status
where store_id = 8444136742823051302
order by timestamp_local;


select status, timestamp_utc + interval '5 hours' as timestamp_utc_plus_5
from store_status
where store_id = 8444136742823051302
and timestamp_utc + interval '5 hours' >= '2023-01-25 00:00:00' and timestamp_utc + interval '5 hours' < '2023-01-26 00:00:00'
order by timestamp_utc_plus_5;


-- New Query
-- take the interval from the currTime table with eg: timezone_str = 'America/New_York'and then display the time difference
select status, timestamp_utc at time zone 'America/Los_Angeles' as timestamp_local
from store_status
where store_id = 1472400125885919118
order by timestamp_local;

-- utc to given time zone
select status, timestamp_utc::timestamp at time zone 'America/Los_Angeles' as timestamp_local
from store_status
where store_id = 1472400125885919118
order by timestamp_local;

-- display the status and timestamp_utc from store_status table for store_id = 8444136742823051302 and change the timestamp_utc to local time using store_timezone table and sort by local timestamp
select status, timestamp_utc at time zone tz.timezone_str as timestamp_local from store_status ss join store_timezone tz on ss.store_id = tz.store_id where ss.store_id = 8444136742823051302 order by timestamp_local;
-- select status, timestamp_utc at time zone tz.timezone_str as timestamp_local from store_status ss join store_timezone tz on ss.store_id = tz.store_id where ss.store_id = 1217505942626861817 order by timestamp_local limit 10;

select status, timestamp_utc at time zone tz.timezone_str as timestamp_local
from store_status ss
join store_timezone tz on ss.store_id = tz.store_id
where ss.store_id = 8444136742823051302
order by timestamp_local;

\copy store_report TO '/root/anyc/AllRepos/SSM_Backend/src/res/res.csv' DELIMITER ',' CSV HEADER;