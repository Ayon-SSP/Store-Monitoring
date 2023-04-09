"""Configuration file for the application"""

# rename this file to Configuration.py and fill in the values

hostname = '<localhost>'
database = '<db-name>'
username = '<postgres>'
pwd = '<password>'
port_id = 5432


#! databasetype://username:password@hostname:port/database
dbLink = 'postgresql://'+username+':'+pwd+'@'+hostname+':'+str(port_id)+'/'+database
