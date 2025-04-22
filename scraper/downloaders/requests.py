from .downloader import Downloader
import requests
import ssl
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

class RequestsDownloader(Downloader):
    """
    Downloader subclass that uses Requests to download content.

    Raises:
        Exception: Content couldn't be downloaded successfully.

    Returns:
        string: HTML string of content.
    """
    @staticmethod
    def download(url):
        session = requests.Session()
        session.mount('https://', TLSAdapter())
        
        result = session.get(
            url,
            timeout=10,
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
         
        if result.status_code != 200:
            raise Exception("Received non-200 response.")
        else:
            print('Modem response OK')

        return result.content
