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

        for universe in range(1,25):
            self.sender.activate_output(universe)
            self.sender[universe].destination = dest_ip



    def send(self, data):
        if type(data) is None:
            print("Warning: none data")
            return
        self.data_queue.append(data)
        if len(self.data_queue) == self.reduction_rate:

            fame_average = 256 * np.mean(self.data_queue,axis = 0) 
            frame_average = fame_average.astype(np.uint8)

            frame_average = np.tile(frame_average, 16)
            for universe in range(1,24): 
                c = universe * 510
                self.sender[universe].dmx_data = frame_average[c-510:c]
            
           
            self.sender.flush()
            self.data_queue = []

