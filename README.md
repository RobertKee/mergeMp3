This script creates long concatenated mp3s from numerous short files. It is intended for audiobooks. 

It wraps the ffmpeg concatenate shell command in nicer python handling. Run it from the directory that contains the files or folder you want to merge.

to install:

python -m build

cd dist

pip install <wheel file>

to run:
  
merge-mp3

all arguments are optional
--single-file boolean, default true
this merges the files in the directory the script is run in. if false, it will create files of each disc (assuming per-disc subdirectories) or nothing (no files outside pwd)

--file-extension, default "mp3"
sets the type of file to be merged, only supports audio file extensions supported by ffmpeg
