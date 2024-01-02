import os
import librosa
import numpy as np
from tqdm import tqdm
import pickle
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import noisereduce as nr
# load data
from scipy.io import wavfile
from shutil import move

np.float = float 

def move_files(flag):

    print("Moving Files")
    if flag == 1:

        for i in range(1, 6):
            move("/home/pi/proyekTelematika/aht10-python-master/belly_cry"+str(i)+".wav",
                 "/home/pi/proyekTelematika/aht10-python-master/belly_pain/belly_cry"+str(i)+".wav")
            
    elif flag == 2:
        for i in range(1, 6):
            move("/home/pi/proyekTelematika/aht10-python-master/burping_cry" + str(i) + ".wav",
                 "/home/pi/proyekTelematika/aht10-python-master/burping/burping_cry" + str(i) + ".wav")
            
    elif flag == 3:
        for i in range(1, 6):
            move("/home/pi/proyekTelematika/aht10-python-master/discomfort_cry" + str(i) + ".wav",
                 "/home/pi/proyekTelematika/aht10-python-master/discomfort/discomfort_cry" + str(i) + ".wav")
            
    elif flag == 4:
        for i in range(1, 6):
            move("/home/pi/proyekTelematika/aht10-python-master/hungry_cry" + str(i) + ".wav",
                 "/home/pi/proyekTelematika/aht10-python-master/hungry/hungry_cry" + str(i) + ".wav")

    elif flag == 5:
        for i in range(1, 6):
            move("/home/pi/proyekTelematika/aht10-python-master/tired_cry" + str(i) + ".wav",
                 "/home/pi/proyekTelematika/aht10-python-master/tired/tired_cry" + str(i) + ".wav")
            
    else:
        for i in range(1, 6):
            move("/home/pi/proyekTelematika/aht10-python-master/silent_" + str(i) + ".wav",
                 "/home/pi/proyekTelematika/aht10-python-master/silence/silent_" + str(i) + ".wav")


def predict():
    file = open("/home/pi/proyekTelematika/aht10-python-master/Model_1.pkl", "rb") # load model
    Model = pickle.load(file)

    # Sampling frequency
    frequency = 22050

    # Recording duration in seconds
    duration = 7

    # to record audio from
    # sound-device into a Numpy
    recording = sd.rec(int(duration * frequency),
                       samplerate=frequency, channels=1)

    # Wait for the audio to complete
    sd.wait()

    # using scipy to save the recording in .wav format
    # This will convert the NumPy array
    # to an audio file with the given sampling frequency
    write("recording0.wav", rate=frequency, data=recording)
    rate, data = wavfile.read("recording0.wav")

    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write("New.wav", rate=rate, data=reduced_noise)

    filename = "New.wav"
    audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')

    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)

    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)

    predicted_label = Model.predict(mfccs_scaled_features)


    return predicted_label, filename



