# badsum fooling mode
import pydivert

def badsum():
    with pydivert.WinDivert("tcp.DstPort==443 and outbound and tcp.PayloadLength > 0") as w:
        for packet in w:
            packet.tcp.cksum=0
        
            w.send(packet)