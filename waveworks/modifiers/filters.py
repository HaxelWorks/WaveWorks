import numpy as np
from scipy.signal import savgol_filter as savgol
from scipy.ndimage import gaussian_filter1d, convolve1d
from scipy.signal.windows import gaussian

def integral(multiplier=1):

    samples = yield
    yield samples
    while True:
        newsamp = yield

        samples = (newsamp * multiplier + samples * (1 - multiplier)).clip(0, 1)

        yield samples

def smooth1(a):
    samples = yield
    yield samples
    while True:
        newsamp = yield
        samples = newsamp*a+samples*(1-a)
        yield samples


def savgol_integral(multiplier=1):
    samples = yield
    yield samples
    while True:
        newsamp = yield

        samples = newsamp * multiplier + samples * (1 - multiplier)
        samples = savgol(samples, 11, 3).clip(0, 1)

        yield samples

window = gaussian(11*4,0.65)
def diffusion(outward_pressure=1 ):
    arr = yield
    yield arr
    while True:
        fresh_samples = yield
        arr = convolve1d(fresh_samples*0.5+arr,window,origin=-1).clip(0, 2)*0.5
        yield arr