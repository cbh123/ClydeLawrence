# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:35:25 2016

@author: Frisch
"""
import os
from essentia.standard import *
from pylab import *
from numpy import *

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
    
    
def analyzeSongs(alg):
    songlist = os.listdir(os.getcwd()+'/audio/list')
    #this is where I am keeping a bunch of soundfiles
    d = {}

    for songfile in songlist:
        song = MonoLoader(filename = 'audio/list/'+songfile)()
        song = EqualLoudness()(song)
        d[songfile]=alg(song)
    
    return d
    
    
def sortDict(d):
    s = [(i,d[i]) for i in d]
    s.sort(key=lambda x: x[1], reverse=True)
    return s