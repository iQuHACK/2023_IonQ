from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
from tempfile import TemporaryFile
import os
import pickle
import random 
import operator
import math
from collections import defaultdict
from midi2audio import FluidSynth

def distance(instance1 , instance2 , k):
    distance = 0 
    mm1 = instance1[0]
    cm1 = instance1[1]
    mm2 = instance2[0]
    cm2 = instance2[1]
    distance = np.trace(np.dot(np.linalg.inv(cm2), cm1)) 
    distance += (np.dot(np.dot((mm2-mm1).transpose(), np.linalg.inv(cm2)), mm2-mm1)) 
    distance += np.log(np.linalg.det(cm2)) - np.log(np.linalg.det(cm1))
    distance -= k
    return distance

def getNeighbors(trainingSet, instance, k):
    distances = []
    for x in range (len(trainingSet)):
        dist = distance(trainingSet[x], instance, k) + distance(instance, trainingSet[x], k)
        distances.append((trainingSet[x][2], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def nearestClass(neighbors):
    classVote = {}

    for x in range(len(neighbors)):
        response = neighbors[x]
        if response in classVote:
            classVote[response] += 1
        else:
            classVote[response] = 1

    sorter = sorted(classVote.items(), key = operator.itemgetter(1), reverse=True)
    return sorter[0][0]

def getAccuracy(testSet, predictions):
    correct = 0 
    for x in range (len(testSet)):
        if testSet[x][-1]==predictions[x]:
            correct+=1
    return 1.0*correct/len(testSet)

def trainModel(directory = "Data/genres_original/"):
    f = open("my.dat" ,'wb')
    i = 0

    for folder in os.listdir(directory):
        if folder != '.DS_Store':
            i += 1
            if i == 11:
                break
            print(directory+folder)
            for file in os.listdir(directory+folder):
                try:
                    (rate,sig) = wav.read(directory+folder+"/"+file)
                    mfcc_feat = mfcc(sig,rate ,winlen=0.020, appendEnergy = False)
                    covariance = np.cov(np.matrix.transpose(mfcc_feat))
                    mean_matrix = mfcc_feat.mean(0)
                    feature = (mean_matrix, covariance, i)
                    pickle.dump(feature, f)
                except:
                    continue

    f.close()

    dataset = []
    def loadDataset(filename , split , trSet , teSet):
        with open("my.dat" , 'rb') as f:
            while True:
                try:
                    dataset.append(pickle.load(f))
                except EOFError:
                    f.close()
                    break  

        for x in range(len(dataset)):
            if random.random() < split:      
                trSet.append(dataset[x])
            else:
                teSet.append(dataset[x])  

    trainingSet = []
    testSet = []
    loadDataset("my.dat" , 0.8, trainingSet, testSet)

    leng = len(testSet)
    predictions = []
    for x in range (leng):
        predictions.append(nearestClass(getNeighbors(trainingSet ,testSet[x] , 5))) 

    accuracy1 = getAccuracy(testSet, predictions)
    print(accuracy1)

def printDict():
    results = defaultdict(int)
    i = 1
    for folder in os.listdir("Data/genres_original/"):
        if folder != '.DS_Store':
            results[i] = folder
            i += 1
    print(results)

def compute_acc(midiFile):
    dataset = []
    def loadDataset(filename):
        with open("my.dat", 'rb') as f:
            while True:
                try:
                    dataset.append(pickle.load(f))
                except EOFError:
                    f.close()
                    break
    loadDataset("my.dat")

    fs = FluidSynth()
    fs.play_midi(midiFile)
    fs.midi_to_audio(midiFile, 'output.wav')

    (rate, sig) = wav.read('output.wav')
    mfcc_feat = mfcc(sig, rate, winlen=0.020, appendEnergy=False)
    covariance = np.cov(np.matrix.transpose(mfcc_feat))
    mean_matrix = mfcc_feat.mean(0)
    feature = (mean_matrix, covariance, 0)

    neighbors = getNeighbors(dataset, feature, 100)
    return sum([neighbor == 10 for neighbor in neighbors])/100

# Example
compute_acc('output.mid')