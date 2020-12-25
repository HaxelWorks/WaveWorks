#%%
import numba
import numpy as np
from waveworks import N_LED
#%% 
@numba.njit("float64[:,:](float64,float64[:])")
def colorize(hue,arr):
    s = 1
    out = np.empty(shape = (N_LED,3))
    i = int(hue*6.0) 
    f = (hue*6.0) - i
    p = 0
    for index in range(N_LED):
        val = arr[index]
        q = val*(1.0 - s*f)
        t = val*(1.0 - s*(1.0-f))
        i = i%6
        if i == 0:
            out[index] = [ val, t, p]
        if i == 1:
            out[index] = [ q, val, p]
        if i == 2:
            out[index] = [ p, val, t]
        if i == 3:
            out[index] = [ p, q, val]
        if i == 4:
            out[index] = [ t, p, val]
        if i == 5:
            out[index] = [ val, p, q]
    return out

@numba.njit("float64[:,:](float64,float64[:])")
def colorize2(hue,arr):

    s = 1
    out = np.empty(shape = (N_LED,3))
    i = int(hue*6.0) 
    f = (hue*6.0) - i
    p = 0
    for index in range(N_LED):
        val = arr[index]
        q = val*(1.0 - s*f)
        t = val*(1.0 - s*(1.0-f))
        i = i%6

        t ** 8
        p ** 2.5

        
        if i == 0:
            out[index] = [ val, t, p]
        if i == 1:
            out[index] = [ q, val, p]
        if i == 2:
            out[index] = [ p, val, t]
        if i == 3:
            out[index] = [ p, q, val]
        if i == 4:
            out[index] = [ t, p, val]
        if i == 5:
            out[index] = [ val, p, q]
    return out


# TODO convert this function from glsl to python
# def hueShift( vec3 color, float hueAdjust ){

#     const vec3  kRGBToYPrime = vec3 (0.299, 0.587, 0.114);
#     const vec3  kRGBToI      = vec3 (0.596, -0.275, -0.321);
#     const vec3  kRGBToQ      = vec3 (0.212, -0.523, 0.311);

#     const vec3  kYIQToR     = vec3 (1.0, 0.956, 0.621);
#     const vec3  kYIQToG     = vec3 (1.0, -0.272, -0.647);
#     const vec3  kYIQToB     = vec3 (1.0, -1.107, 1.704);

#     float   YPrime  = dot (color, kRGBToYPrime);
#     float   I       = dot (color, kRGBToI);
#     float   Q       = dot (color, kRGBToQ);
#     float   hue     = atan (Q, I);
#     float   chroma  = sqrt (I * I + Q * Q);

#     hue += hueAdjust;

#     Q = chroma * sin (hue);
#     I = chroma * cos (hue);

#     vec3    yIQ   = vec3 (YPrime, I, Q);

#     return vec3( dot (yIQ, kYIQToR), dot (yIQ, kYIQToG), dot (yIQ, kYIQToB) );
