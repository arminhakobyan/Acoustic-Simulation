import numpy as np
from funcs import read_wav, resamplingAudio
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import wave

new_fs = 32000
n = 10
filename = 'C:\\examples_samples_guitar.wav'
sound_array, fs = read_wav(filename, mmap=False)
audio = resamplingAudio(list(sound_array), fs, 32000)
write("audio.wav", 32000, audio.astype(np.int16))

file_name = wave.open("audio.wav", 'rb')
length_n = int(len(audio) / 10)  # length of each part of a divided audio
duration = int(len(audio) / 32000)  # duration of an audio
time_array = np.arange(0, duration, duration / len(audio))

#  doing fft
power_spectrum, frequencies_found, t, image_axis = plt.specgram(audio, Fs=new_fs,
                                                                mode='magnitude',
                                                                noverlap=0,
                                                                NFFT=1024,
                                                                xextent=(0, np.max(time_array)))
powers = np.transpose(power_spectrum)
#  finding max value of all powers
max_value_of_each_spec = []
for i in range(len(powers)):
    max_value_of_each_spec.append(max(powers[i]))
    max_of_all_spec = max(max_value_of_each_spec)

powers = list(powers)
frequencies_found = list(frequencies_found)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
x = frequencies_found
y = powers[0]
ax.set_ylim([0, max_of_all_spec * 1.2])
line1, = ax.plot(x, y, 'c-')
audio = list(audio)
i = 0
while i <= len(audio) - length_n:
    for j in range(i, i + length_n):
        line1.set_ydata(powers[j])
        fig.canvas.draw()
        fig.canvas.flush_events()
    i += length_n
