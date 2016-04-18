# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:35:25 2016

@author: Frisch
"""
import os
import essentia.standard as es
from pylab import *
from numpy import *
from collections import defaultdict

def file2audio(path):
    song = es.MonoLoader(filename = path)()
    song = es.EqualLoudness()(song)
    return song

def bpm(audio):
    rhythm = es.RhythmExtractor()
    r = rhythm(audio)
    return r[0]

def pitchseq(pitch,conf):
    #some constants for freq2pitch:
    A4 = 440
    C0 = A4*pow(2, -4.75)
    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    i = 1
    a = freq2pitch(pitch[0],C0,name)
    seq = []
    if a != 'NP':
        seq.append(a)
    while i < len(pitch):
        b = freq2pitch(pitch[i],C0,name)
        if b != a:
            if b != 'NP' and conf[i]> .02 :
                seq.append(b)
        a = b
        i +=1
    return seq
    
# http://www.johndcook.com/blog/2016/02/10/musical-pitch-notation    
def freq2pitch(freq,C0,name):
    if freq < 1:
        return 'NP'
    h = round(12*log2(freq/C0))
    octave = int(h // 12)
    n = int(h % 12)
    return name[n] + str(octave)
    
def pitch2int(pitch):
    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return name.index(pitch)

def majmin2int(scale):
    if scale == 'major':
        return 1
    else:
        return 0
    
def analyzeSongs(alg,directory,dim):
    songlist = os.listdir(os.getcwd()+'/'+directory)
    for song in songlist:
        if song[0] == '.':
            songlist.remove(song)
    #this is where I am keeping a bunch of soundfiles
    l = len(songlist)
    m = zeros([l,dim])
    i = 0
    for songfile in songlist:
        song = es.MonoLoader(filename = directory+songfile)()
        song = es.EqualLoudness()(song)
        m[i]=alg(song)
        i += 1
    return m
    
    
def chordseq(chords):
    i = 1
    a = chords[0]
    seq = []
    while i < len(chords):
        b = chords[i]
        if b != a:
            seq.append(b)
        a = b
        i +=1
    return seq
    
def countchords(chords):
    counts = defaultdict(int)
    for chord in chords:
        counts[chord]+=1
    return counts
    
def sortDict(d):
    s = [(i,d[i]) for i in d]
    s.sort(key=lambda x: x[1], reverse=True)
    return s
    
def plotChords(audio):
    tonal = es.TonalExtractor()
    t = tonal(audio)
    bar(arange(24),t[1])
    
def chordCounter(audio):
    tonal = es.TonalExtractor()
    t = tonal(audio)
    chords = t[4]
    counts = countchords(chords)
    sortedCounts = sortDict(counts)
    return sortedCounts