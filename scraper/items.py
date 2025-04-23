"""
Items module.
"""
class Item():
    """
    Subclass this to represent a scraped Item.
    """
    def __init__(self, fieldDict):
        """
        Create an item by passing in a dict of fields.

        Args:
            fieldDict (dict): Dict to populate properties of the Item.
        """
        for key, val in fieldDict:
            setattr(self, key, val)

class InfluxableItem(Item):
    """
        Gives us the ability to print out InfluxableItems into
        a readable format.
    """
    def __str__(self):
        return str(self.output_for_influxdb())

    def output_for_influxdb(self):
        """
        Method that should be implemented to represent the item
        as an InfluxDB point.
        """

    @staticmethod
    def int_at_pos(val, pos=0):
        """
        Convert value to integer at given position after splitting
        
        Args:
            val: The value to convert
            pos: Position in split string (default: 0)
            default: Value to return if conversion fails (default: None)
            
        Returns:
            Integer value or default if conversion fails
        """

        if val is None:
            return 0
        try:
            parts = str(val).strip().split()
            if not parts:
                return 0
            return int(parts[pos])
        except (ValueError, IndexError):
            return 0

    @staticmethod
    def float_at_pos(val, pos = 0):
        """
        Splits a string v and converts element at position p to a float.
        """
        return float(str(val).split()[pos])
