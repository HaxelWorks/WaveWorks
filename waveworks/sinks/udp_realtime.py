import numpy as np
import numba 

import socket

from scipy.ndimage.measurements import labeled_comprehension







class WledSink():
    """
        Value	Description	Max. LEDs
    1	WARLS	255
    2	DRGB	490
    3	DRGBW	367
    4	DNRGB	489/packet
    0	WLED Notifier	-


    https://github.com/Aircoookie/WLED/wiki/UDP-Realtime-Control
    """
    

    #configbytes [protocol,timeout seconds]
    DRGB = np.array([2,5],np.uint8)
    DNRGB = np.array([4,5],np.uint8) 


    def __init__(self,dest_ip = "localhost",reduction_rate = 2,colors_per_led = 3,protocol="DNRGB",leds_per_packet =144): 
        self.reduction_rate = reduction_rate
        
        self.dest_ip = dest_ip
        self.data_queue = []
        self.prev_queue = self.data_queue
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
        

        self.packetizer = WledSink.packetizer_factory(protocol,colors_per_led,leds_per_packet)

    @staticmethod
    def packetizer_factory(protocol,colors_per_led,leds_per_packet):
        if protocol == "DNRGB":
            assert leds_per_packet <= 489, "max leds per packet for DNRGB is 489"
            config_bytes = WledSink.DNRGB
            # @staticmethod
            # @numba.njit("float64[:,:](float64[:,:],float64[:,:])")      
            def DNRGB(leddata):    
                """
                DNRGB: DRGB, but with 2 additional bytes that signify the starting LED index. This allows for more than 490 LEDs in realtime mode by sending multiple packets.

                Byte	Description
                2	Start index high byte
                3	Start index low byte
                4 + n*3	Red Value
                5 + n*3	Green Value
                6 + n*3	Blue Value
                """

                # li//256,li%256
                leddata *= 255
                leddata = leddata.astype(np.uint8)
                # leddata = leddata.repeat(5,axis=0)
                return [np.concatenate((config_bytes,np.array([(144*index)//256,(144*index)%256],np.uint8),packet.flatten()))for index,packet in enumerate(np.split(leddata,len(leddata)//leds_per_packet))]

            
        return DNRGB


    def send(self,data):
        self.data_queue.append(data)
        if len(self.data_queue) == self.reduction_rate:

            merged = np.mean(self.data_queue,axis=0)    
            
            for packet in self.packetizer(merged):
                self.sock.sendto(packet, (self.dest_ip, 21324))

            
            self.data_queue.clear()






                