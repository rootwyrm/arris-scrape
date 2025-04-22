from .outputter import Outputter
from ..targets.arris_modem import DownstreamItem, UpstreamItem

class PrinterOutputter(Outputter):
    """
    Prints items to the screen.
    """
    def reset(self):
        """Reset state - nothing to do for printer"""
        pass

    def output(self, items):
        """
        Print downstream and upstream items in a readable format
        
        Args:
            items ([DownstreamItem], [UpstreamItem]): Tuple of downstream and upstream items
        """
        # Add detailed debug output
        print("\nDEBUG: Modem Response Details")
        print(f"DEBUG: Type: {type(items)}")
        print(f"DEBUG: Raw content: {repr(items)}")
        if isinstance(items, (list, tuple)):
            print(f"DEBUG: Length: {len(items)}")
            for i, item in enumerate(items):
                print(f"DEBUG: Item {i}: Type={type(item)}, Value={repr(item)}")
            print(f"DEBUG: Response structure: {type(items).__name__}[{', '.join(str(type(x).__name__) for x in items)}]")

        # Handle empty response
        if not items:
            print(f"\nERROR: Empty response from modem")
            print(f"Response type: {type(items)}")
            print(f"Response value: {repr(items)}")
            return
            
        # Handle string response (usually error or credential token)
        if isinstance(items, str):
            print(f"\nERROR: Received string instead of channel data")
            print(f"Length: {len(items)}")
            print(f"Content: {repr(items)}")
            return

        # Split items into downstream and upstream lists
        downstream_items = [item for item in items if isinstance(item, DownstreamItem)]
        upstream_items = [item for item in items if isinstance(item, UpstreamItem)]

        print("\n=== Downstream Channels ===")
        if downstream_items:
            for item in downstream_items:
                print(f"Channel {item.downstream_id}:")
                print(f"  Status: {item.lock_status}")
                print(f"  Modulation: {item.modulation}")
                print(f"  Frequency: {item.freq} Hz")
                print(f"  Power: {item.power} dBmV")
                print(f"  SNR: {item.snr} dB")
                print(f"  Corrected: {item.correcteds}")
                print(f"  Uncorrectables: {item.uncorrectables}")
                print("")
        else:
            print("No downstream channels found")

        print("\n=== Upstream Channels ===")
        if upstream_items:
            for item in upstream_items:
                print(f"Channel {item.upstream_id}:")
                print(f"  Status: {item.lock_status}")
                print(f"  Modulation: {item.modulation}")
                print(f"  Frequency: {item.freq} Hz")
                print(f"  Power: {item.power} dBmV")
                print("")
        else:
            print("No upstream channels found")  