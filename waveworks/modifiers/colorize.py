#%%
import numba
import numpy as np

#%% 
@numba.njit("float64[:,:](float64,float64[:])")
def colorize(h,v):
    s = 1
    out = np.empty(shape = (250,3))
    i = int(h*6.0) 
    f = (h*6.0) - i
    p = 0
    for index in range(250):
        val = v[index]
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


