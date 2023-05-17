import os.path 
import subprocess
import argparse
import glob
from natsort import natsorted

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
    for subdir, dirs, files in os.walk(baseDirectory):
        for file in files:
            tempext = os.path.splitext(file)[1]
            if tempext not in extensions:
                extensions[tempext] = 1
            else:
                extensions[tempext] = extensions[tempext]+1
    print("extensions found:", extensions)
    ext = max(extensions, key=extensions.get)
    print("file extension set to", ext)

    # for processing disc folders
    for subdir in natsorted(os.listdir(baseDirectory)):
        if not subdir.startswith('.') and (os.path.isdir(subdir)):
            print("adding files from folder", subdir)       
            runCommand(subdir)

    if singleFile:
        runCommand(baseDirectory)
        for file in glob.glob(f"Disc*{ext}"):
            filecount-=1
            os.remove(file)

    
    print(f"created {filecount} files")

def runCommand(directory):

    count = 0
    global filecount
    samplefile = ""

    with open("filelist.txt", "w") as fileList:
        for filename in sorted(os.listdir(directory)):
            if not (filename.startswith('.')) and (filename.lower().endswith(ext)):
                relativePath = os.path.join(directory,filename)
                if not samplefile:
                    samplefile = relativePath
                print("adding", relativePath)
                print(f"file '{relativePath}'", file=fileList)
                count += 1

    print("files to process", count)
    
    if count > 0:
        arg = f"-f concat -safe 0 -i filelist.txt -acodec copy output{ext}"
        subprocess.check_call("ffmpeg %s" % arg, shell=True)
        filecount+=1
        outputName = os.path.basename(directory) + ext
        finaloutput = f"{baseDirectory}/{outputName}"
        print("final output name", finaloutput)
        os.rename(f"output{ext}", finaloutput)        
        os.remove("filelist.txt")

# ffmpeg -f concat -safe 0 -i filelist.txt -acodec copy output.m4b