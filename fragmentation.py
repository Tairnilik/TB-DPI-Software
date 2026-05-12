# Fragmentation desync mode
import pydivert
import argparse
from netaddr import IPSet, IPAddress
import datetime
import copy

#IPSET
print("ipset loading")
ipset=IPSet()
with open("ipset/ipset.txt", "r", encoding="utf-8") as file:
    ipset = IPSet(line.strip() for line in file if line.strip())
print("Succesfuly loaded")

parser = argparse.ArgumentParser(description="TB-Software Network Filter")
parser.add_argument("--split-mode", type=str, choices=["split", "disorder"], help="fragmentation mode")
parser.add_argument("--split-pos", type=int, default=2, help="split position")
parser.add_argument("--mark", type=int, default=1337, help="Safety")
args = parser.parse_args()

def frag():
    # Capture
    print(f"Packet capture started at: {datetime.datetime.now()}", flush=True)
    try:
        with pydivert.WinDivert(f"tcp.DstPort==443 and outbound") as w:
            for packet in w:
                if packet.tcp.window_size == args.mark or len(packet.payload) == 0:
                        w.send(packet)
                        continue

                if IPAddress(packet.dst_addr) not in ipset:
                    w.send(packet)
                    continue
                
                if IPAddress(packet.dst_addr) in ipset:
                    if args.split_mode == "split":
                        if len(packet.payload) > args.split_pos:
                            part1 = copy.copy(packet)
                            part1.payload = packet.payload[:args.split_pos]
                
                            part2 = copy.copy(packet)
                            part2.payload = packet.payload[args.split_pos:]
                
                            part2.tcp.seq_num += len(part1.payload)
                        
                            part1.tcp.window_size = args.mark
                            part2.tcp.window_size = args.mark
                        
                            w.send(part1)
                            w.send(part2)
                            print("Packet was splitted")
                            continue
                    elif args.split_mode == "disorder":
                        if len(packet.payload) > args.split_pos:
                            part1 = copy.copy(packet)
                            part1.payload = packet.payload[:args.split_pos]
                
                            part2 = copy.copy(packet)
                            part2.payload = packet.payload[args.split_pos:]
                
                            part2.tcp.seq_num += len(part1.payload)
                            
                            part1.tcp.window_size = args.mark
                            part2.tcp.window_size = args.mark
                        
                            w.send(part2)
                            w.send(part1)
                            print("Packet was disordered")
                            continue
                            
                w.send(packet)
    except Exception as e:
        print(f"Error: {e}")
        
if __name__=="__main__":
    frag()