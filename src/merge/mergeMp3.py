import os.path 
import subprocess
import sys
from mutagen.id3 import ID3
import argparse


def merge_mp3(singleFile=True,fileExtension=".mp3"):

    baseDirectory = os.getcwd()
    disc = 1
    outputName = ""

    parser = argparse.ArgumentParser()
    parser.add_argument('--single-file', '-s', help="toggles output of single file (t) or file per disc (f)", type= bool, default=True)
    parser.add_argument('--file-extension', '-e', help="sets the file extension, default mp3", type= str, default=".mp3")

    for subdir in sorted(os.listdir(baseDirectory)):
        if not subdir.startswith('.') and (os.path.isdir(subdir)):     
            with open("discFileList.txt", "w") as fileList:
                for filename in sorted(os.listdir(subdir)):
                    if not (filename.startswith('.')) and (filename.lower().endswith(fileExtension)):
                        relativePath = os.path.join(subdir,filename)
                        print("adding", relativePath)
                        print(f"file '{relativePath}'", file=fileList)

            audio = ID3(os.listdir(baseDirectory)[0])
            if (str(audio.get('artist')) != "None") and (str(audio.get('album')) != "None"):
                outputName = str(audio.get('artist')) + " - " + str(audio.get('album')) + " Disc " + disc + fileExtension
            else:
                outputName = os.path.basename(baseDirectory) + fileExtension
            print("output file name", outputName)

            arg = "-f concat -safe 0 -i discFileList.txt -acodec copy output.mp3"
            subprocess.check_call("ffmpeg %s" % arg, shell=True) 
            
            os.rename("output.mp3", outputName)
            os.remove("discFileList.txt")
            disc += 1
            outputName = ""

    if singleFile:
        print("Outputting single file")
        with open("fileList.txt", "w") as fileList:
            for filename in sorted(os.listdir(baseDirectory)):
                if not (filename.startswith('.')) and (filename.lower().endswith(fileExtension)):
                    print("adding", filename)
                    print(f"file '{filename}'", file=fileList)

        audio = ID3(os.listdir(baseDirectory)[0])
        if (str(audio.get('artist')) != "None") and (str(audio.get('album')) != "None"):
            outputName = str(audio.get('artist')) + " - " + str(audio.get('album')) + fileExtension
        else:
            outputName = os.path.basename(baseDirectory) + fileExtension
        print("output file name", outputName)

        arg = "-f concat -safe 0 -i fileList.txt -acodec copy output.mp3"
        subprocess.check_call("ffmpeg %s" % arg, shell=True) 
                    
        os.rename("output.mp3", outputName)
                    
        os.remove("fileList.txt")
        outputName = ""