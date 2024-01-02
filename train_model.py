import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import librosa
#import matplotlib.pyplot as plt
import pandas as pd
import os
import librosa
import numpy as np
from tqdm import tqdm
import pickle

def features_extractor(file):
    audio, sample_rate = librosa.load(file)
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)

    return mfccs_scaled_features

def train_model():
    extracted_features = []

    silent_dir = "D:/dataset/tangisan_bayi/silence/"
    for file in os.scandir(silent_dir):
        final_class_label = 0
        data = features_extractor(file)
        extracted_features.append([data, final_class_label])
        print("Done")

    belly_pain_dir = "D:/dataset/tangisan_bayi/belly_pain/"
    for file in os.scandir(belly_pain_dir):
        final_class_label = 1
        data = features_extractor(file)
        extracted_features.append([data, final_class_label])
        print("Done")

    burping_dir = "D:/dataset/tangisan_bayi/burping/"
    for file in os.scandir(burping_dir):
        final_class_label = 2
        data = features_extractor(file)
        extracted_features.append([data, final_class_label])
        print("Done")

    discomfort_dir = "D:/dataset/tangisan_bayi/discomfort/"
    for file in os.scandir(discomfort_dir):
        final_class_label = 3
        data = features_extractor(file)
        extracted_features.append([data, final_class_label])
        print("Done")
    
    hungry_dir = "D:/dataset/tangisan_bayi/hungry/"
    for file in os.scandir(hungry_dir):
        final_class_label = 4
        data = features_extractor(file)
        extracted_features.append([data, final_class_label])
        print("Done")
    
    tired_dir = "D:/dataset/tangisan_bayi/tired/"
    for file in os.scandir(tired_dir):
        final_class_label = 5
        data = features_extractor(file)
        extracted_features.append([data, final_class_label])
        print("Done")

    extracted_features_df = pd.DataFrame(extracted_features, columns=['feature', 'class'])
    X = np.array(extracted_features_df['feature'].tolist())
    Y = np.array(extracted_features_df['class'].tolist())
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

    model = KNeighborsClassifier()

    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    file = open("Model_1.pkl", "wb")
    pickle.dump(model, file)
    print("Training Success")
    print("Accuracy :", score)

if __name__ == "__main__" :
    train_model()