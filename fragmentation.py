# Fragmentation desync mode
import pydivert
import time
import copy

#IPSET
with open("ipset/ipset.txt", "r", encoding="utf-8") as file:
    ipset = {line.strip() for line in file if line.strip()}


# Settings
mode_frag=input("split/disorder: ").lower().strip()
print("Fragmentation_method: " + mode_frag)
s_p=int(input("Split position: "))
print("Split position: " + str(s_p))
time.sleep(1)
# Capture
print("Packet capture is enabled")

with pydivert.WinDivert("tcp.DstPort==443 and outbound") as w:
    for packet in w:
        if mode_frag=="split":
            if len(packet.payload) > s_p:
                part1=copy.copy(packet)
                part1.payload=packet.payload[:s_p]
            
                part2=copy.copy(packet)
                part2.payload=packet.payload[s_p:]
            
                part2.tcp.seq_num += len(part1.payload)
                    
                w.send(part1)
                w.send(part2)
                print("Packet was splitted")
                continue
        elif mode_frag=="disorder":
            if len(packet.payload) > s_p:
                part1=copy.copy(packet)
                part1.payload=packet.payload[:s_p]
            
                part2=copy.copy(packet)
                part2.payload=packet.payload[s_p:]
            
                part2.tcp.seq_num += len(part1.payload)
                    
                w.send(part2)
                w.send(part1)
                print("Packet was disordered")
                continue
        w.send(packet)