This script creates long concatenated mp3s from numerous short files. It is intended for audiobooks. 

It wraps the ffmpeg concatenate shell command in nicer python handling. Run it from the directory that contains the files or folder you want to merge.

to install:

python -m build

cd dist

pip install <wheel file>

to run:
  
merge-mp3

optional argument 
--disc-files
will create single files of each disc or directory instead of a single file for the whole folder
