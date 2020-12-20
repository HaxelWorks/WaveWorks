# %% imports
from time import sleep,perf_counter
import soundcard as sc
import numpy as np


UPS = 120 #updates per second
# BLOCKSIZE = 4096
SAMPLERATE = 48000
FFT_WINDOW_SIZE = 16384//2
OUTPUT_BUFFER_SIZE =FFT_WINDOW_SIZE
default_speaker_name = sc.default_speaker().name
# %%

input_audio_device = sc.get_microphone(default_speaker_name, include_loopback=True)



def buffer(buffer,data):
     if len(data)!=0:
                output_buffer = np.roll(output_buffer,-len(data))
                output_buffer[-len(data):] = data
                # output_buffer.reshape(-1, int(OUTPUT_BUFFER_SIZE/256))

# %%

def audio_generator():
    output_buffer = np.zeros(OUTPUT_BUFFER_SIZE,dtype = np.float32)
    
    window = int(SAMPLERATE / UPS)
    counter = 0
    acc_time = 0
    with input_audio_device.recorder(samplerate=SAMPLERATE) as mic:
        while True:
            counter+=1
            p = perf_counter()
            audio_fragment = mic.record(window).mean(axis=1)
            acc_time += perf_counter() - p
            if counter % 100 == 0:
                print((acc_time/100)*UPS)
                acc_time=0
            
            # print(audio_fragment.shape)
            # print((audio_fragment:= audio_fragment.mean(axis=1)).shape)
            if len(audio_fragment)!=0:
                output_buffer = np.roll(output_buffer,-len(audio_fragment))
                output_buffer[-len(audio_fragment):] = audio_fragment
                # output_buffer.reshape(-1, int(OUTPUT_BUFFER_SIZE/256))
            yield output_buffer

