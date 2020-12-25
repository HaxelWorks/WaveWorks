import numpy as np
import socket

from numpy.core.defchararray import array
from waveworks import N_LED
INDICHES = np.array([x for x in range(N_LED)],dtype=np.uint8)

class WledSink():
    
    MAX_PIXELS_PER_PACKET = 126

    def __init__(self,dest_ip = "localhost"): 
        self.dest_ip = dest_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    

    def send(self,arr):
        arr *= 256
        arr = arr.astype(np.uint8)
        arr = np.insert(arr,0, INDICHES, 1)
        arr = arr.flatten()
        self.sock.sendto(arr[:288], (self.dest_ip, 7777))
        self.sock.sendto(arr[288:], (self.dest_ip, 7777))