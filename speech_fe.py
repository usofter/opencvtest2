import time

import numpy as np

import matplotlib.pyplot as plt

from scipy.io import wavfile

from python_speech_features import mfcc, logfbank


import sounddevice as sd
from scipy.io.wavfile import write

# fs = 16000  # Sample rate
# seconds = 5  # Duration of recording
#
# myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
# sd.wait()  # Wait until recording is finished
# write('output.wav', fs, myrecording)  # Save as WAV file



#Reading the stored audio file, returning sampling frequency and audio signal

freq_sampling, audio_sig = wavfile.read("output.wav")

#Taking first 15000 samples for analysis

# audio_sig = audio_sig[:15000]
audio_sig = audio_sig[:15000]

#Exatracting MFCC features and printing its parameters

mfcc_features = mfcc(audio_sig, freq_sampling)

print('\nMFCC:\nNumber of windows =', mfcc_features.shape[0])

print('Length of each feature =', mfcc_features.shape[1])

# Output:
#
# MFCC:
#
# Number of windows = 186
#
# Length of each feature = 13

#Plotting and visualizing the MFCC features

mfcc_features = mfcc_features.T


plt.matshow(mfcc_features)
plt.title('MFCC')
plt.show()


# Exatracting Filter bank features and printing its parameters
filterbank_features = logfbank(audio_sig, freq_sampling)

print('\nFilter bank:\nNumber of windows =', filterbank_features.shape[0])

print('Length of each feature =', filterbank_features.shape[1])

#Plotting and visualizing the Filterbank features

filterbank_features = filterbank_features.T

plt.matshow(filterbank_features)

plt.title('Filter bank')

plt.show()



