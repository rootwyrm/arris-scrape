from .outputter import Outputter

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
        downstream_items, upstream_items = items

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
                print(f"  Type: {item.channel_type}")
                print(f"  Frequency: {item.freq} Hz")
                print(f"  Width: {item.width} Hz") 
                print(f"  Power: {item.power} dBmV")
                print("")
        else:
            print("No upstream channels found")