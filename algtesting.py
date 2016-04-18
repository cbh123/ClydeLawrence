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
# Extractor



import essentia.standard as es
from pylab import *
from numpy import *
from helper import *
from sklearn import svm
from sklearn.decomposition import PCA

def main():
    dim = 24
    X = analyzeSongs(chord_vectorize,'audio/train/',dim)
    y = ['daft']*8+['beatles']*8+['wu']*4
    clf=svm.SVC()
    clf.fit(X,y)
    
    wu = analyzeSongs(chord_vectorize,'audio/test/',dim)
    print clf.predict(wu)
        

def chord_vectorize(audio):
    tonal = es.TonalExtractor()
    t = tonal(audio)
    beatsperminute = bpm(audio)
    return [beatsperminute]+t[1]
    
def hi_level_vectorize(audio):
    tonal = es.TonalExtractor()
    rhythm = es.RhythmExtractor()
    dynamic = es.DynamicComplexity()
    t = tonal(audio)
    r = rhythm(audio)
    d = dynamic(audio)
    v =array([r[0],pitch2int(t[9]),majmin2int(t[10]),t[11],t[0],d[0],d[1]])
    #v = array([r[0],t[11]])
    return v
    
def lo_level_vectorize(audio):
    ext = es.LowLevelSpectralExtractor()
    slicer = es.Slicer(startTimes = [60],endTimes = [90])
    audioSlice = slicer(audio)[0]

    
    
    
    barkbands=ext(audioSlice)[0]
    pca = PCA(n_components=2)
    v=pca.fit_transform(barkbands)
    v = reshape(v,[1,-1])[0]

    #dim = 2586 for two components
    return v
    
    
    
    
    
    

#our info: [BPM,Key,Maj/Minor,Strength,ChangeRate]

####   Tonal Vector ####
#chords_changes_rate (real) - See ChordsDescriptors algorithm documentation
#chords_histogram (vector_real) - See ChordsDescriptors algorithm documentation
#chords_key (string) - See ChordsDescriptors algorithm documentation
#chords_number_rate (real) - See ChordsDescriptors algorithm documentation
#chords_progression (vector_string) - See ChordsDetection algorithm documentation
#chords_scale (string) - See ChordsDetection algorithm documentation
#chords_strength (vector_real) - See ChordsDetection algorithm documentation
#hpcp (vector_vector_real) - See HPCP algorithm documentation
#hpcp_highres (vector_vector_real) - See HPCP algorithm documentation
#key_key (string) - See Key algorithm documentation
#key_scale (string) - See Key algorithm documentation
#key_strength (real) - See Key algorithm documentation

#### Rhythm Vector ####
#bpm (real) - the tempo estimation [bpm]
#ticks (vector_real) - the estimated tick locations [s]
#estimates (vector_real) - the bpm estimation per frame [bpm]
#bpmIntervals (vector_real) - list of beats interval [s]