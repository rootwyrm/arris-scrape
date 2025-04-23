from .downloader import Downloader
import time
import requests
import requests.exceptions
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
    """Downloader subclass that handles authentication for CM8200."""
    def __init__(self, username, password):
        """Initialize with credentials"""
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.mount('https://', TLSAdapter())
        self.auth_token = None
        self.status_url = None
        self.credential_token = None

    def authenticate(self, base_url):
        """Authenticate with the modem using the same flow as the web UI"""
        credentials = f"{self.username}:{self.password}"
        self.auth_token = base64.b64encode(credentials.encode()).decode()
        self.status_url = f"{base_url}/cmconnectionstatus.html"
        
        # First auth request to get credential token
        auth_url = f"{self.status_url}?{self.auth_token}"
        
        response = self.session.get(
            auth_url,
            timeout=10,
            verify=False,
            headers={
                'Authorization': f'Basic {self.auth_token}',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Accept-Language': 'en-US,en;q=0.9'
            },
            cookies={
                'HttpOnly': 'true',
                'Secure': 'true'
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.status_code}\n Check username and password in config file.")

        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.status_code}")

        # Store credential token, stripping any HTML
        content = response.content.decode('utf-8')
        if '<!DOCTYPE' in content:
            raise Exception("Received login page instead of credential token")
            
        self.credential_token = content.strip()
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
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin', 
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Accept-Language': 'en-US,en;q=0.9'
            },
            cookies={
                'HttpOnly': 'true',
                'Secure': 'true',
                'credential': self.credential_token
            }
        )

        if result.status_code != 200:
            raise Exception(f"Received non-200 response: {result.status_code}")
            
        try:
            return result.content.decode('utf-8')
        except UnicodeDecodeError:
            return result.content

    def logout(self, base_url):
        """Logout from the modem"""
        ## Uses a timestamp to prevent caching
        timestamp = int(time.time() * 1000)
        logout_url = f"{base_url}/logout.html?_={timestamp}"
        
        try:
            self.session.get(
                logout_url,
                timeout=10,
                verify=False,
                headers={
                    'Authorization': f'Basic {self.auth_token}',
                    'User-Agent': 'Mozilla/5.0',
                    'Accept': '*/*',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
            # Connection reset is expected behavior on logout
            pass
        except Exception as e:
            print(f"WARNING: Unexpected error during logout: {e}")
        finally:
            # Clear session data regardless of outcome
            self.auth_token = None
            self.credential_token = None
            self.session.cookies.clear()