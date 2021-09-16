This script creates long concatenated mp3s from numerous short files. It is intended for audiobooks. It wraps the ffmpeg concatent shell command in nicer python handling. Run it from the directory that contains the files or folder you want to merge.

python -m build
cd dist
pip install <wheel file>

mergeMp3 <arg> <arg>

all arguments are optional
--single-file boolean, default true. this merges the files in the directory the script is run in. if false, it will create files of each disc or nothing

--file-extension, default "mp3". sets the type of file to be merged.