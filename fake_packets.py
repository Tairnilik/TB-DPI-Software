# Fake desync mode
import pydivert
import time
import copy
import random

#SETTINGS
repeats=int(input("The number of fake packets per request: "))
print("fake packet per request: " + str(repeats))
ttl_f_p=int(input("Enter the number TTL(Time-To-Live) of fake packets: "))
print("TTL: " + str(ttl_f_p))

#LOGIC
with pydivert.WinDivert("tcp.DstPort==443 and outbound and !windivert.is_loopback") as w:
    for packet in w:
        for i in range(repeats):
            fake_packet=copy.copy(packet)
            fake_packet.payload=random.randbytes(len(packet.payload))
            fake_packet.ip.ttl=ttl_f_p
            
            
            w.send(fake_packet)
        w.send(packet)  
        print(f"Succesfully send {repeats} fake packets")