from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from .outputter import Outputter

class InfluxDBOutputter(Outputter):
    """Outputs items to InfluxDB"""
    def __init__(self, config):
        """Initialize with InfluxDB configuration"""
        # Initialize members to None first
        self.client = None
        self.write_api = None
        
        # Store connection parameters
        self.url = f"http://{config['host']}:{config['port']}"
        self.org = config['org']
        self.bucket = config['bucket']
        self.verify_ssl = config.get('verify_ssl', True)
        self.token = config.get('token')
        self.username = config.get('username')
        self.password = config.get('password')
        
        # Create initial connection
        self._setup()

    def _setup(self):
        """Setup InfluxDB client connection"""
        # Close existing client if any
        if hasattr(self, 'client') and self.client is not None:
            try:
                if hasattr(self, 'write_api') and self.write_api is not None:
                    self.write_api.close()
                self.client.close()
            except:
                pass

        # Setup client arguments
        client_args = {
            'url': self.url,
            'org': self.org,
            'verify_ssl': self.verify_ssl
        }
        
        if self.token:
            client_args['token'] = self.token
        else:
            client_args['username'] = self.username
            client_args['password'] = self.password

        # Create new client and write API
        self.client = InfluxDBClient(**client_args)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def output(self, items):
        """Write items to InfluxDB"""
        if not items:
            return
            
        try:
            points = list(map(lambda i: i.output_for_influxdb(), items))
            self.write_api.write(
                bucket=self.bucket,
                org=self.org,
                record=points
            )
        except Exception as e:
            print(f"Failed to write to InfluxDB: {e}")
            raise

    def reset(self):
        """Reset connection if needed"""
        self._setup()

    def __del__(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'write_api') and self.write_api is not None:
                self.write_api.close()
            if hasattr(self, 'client') and self.client is not None:
                self.client.close()
        except:
            pass