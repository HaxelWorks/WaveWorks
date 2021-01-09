#%%
import numba
import numpy as np
from waveworks import N_LED

#%%
@numba.njit("float64[:,:](float64,float64[:])")
def colorize(hue, arr):
    s = 1
    out = np.empty(shape=(N_LED, 3))
    i = int(hue * 6.0)
    f = (hue * 6.0) - i
    p = 0
    for index in range(N_LED):
        val = arr[index]
        q = val * (1.0 - s * f)
        t = val * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            out[index] = [val, t, p]
        if i == 1:
            out[index] = [q, val, p]
        if i == 2:
            out[index] = [p, val, t]
        if i == 3:
            out[index] = [p, q, val]
        if i == 4:
            out[index] = [t, p, val]
        if i == 5:
            out[index] = [val, p, q]
    return out


@numba.njit("float64[:,:](float64,float64[:])")
def colorize2(hue, arr):

    s = 1
    out = np.empty(shape=(N_LED, 3))
    i = int(hue * 6.0)
    f = (hue * 6.0) - i
    p = 0
    for index in range(N_LED):
        val = arr[index]
        q = val * (1.0 - s * f)
        t = val * (1.0 - s * (1.0 - f))
        i = i % 6

        t ** 8
        p ** 2.5

        if i == 0:
            out[index] = [val, t, p]
        if i == 1:
            out[index] = [q, val, p]
        if i == 2:
            out[index] = [p, val, t]
        if i == 3:
            out[index] = [p, q, val]
        if i == 4:
            out[index] = [t, p, val]
        if i == 5:
            out[index] = [val, p, q]
    return out


# TODO convert this function from glsl to python
@numba.njit("float64[:,:](float64,float64[:])")
def hueShift(hueAdjust, arr):

    kRGBToYPrime = np.array([0.299, 0.587, 0.114])
    kRGBToI = np.array([0.596, -0.275, -0.321])
    kRGBToQ = np.array([0.212, -0.523, 0.311])

    kYIQToR = np.array([1.0, 0.956, 0.621])
    kYIQToG = np.array([1.0, -0.272, -0.647])
    kYIQToB = np.array([1.0, -1.107, 1.704])

    out = np.zeros(shape=(N_LED, 3))
    for i in range(arr.shape[0]):

        color = np.array([arr[i],arr[i]**8,arr[i]**2.5])
        YPrime = np.dot(color, kRGBToYPrime)
        I = np.dot(color, kRGBToI)
        Q = np.dot(color, kRGBToQ)
        hue = np.arctan(Q/I)
        chroma = np.sqrt(I * I + Q * Q)

        hue += hueAdjust

        Q = chroma * np.sin(hue)
        I = chroma * np.cos(hue)

        yIQ = np.array([YPrime, I, Q])

        R = np.dot(yIQ, kYIQToR)
        G = np.dot(yIQ, kYIQToG)
        B = np.dot(yIQ, kYIQToB)

        # np.max(np.min(1.0,R),0.0)
        # np.max(np.min(1.0,G),0.0)
        # np.max(np.min(1.0,B),0.0)
        out[i] = [R,G,B]
        
    
    return np.fmin(np.fmax(out,0.0),1.0)