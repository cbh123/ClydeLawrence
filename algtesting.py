# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 19:27:26 2016

@author: Frisch
"""
#relevant algorithms:
# MonoLoader
# EqualLoudness
# PredominantPitchMelodia
# KeyExtractor
#MultiPitchKlapuri
# RhythmExtractor
#




from essentia.standard import *
from pylab import *
from numpy import *

filename = 'audio/clyde/oranges.m4a'

audio = MonoLoader(filename = filename)()
audio = EqualLoudness()(audio)

rhythm = RhythmExtractor()

r = rhythm(audio)

KeyExt = KeyExtractor()
k = KeyExt(audio)

#beat = BeatTrackerMultiFeature()
#
#ticks,conf = beat(audio)


#multi = MultiPitchKlapuri()
#
#pcp = multi(audio)


#peaks = SpectralPeaks()
#frequencies,magnitudes = peaks(audio)
#
#hpcp = HPCP()
#pcp = hpcp(frequencies,magnitudes)
#
#key = Key()
#
#out = key(pcp)



#chord_detection = ChordsDetection()
#chords = chord_detection(pcp)
