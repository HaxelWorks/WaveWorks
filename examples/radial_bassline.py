import waveworks

from waveworks.sources import audio_generator
from waveworks.modifiers.filters import diffusion, savgol_integral, smooth1
from waveworks.sinks.display.radial_sink import RadialSink
from waveworks.sinks.DMX.sacn_sink import SacnSink
from waveworks.modifiers.colorize import colorize
from librosa.feature.spectral import spectral_bandwidth
import numpy as np
import sys
try:
    receiver_ip = sys.argv[1]
except:
    receiver_ip = input("sACN receiver ip?")



next(diff := diffusion())
next(savgol := savgol_integral(0.20))
next(smooth1 := smooth1(0.15))
audio_source = audio_generator()
display_sink = RadialSink()
dmx_sink = SacnSink(receiver_ip)

count = 0
maximum = 0

window = np.kaiser(len(next(audio_source)), 6)
window_len = len(next(audio_source))

x = np.logspace(1.3, 2.3, 250)  # 10-200Hz
# x = np.logspace(2.3, 3, 256) # 200-1000Hz

xp = np.linspace(0, (window_len // 2) - 1, (window_len // 2) + 1)



while True:
    count += 1 
    display_sink.process_events()

    samples = next(audio_source) * window
    samples = (1 + samples) * 0.5

    fft = np.real(np.fft.rfft(samples))

    bandwidth = spectral_bandwidth(S=np.expand_dims(fft ** 2, 1))[0][0]  # outputs result usually <5
    if maximum < bandwidth:
        print("max" + str(maximum := bandwidth))

    fft = np.interp(
        x=x,
        xp=xp,
        fp=fft,
    )

    final_values = diff.send(savgol.send((fft / 75) ** 2))
    hue = smooth1.send((bandwidth/22))
    if hue is None:
        hue = 0.0
    dmx_sink.send(colorize(hue,final_values).flatten())
    display_sink(color=hue, samples=final_values)

    next(savgol)
    next(diff)
