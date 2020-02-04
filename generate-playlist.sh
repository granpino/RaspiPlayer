#!/bin/bash
# This will scan the USB drive for folders with MP3 and create playlists
# and send them to the mpd directory. 
# Bash script to create playlist files in music subdirectories
# to work with RaspiPlayer. 
# Original by; Steve Carlson (stevengcarlson@gmail.com)
shopt -s extglob

cd /mnt/usbdrive
mv /var/lib/mpd/playlists/!(Radio.m3u) /tmp/ # move old playlists
find . -type d |
while read -r subdir
do
  rm -f "$subdir"/*.m3u
  for filename in "$subdir"/*
  do
    if [ ${filename: -4} == ".mp3" ] || [ ${filename: -5} == ".flac" ] || [ ${filename: -4} == ".ogg" ]
    then
        echo "${filename##*/}" >> ./"$subdir"/"${subdir##*/}.m3u"
    fi
  done
cp -f "$subdir"/*.m3u /var/lib/mpd/playlists/
done
