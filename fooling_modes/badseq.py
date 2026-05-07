# badseq fooling mode
import pydivert
import random

def badseq(a,b):
    with pydivert.WinDivert("tcp.DstPort==443 and outbound and tcp.PayloadLength > 0") as w:
        for packet in w:
            packet.tcp.seq_num += random.randint(a,b)
        
            w.send(packet)