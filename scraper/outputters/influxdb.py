from influxdb_client import InfluxDBClient
from .outputter import Outputter
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBOutputter:
    """Outputs items to InfluxDB"""
    def __init__(self, config):
        """Initialize with InfluxDB configuration"""
        # Build URL from host/port
        url = f"http://{config['host']}:{config['port']}"
        
        # Build auth args based on config
        client_args = {
            'url': url,
            'org': config['org'],
            'verify_ssl': config.get('verify_ssl', True)
        }

        # Use token auth if provided, otherwise username/password
        if 'token' in config:
            client_args['token'] = config['token']
        else:
            client_args['username'] = config['username']
            client_args['password'] = config['password']

        self.client = InfluxDBClient(**client_args)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = config['bucket']
        self.org = config['org']

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def _setup(self):
        if self.client is not None:
            self.client.close()
        self.client = InfluxDBClient(**self.config)
        self.client.create_database(self.config['database'])

    def reset(self):
        self._setup()

    def output(self, items):
        points = list(map(lambda i: i.output_for_influxdb(), items))
        self.client.write_points(points)
