from .downloader import Downloader
import requests
import ssl
import base64
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class TLSAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.set_ciphers('DEFAULT')
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        super(TLSAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context
        )

class AuthenticatedDownloader(Downloader):
    """
    Downloader subclass that handles authentication for CM8200.

    Raises:
        Exception: Content couldn't be downloaded successfully.

    Returns:
        string: HTML string of content.
    """
    def __init__(self, username, password):
        """Initialize with credentials"""
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.mount('https://', TLSAdapter())
        self.auth_token = None

    def authenticate(self, base_url):
        """Authenticate with the modem and get token"""
        credentials = f"{self.username}:{self.password}"
        self.auth_token = base64.b64encode(credentials.encode()).decode()

        self.status_url = f"{base_url}/cmconnectionstatus.html"
        
        login_url = f"{base_url}/login.html"
        response = self.session.get(
            login_url,
            timeout=10,
            verify=False,
            headers={
                'Authorization': f'Basic {self.auth_token}',
                'User-Agent': 'Mozilla/5.0'
            }
        )
        
        if response.status_code != 200:
            raise Exception("Authentication failed")
        
        print('Authentication successful')
        return self.auth_token

    def download(self, url):
        """Download content with authentication"""
        if not self.auth_token:
            self.authenticate(url)
            
        result = self.session.get(
            self.status_url,
            timeout=10,
            verify=False,
            headers={
                'Authorization': f'Basic {self.auth_token}',
                'User-Agent': 'Mozilla/5.0'
            }
        )
         
        if result.status_code != 200:
            raise Exception(f"Received non-200 response: {result.status_code}")
        else:
            print('Modem response OK')

        return result.content