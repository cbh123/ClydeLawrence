# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 19:45:36 2016

@author: Frisch
"""

import os
import essentia.standard as es
from pylab import *
from numpy import *
import png

def piano2hz(n):
    return 2**((n-49)/12.0) * 440

#def getFreqBands(audio):
#    slicer = es.Slicer(startTimes = [20],endTimes = [30])
#    audio = slicer(audio)[0]
#    m = zeros([256,128])
#    W = es.Windowing()
#    FC = es.FrameCutter()
#    S = es.Spectrum()
#    bands = range(1,130)
#    bands = [x-.5 for x in bands]  
#    bands = [piano2hz(x) for x in bands]
#    F = es.FrequencyBands(frequencyBands = bands)
#    for i in range(256):
#        frame = FC(audio)
#        window = W(frame)
#        spectrum = S(window)
#        m[i]=F(spectrum)
#    m=m.transpose()
#    im = zeros([256,256])
#    for i in range(128):
#        im[2*i] = m[i]
#        im[2*i+1]= m[i]
#    return im
    
    
def getFreqBeats(audio):
    Rhythm=es.RhythmExtractor()
    r = Rhythm(audio)
    ticks = r[1][:256]
    if len(ticks) < 256:
        return array([])
    endticks = ticks+.5
    slicer = es.Slicer(startTimes = ticks,endTimes = endticks)
    slices = slicer(audio)
    m = zeros([256,128])
    W = es.Windowing()
    S = es.Spectrum()
    bands = range(1,130)
    bands = [x-.5 for x in bands]  
    bands = [piano2hz(x) for x in bands]
    F = es.FrequencyBands(frequencyBands = bands)
    for i in range(256):
        window = W(slices[i])
        spectrum = S(window)
        m[i]=F(spectrum)
    m=m.transpose()
    im = zeros([256,256])
    for i in range(128):
        im[2*i] = m[i]
        im[2*i+1]= m[i]
    return im
 
def songs2png(directory):
    songlist = os.listdir(os.getcwd()+'/audio/'+directory)
    for song in songlist:
        if song[0] == '.':
            songlist.remove(song)
    if not os.path.exists('images/'+directory):
        os.makedirs('images/'+directory)
    for songfile in songlist:
        song = es.MonoLoader(filename = 'audio/'+directory+'/'+songfile)()
        song = es.EqualLoudness()(song)
        bands = getFreqBeats(song)
        if bands.any():
            stripped = os.path.splitext(songfile)[0]
            picfile='images/'+directory+'/'+stripped+'.png'
            bands2png(bands,picfile)

   
def bands2png(bands,filename):
    multifactor = 255/(bands.max())
    pngbands = (bands * multifactor).astype(int)
    
    f = open(filename,'wb')
    w = png.Writer(pngbands.shape[1],pngbands.shape[0],greyscale=True)
    w.write(f,pngbands)
    f.close()