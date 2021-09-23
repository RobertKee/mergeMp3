from os import extsep
import os.path 
import subprocess
import sys
from mutagen.id3 import ID3
import argparse
import pathlib
# import glob

def merge_mp3(**kwargs):

    parser = argparse.ArgumentParser()
    parser.add_argument('--disc-files', default=False, help="set this flag to create one file per disc instead of one file per book", action='store_true')
    args = parser.parse_args()

    global baseDirectory 
    global ext
    global filecount
    global singleFile
    global dotmp3
    global audio

    baseDirectory = os.getcwd()
    filecount = 0
    singleFile = not args.disc_files
    dotmp3 = ".mp3"

    print("merging files in the subdirectories of", baseDirectory)
    print("current directory files merged to create single file:", singleFile)

    # gets file extension
    extensions = dict()
    for files in os.walk(os.getcwd()):
        for file in files:
            print("checking file", file)
            tempext = pathlib.Path(file).suffix
            if tempext not in extensions:
                extensions[tempext] = 1
            else:
                extensions[tempext] = extensions[tempext]+1
    
    ext = max(extensions, key=extensions.get)
    print("file extension set to", ext)


    # for processing disc folders
    for subdir in sorted(os.listdir(baseDirectory)):
        if not subdir.startswith('.') and (os.path.isdir(subdir)):
            print("adding files from folder", subdir)       
            runCommand(subdir)

    if singleFile:
        runCommand(baseDirectory)
    
    print(f"created {filecount} files")

def getOutputName(directory):
    if os.listdir(directory)[0].endswith(dotmp3):
        audio = ID3(os.listdir(directory)[0])
        if (str(audio.get('artist')) != "None") and (str(audio.get('album')) != "None"):
            outputName = str(audio.get('artist')) + " - " + str(audio.get('album')) + dotmp3            
    else:
        outputName = os.path.basename(directory) + ext
        
    print("output file name", outputName)
    return outputName

def runCommand(directory):

    count = 0
    global filecount

    with open("filelist.txt", "w") as fileList:
        for filename in sorted(os.listdir(directory)):
            if not (filename.startswith('.')) and (filename.lower().endswith(ext)):
                relativePath = os.path.join(directory,filename)
                print("adding", relativePath)
                print(f"file '{relativePath}'", file=fileList)
                count += 1

    print("files to process", count)
    
    if count > 0:
        print("creating single file")
        arg = f"-f concat -safe 0 -i filelist.txt -acodec copy output{ext}"
        subprocess.check_call("ffmpeg %s" % arg, shell=True)
        filecount+=1
        finaloutput = f"{baseDirectory}/{getOutputName(directory)}"
        os.rename(f"output{ext}", finaloutput)
        os.remove("fileList.txt")

        if finaloutput.endswith(dotmp3):
            # targetPattern = f"{baseDirectory}/**/*{dotmp3}"
            audio = pathlib.Path(baseDirectory).glob(dotmp3)[0]
            tag = ID3(finaloutput)
            tag.add_tags()
            tag['artist'] = audio.get('artist')
            tag['title'] = audio.get('title')
            tag['date'] = audio.get('date')
            tag['album'] = audio.get('album')
            tag['albumartist'] = audio.get('albumartist')
            tag['tracknumber'] = 1
            tag['discnumber'] = filecount
            tag.save(v2_version=3)
            
            


# ffmpeg -f concat -safe 0 -i filelist.txt -acodec copy output.m4b