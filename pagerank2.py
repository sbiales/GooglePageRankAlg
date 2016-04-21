#CSE 3504 Project 2
#Siena Biales, Vincent Chov
#Google PageRank Algorithm Implementation

import csv
import operator
import numpy as np

with open("hollins.dat", "r") as data:
    reader = csv.reader(data, delimiter = ' ', skipinitialspace=True)

    cols = next(reader)
    
    #Extract the number of nodes (V) and edges (E) from the first line of the file
    V = int(cols[0])
    E = int(cols[1])

    #create a dictionary of the index : url
    urls = {}

    #create a dictionary of the source nodes (i) : all destination nodes (j)
    outgoing = [[] for i in range(V)]

    #add every node to the dictionary
    for n in range(0,V) :
        line = next(reader)             #read the next line from the file
        index = int(line[0])            #cast the index to an integer
        urls[index] = line[1]           #add the data to the dictionary

    for n in range(0, E) :
        line = next(reader)             #read the next line from the file
        src = int(line[0])
        dst = int(line[1])
        #if the key has no value, set the value to an empty list
        #then append the destination node to the list
        outgoing[src-1].append(dst-1)

    #create initial state vector p(0)
    initialVector = []
    for n in range(0,V) :
        initialVector.append(1/V)          #initialize the vector


    #Initialize an array/matrix P
    P = np.zeros((V,V))

    #populate the matrix
    for i in range(0,V) :
        for j in range(0,V) :
            if i in outgoing[j] :
                P[i][j] = 1/len(outgoing[j])

#PR(P, initialVector, damp)
def PageRank(trans, initVec, damp, n=0) :

    length = len(initVec)
    
    nextVector = [0] * length
    
    for i in range(length) :
        total = sum([initVec[j]*trans[i][j] for j in range(length)])
        #for j in range(length) :
        #    total += initVec[j]*trans[i][j]
        nextVector[i] = (1-damp) + damp*total
    
    if (initVec != nextVector and n<100) :
        return PageRank(trans, nextVector, damp, n+1)
    else :
        print("success!")
        return nextVector
    
finalRank = PageRank(P, initialVector, .85)
print(finalRank)
