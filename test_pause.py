import os
import pygame
from pygame import mixer_music
from shutil import move
from threading import Thread
import time
import predict_model
import Music_Player

songs = Music_Player.load_music()

song = []
flag = 0
songs2 = Music_Player.PriorityQueue()
belly_cry_count = 1
burping_cry_count = 1
discomfort_cry_count = 1
hungry_cry_count = 1
tired_cry_count = 1
silent_count = 1

record_flag = True  # Flag to control recording

def Baby_Cry_Detection():
    global belly_cry_count, burping_cry_count, discomfort_cry_count, hungry_cry_count, tired_cry_count, silent_count, flag, song, songs, songs2

    while True:
        if record_flag:
            print("Recording Audio ... ")
            label, file = predict_model.predict()

            if label == 1:
                # Play Music
                if songs.isEmpty():
                    songs = Music_Player.load_music()
                song = songs.delete()
                print("Baby is Crying because of Belly Pain")

                flag = 1
                if belly_cry_count == 6:
                    predict_model.move_files(1)
                    belly_cry_count = 1
                move("New.wav", "belly_cry" + str(belly_cry_count) + ".wav")

                belly_cry_count += 1
            
            elif label == 2:
                # Play Music
                if songs.isEmpty():
                    songs = Music_Player.load_music()
                song = songs.delete()
                print("Baby is Crying because of Burping")

                flag = 2
                if burping_cry_count == 6:
                    predict_model.move_files(2)
                    burping_cry_count = 1
                move("New.wav", "burping_cry" + str(burping_cry_count) + ".wav")

                burping_cry_count += 1

            elif label == 3:
                # Play Music
                if songs.isEmpty():
                    songs = Music_Player.load_music()
                song = songs.delete()
                print("Baby is Crying because of Discomfort")
                print("Playing Song" + song[0])
                pygame.mixer.music.load("Songs/" + song[0])
                pygame.mixer.music.play()

                flag = 3
                if discomfort_cry_count == 6:
                    predict_model.move_files(3)
                    discomfort_cry_count = 1
                move("New.wav", "discomfort_cry" + str(discomfort_cry_count) + ".wav")

                discomfort_cry_count += 1

            elif label == 4:
                # Play Music
                if songs.isEmpty():
                    songs = Music_Player.load_music()
                song = songs.delete()
                print("Baby is Crying because of Hungry")
            
                flag = 4
                if hungry_cry_count == 6:
                    predict_model.move_files(4)
                    hungry_cry_count = 1
                move("New.wav", "hungry_cry" + str(hungry_cry_count) + ".wav")

                hungry_cry_count += 1

            elif label == 5:
                # Play Music
                if songs.isEmpty():
                    songs = Music_Player.load_music()
                song = songs.delete()
                print("Baby is Crying because of Tired")
                print("Playing Song" + song[0])
                pygame.mixer.music.load("Songs/" + song[0])
                pygame.mixer.music.play()

                flag = 5
                if tired_cry_count == 6:
                    predict_model.move_files(5)
                    tired_cry_count = 1
                move("New.wav", "tired_cry" + str(tired_cry_count) + ".wav")

                tired_cry_count += 1

            else:
                if silent_count == 6:
                    predict_model.move_files(0)
                    silent_count = 1
                move("New.wav", "silent_" + str(silent_count) + ".wav")

                silent_count += 1
                if flag == 0:
                    song[1] += 1
                    print(song)
                    songs.insert(song[0], song[1])
                    flag = 0
                print("Baby is Silent")
        
        else :
            print("Recording Paused...")
        time.sleep(3)  # Adjust the sleep duration based on your needs

status = True
if __name__ == '__main__':
    pygame.init()
    Thread(target=Baby_Cry_Detection).start()

    while status:
        # Check if music is playing
        if pygame.mixer.music.get_busy():
            record_flag = False  # Pause recording while music is playing
        else:
            record_flag = True  # Resume recording when music is done playing

        time.sleep(3)  # Adjust the sleep duration based on your needs
