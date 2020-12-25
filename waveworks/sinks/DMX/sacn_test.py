import time
import sacn
import numpy as np
from pprint import pprint


# sender.manual_flush = False # keep maunal flush off as long as possible, because if it is on, the automatic
# sending of packets is turned off and that is not recommended
# sender.stop() # stop sending out


class SacnSink(object):
    """
    docstring
    """


    def __init__(self,dest_ip = "localhost",reduction_rate = 3): 
        self.reduction_rate = reduction_rate
        self.data_queue = []


        self.sender = sacn.sACNsender(fps=40)
        self.sender.start()
        self.sender.manual_flush = True

        self.sender.activate_output(1)
        self.sender[1].destination = dest_ip



    def send(self, data):
        if type(data) is None:
            print("Warning: none data")
            return
        self.data_queue.append(data)
        if len(self.data_queue) == self.reduction_rate:

            fame_average = 256 * np.mean(self.data_queue,axis = 0) 
            frame_average = fame_average.astype(np.uint8)
            
            self.sender[1].dmx_data = frame_average
            self.sender.flush()
            self.data_queue = []

