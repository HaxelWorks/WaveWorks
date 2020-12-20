from scipy.stats import gausshyper
import matplotlib.pyplot as plt
import numpy as np

# GARBAGE
# a, b, c, z = 13.8, 3.12, 2.51, 5.18
# mean, var, skew, kurt = gausshyper.stats(a, b, c, z, moments="mvsk")
# window = np.linspace(gausshyper.ppf(0., a, b, c, z), gausshyper.ppf(1, a, b, c, z), 13)




from scipy.signal.windows import gaussian
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1)
    ax.plot(gaussian(13,2))
