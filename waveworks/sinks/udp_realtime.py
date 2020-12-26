import numpy as np
import socket

from numpy.core.defchararray import array
from waveworks import N_LED


class WledSink():
    configbytes = np.array([2,5],np.uint8)

    def __init__(self,dest_ip = "localhost"): 
        self.dest_ip = dest_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
        print("vieze vieze kak echt waar het meurt!")

    def send(self,arr):
        arr *= 256
        arr = arr.astype(np.uint8)
        
        arr = arr.flatten()
        arr = np.concatenate([WledSink.configbytes,arr])

        self.sock.sendto(arr, (self.dest_ip, 21324))
        
