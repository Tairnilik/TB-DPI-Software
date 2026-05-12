# filter_l3 mode
import pydivert

def l3(typ="all"):
    if typ=="ipv4":
        l3_filter="ip"
    elif typ=="ipv6":
        l3_filter="ipv6"
    else:
        l3_filter="(ipv4 or ipv6)"
    
    pydivert_l3_filter= f"{l3_filter} and outbound and tcp.DstPort==443"
    
    try:
        with pydivert.WinDivert(pydivert_l3_filter) as w:
            for packet in w:
                if packet.ipv4:
                    print("ipv4 detected")
                    pass
                elif packet.ipv6:
                    print("ipv6 detected")
                    pass
                    
                w.send(packet)
    except Exception as e:
        print(f"Error: {e}")    

# usage
# l3("ipv6")