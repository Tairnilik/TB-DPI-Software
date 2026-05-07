# md5sig fooling mode
import pydivert
import copy

def badseq(TTL):
    with pydivert.WinDivert("tcp.DstPort==443 and outbound and tcp.PayloadLength > 0") as w:
        for packet in w:
            #MD5 fake packet
            fake_packet=copy.copy(packet)
            fake_packet.tcp.options = [pydivert.models.TCPOption(kind=19, data=b'A'*16)]
            
            fake_packet.ip.ttl=TTL
            w.send(fake_packet)
            
            w.send(packet)