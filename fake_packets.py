# Fake desync mode
import pydivert
import argparse
from netaddr import IPSet, IPAddress
import datetime
import copy
import random

#ipset
print("ipset loading")
ipset=IPSet()
with open("ipset/ipset.txt", "r", encoding="utf-8") as file:
    ipset = IPSet(line.strip() for line in file if line.strip())
print("Succesfuly loaded")

parser = argparse.ArgumentParser(description="TB-Software Network Filter")
parser.add_argument("--repeats", type=int, default=6, help="send fake packets N times")
parser.add_argument("--ttl-f", type=int, default=5, help="Time-To-Live for fake packets")
parser.add_argument("--mark", type=int, default=1337, help="Safety")
args = parser.parse_args()

def fake_p():
    #LOGIC
    print(f"Packet capture started at: {datetime.datetime.now()}", flush=True)
    try:
        with pydivert.WinDivert("tcp.DstPort==443 and outbound") as w:
            for packet in w:
                if packet.tcp.window_size == args.mark or len(packet.payload) == 0:
                        w.send(packet)
                        continue
            
                if IPAddress(packet.dst_addr) in ipset:
                    for i in range(args.repeats):
                        fake_packet=copy.copy(packet)
                        fake_packet.tcp.window_size=args.mark
                        if len(fake_packet.payload)>=3:
                            fake_packet.payload = b'\x16\x03\x01' + random.randbytes(len(packet.payload)-3)
                        else:
                            orig_len = len(packet.payload)
                            fake_packet.payload = (b'\x16\x03\x01' * 2)[:orig_len]
                        fake_packet.ip.ttl=args.ttl_f
            
                        w.send(fake_packet)
                try:
                    w.send(packet)
                except:
                    pass
    except Exception as e:
        print(f"Error: {e}")
 
if __name__=="__main__":
    fake_p()