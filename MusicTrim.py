#!/usr/bin/python
import re
import os
import fnmatch
import eyed3

def getfilename(song) :
    try:
        songname = song.split("-", 2)[1].lstrip().rstrip()
        songname = re.sub(r'\(.*\)', "", songname)
        songname = songname.rstrip() + ".mp3"
        return songname
    except Exception as e:
        return song

def getwebsitename(song):
    try:
        return song.split("-", 2)[2].lstrip().replace(".mp3", "")
    except Exception as e:
        return ""

def fixtags(audio, filename, websitename):
    audio.tag.title = unicode(filename.replace(".mp3", ""))
    print("-Fixed song title")
    if audio.tag.album is not None:
        audio.tag.album = re.sub(r'\(.*\)', "", audio.tag.album)
        print("-Fixed album name")
    if audio.tag.album_artist is not None:
        if websitename in audio.tag.album_artist:
            audio.tag.album_artist = u""
            print("-Fixed album artist")
    if audio.tag.comments is not None:
        audio.tag.comments.set(u"")
        print("-Fixed comments")
    audio.tag.save()
    print("-Committed changes")

def fixsong(song) :
    print("\nStage 1: Repairing song name")
    filename = getfilename(song)
    websitename = getwebsitename(song)
    print("-Repaired name from \"%s\" to \"%s\"" % (song, filename))
    os.rename(song, filename)
    print("\nStage 2: Repairing song tags")
    fixtags(eyed3.load(os.path.abspath(filename)), filename, websitename)

def main() :
    print("\nFinding music files in " + os.getcwd())
    songs = fnmatch.filter(os.listdir(os.getcwd()), '*.mp3')
    for song in songs:
        print("\nProcessing \"%s\" song" % song)
        fixsong(song)

if __name__ == '__main__':
    main()
