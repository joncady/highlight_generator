'''
Name: Highlight Generator
Version: 1.0
Dev: Jonathan Cady
License:
    -Please do not sell this program for money, it is open source
    -All packages are available on PyPi
    -More info in the Readme file
'''


from moviepy.editor import *
import moviepy.audio.fx.all as afx
# necessary for finding all of the video files in the 'clips' directory
from os import listdir
import random
import math
import os


# chooses from the songs available in the soundtrack folder
def get_random_soundtrack():
    allTracks = listdir('./soundtracks')
    track = random.choice(allTracks)
    return AudioFileClip('./soundtracks/' + track)


# returns a start for the soundtrack that is the length of the video and will not overflow over the duration
def get_random_start(videoDuration, audioDuration):
    randomStart = random.randint(0, math.floor(audioDuration - videoDuration))
    return randomStart


# creates a sublip based on user input
# tests all cases and ensures that start and end times are valid
def get_subclip(videoClip):
    error = True
    while error:
        try:
            start = int(input('Enter start time: '))
            end = int(input('Enter end time: '))
            if start < 0 or end < 0:
                print('One or both of your times was negative. Only positive times work, try again!')
            elif start > videoClip.duration:
                print('Your start time was beyond the duration of the clip! Try again!')
            elif end < start:
                print('Your start is after your end, please try again!')
            elif end > videoClip.duration:
                print('Your end time was beyond the duration of the clip! Try again!')
            else:
                error = False
        except ValueError:
            print('Please print a valid integer that is greater than 0.')
    cutClip = videoClip.subclip(start, end)
    return cutClip


print('Welcome to Highlight Generator!')
# gets the path for each file in the 'clips' directory
allClips = listdir('./clips')
if len(allClips) == 0:
    while True:
        print('Please add some files to the "clips" directory!')
        check = input('Type "c" to check again, or "a" to abort the program. ')
        if check is 'c':
            allClips = listdir('./clips')
            if len(allClips) > 0:
                break
        elif check is 'a':
            print('Program shutting down! See you next time.')
            raise SystemExit
# relative path for the 'directory'
relPath = './clips/'
clipsList = []
for clip in allClips:
    while True:
        choice = input('Would you like to trim {}? '.format(clip))
        fullClip = relPath + clip
        if choice is 'y':
            clipsList.append(get_subclip(VideoFileClip(fullClip)))
            break
        elif choice is 'n':
            clipsList.append(VideoFileClip(fullClip))
            break
        else:
            print('Type "y" for yes or "n" or no please!')
combinedClip = concatenate_videoclips(clipsList)
audioClip = get_random_soundtrack()
audioStart = get_random_start(combinedClip.duration, audioClip.duration)
trimmedClip = audioClip.subclip(audioStart, audioStart + combinedClip.duration)
newAudio = (trimmedClip.fx(afx.volumex, 0.5)
            .fx(afx.audio_fadein, 1.0)
            .fx(afx.audio_fadeout, 1.0))
finalClip = combinedClip.set_audio(newAudio)
finalClip.write_videofile('./finished/replay.mp4')
for doneClip in clipsList:
    doneClip.close()
delete = input('Would you like to delete the video files in the "clips" directory? ')
while delete is 'y':
    try:
        for file in allClips:
            os.remove(relPath + file)
        print('Clips deleted!')
        break
    except PermissionError as e:
        print(e)
        print('Unable to delete files! Please close open files and folders.')
        delete = input('Would you like to try again? ')
print('Your new clip is done! Thanks for using this program!')
