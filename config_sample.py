"""
Parameters for the modem scraper.
"""
scraper_config = {
    'modem_model': '', # POPULATE MODEM MODEL HERE
    'modem_url': '', # POPULATE MODEM URL HERE
    'max_retries': 5,
    'poll_interval_seconds': 30,
    'outputter': 'influxdb',    # Output to influxdb or print
    'cm8200_username': '',      # Only set if using a CM8200 with authentication
    'cm8200_password': ''       # Only set if using a CM8200 with authentication
}

"""
Parameters for InfluxDBClient. See influxdb.InfluxDBClient for all options.
"""
influx_config = {
    'host': '', # POPULATE INFLUX_DB HOST HERE
    'port': 8086,
    'database': 'modem'
}
