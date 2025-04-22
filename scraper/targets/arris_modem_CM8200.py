"""
Arris modem module for CM8200 model.
"""
from bs4 import BeautifulSoup
from .arris_modem import ArrisModem, UpstreamItem, DownstreamItem

class ArrisModemCM8200(ArrisModem):
    """
    ArrisModem subclass that represents an Arris modem model CM8200
    """

    def get_downstream_items(self, html_string):
        """
        Function to convert an HTML string to a list of DownstreamItems.

        Args:
            html_string (string): HTML from modem status page

        Returns:
            [DownstreamItem]: List of DownstreamItems
        """
        soup = BeautifulSoup(html_string, 'html5lib')
        
        # key order must match the table column layout
        keys = [
            'downstream_id',
            'lock_status', 
            'modulation',
            'freq',
            'power',
            'snr',
            'correcteds',
            'uncorrectables',
            'octets'
        ]
        
        items = []
        
        # Find the Downstream Bonded Channels table
        downstream_table = None
        for table in soup.find_all("table", class_="simpleTable"):
            if "Downstream Bonded Channels" in table.text:
                downstream_table = table
                break
                
        if not downstream_table:
            return items
            
        # Skip header rows
        for table_row in downstream_table.find_all("tr")[2:]:
            cells = table_row.find_all('td')
            if not cells:
                continue
                
            channel = cells[0].text.strip()
            lock_status = cells[1].text.strip()
            modulation = cells[2].text.strip()
            frequency = cells[3].text.replace(" Hz", "").strip()
            power = cells[4].text.replace(" dBmV", "").strip()
            snr = cells[5].text.replace(" dB", "").strip()
            corrected = cells[6].text.strip()
            uncorrectables = cells[7].text.strip()
            octets = "0"

            values = (channel, lock_status, modulation, frequency, power, snr, corrected, uncorrectables, octets)
            zipped = dict(zip(keys, values))
            items.append(DownstreamItem(zipped.items()))
            
        return items

    def get_upstream_items(self, html_string):
        """
        Function to convert an HTML string to a list of UpstreamItems.

        Args:
            html_string (string): HTML from modem status page

        Returns:
            [UpstreamItem]: List of UpstreamItems
        """
        soup = BeautifulSoup(html_string, 'html5lib')

        # key order must match the table column layout
        keys = [
            'upstream_id',
            'ucid',
            'lock_status',
            'channel_type',
            'freq',
            'width',
            'power'
        ]

        items = []

        # Find the Upstream Bonded Channels table
        upstream_table = None
        for table in soup.find_all("table", class_="simpleTable"):
            if "Upstream Bonded Channels" in table.text:
                upstream_table = table
                break
                
        if not upstream_table:
            return items

        # Skip header rows
        for table_row in upstream_table.find_all("tr")[2:]:
            cells = table_row.find_all('td')
            if not cells:
                continue
                
            channel = cells[0].text.strip()
            ucid = cells[1].text.strip()
            lock_status = cells[2].text.strip()
            channel_type = cells[3].text.strip()
            freq = cells[4].text.replace(" Hz", "").strip()
            width = cells[5].text.replace(" Hz", "").strip()
            power = cells[6].text.replace(" dBmV", "").strip()

            values = (channel, ucid, lock_status, channel_type, freq, width, power)
            zipped = dict(zip(keys, values))
            items.append(UpstreamItem(zipped.items()))

        return items