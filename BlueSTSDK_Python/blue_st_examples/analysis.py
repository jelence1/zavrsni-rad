import sys
import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt
from scipy.fft import fft
from scipy.signal import spectrogram
import tkinter as tk
from tkinter import filedialog, messagebox

import globals


def annot_max(x, y, n, ax=None):
     yf = 2.0/n * np.abs(y[:n//2])
     ymax = max(yf)
     xpos = np.where(yf == ymax)
     xmax = x[xpos][0]
     text= "x={:.3f}, y={:.3f}".format(xmax, ymax)
     if not ax:
          ax=plt.gca()
     bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
     arrowprops=dict(arrowstyle="<-",connectionstyle="angle,angleA=0,angleB=60")
     kw = dict(xycoords='data',textcoords="axes fraction",
               arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
     ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.96), **kw)

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

try:
     if file_path == "":
          sys.exit(0)
     elif file_path.endswith("raw"):
          samples, sampling_rate = sf.read(file_path, channels=globals.CHANNELS, samplerate=globals.SAMPLE_RATE,
                              subtype=globals.SUBTYPE)
     else:
          samples, sampling_rate = sf.read(file_path)
except RuntimeError:
     messagebox.showerror("Invalid file format. Please select an audio file, such as .raw or .wav.")
     sys.exit(0)

mngr = plt.get_current_fig_manager()
mngr.set_window_title(f"Audio Analysis of {file_path}")

plot1 = plt.subplot2grid((4, 4), (0,0),rowspan=2, colspan=4)
plot1.plot(samples)
plot1.set_title("Audio")
plot1.set_xlabel("Sample")
plot1.set_ylabel("Amplitude")

n = len(samples)
T = 1/sampling_rate
yf = fft(samples)
xf = np.linspace(start=0.0, stop=1.0/(2.0*T), num=n//2)

plot2 = plt.subplot2grid((4, 4), (2,0), rowspan=2, colspan=2)
plot2.plot(xf, 2.0/n * np.abs(yf[:n//2]))
plot2.set_title("FFT")
plot2.set_xlabel("Frequency (Hz)")
plot2.set_ylabel("Magnitude")
plot2.set_xlim(0,globals.FREQ_LIMIT)

annot_max(xf, yf, n, plot2)

plot3 = plt.subplot2grid((4, 4), (2, 2), rowspan=2, colspan=2)
plot3.specgram(samples, Fs=sampling_rate)
plot3.set_title("Spectrogram")
plot3.set_xlabel("Time (s)")
plot3.set_ylabel("Frequency (Hz)")
plot3.set_ylim(0,globals.FREQ_LIMIT)

plt.tight_layout()
plt.show()
