# Monitoring_Flask-RestAPI-pgadmin-sql [`📺 Video Link`](https://youtu.be/n2GgGz60j1A)

This project aims to help restaurant owners monitor the uptime of their online stores during business hours. The backend APIs provided in this project will allow restaurant owners to view reports on past store inactivity.
# 🎯 Block Model
                                                 User Request
                                                      |
                                                      ↓
                  +---------------------------------------------------------------------------+
                  |                 (HTTP request)   [REST API with Flask]                    |
                  +---------------------------------------------------------------------------+
                         |                               |   ↑                ↑
                         |                               |   |                |      File Download [Return Report or CSV File]
                         |                               |   |            +----------------------------+
                         ↓                               |   |            |    /download/<report_id>   |
         +----------------------------+                  |   | Running    +----------------------------+
         |  /trigger_report Endpoint  |                  |   |                ↑                    ↑
         +----------------------------+                  |   |                | Complete           |
                          |                              ↓   |                |                    |
                          |                          +---------------------------------+           |
                          ↓                          |     /get_report Endpoint        |           |
               +-------------------------+           +---------------------------------+           |
               |  Generate Report U_id   |                 ↑                                       |
               +-------------------------+                 |                                       |
                                       ↓                   |                                       |
                                    +---------------------------------+                            |
                                    |       report_status.json        |                            |
                                    +---------------------------------+                            |
                                                     |                                          +---------------------------------+
                                                     |                                          |           <U_id>.csv            |
                                                     | trigger                                  +---------------------------------+
                                                     |                                                                      ↑
                                                     ↓                                                       store_report   |
                               +---------------------------------------------------------------+                            |
                               |            Data Storage and Manipulation (CRUD)               |                            |
                               +---------------------------------------------------------------+                            |
                               |    logic for computing the hours overlap and uptime/downtime  |                            |
                               |    psql dealing  with Time typecasting                        |                            |
                               |    User Data Management and Storage                           |                            |
                               |    Data preprocessing                                         |                            |
                               |    df -> Database                                             |                            |
                               +---------------------------------------------------------------+                            |
                                                 ↑                             |   <--(psycopg2)-- [Preprocessing]          |
                                                 |                             |                                            |
                                              timezone_str                 store_report                                     |
                                              menu_hours                       |                                            |
                                              store_status                     |                                            |
                                                 |                             ↓                                            |
                                                 |                                                                           |
                                                                                                                 +--------------------------+
                    [Preprocessing]---(SQLAlchemy ORM)--->[PostgreSQL Database]----------------------------------|         df.to_csv        |
                                                                                                                 +--------------------------+

```css
-> Frontend NaT
-> Backend server takes care of
       - User DATA management
       - Data storage
       - CSV -> Database
       - Data manipulation(CRUD)
       - logic for computing the hours overlap and uptime/downtime
       - psql dealing  with Time typecasting
       - Data preprocessing
       - File download

-> Flask API is used to manage users, files and data manipulation.
```
