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

    #create a dictionary of the source nodes (j) : all destination nodes (i)
    destinations = {}

    #also create the reverse dict, with destinations : source pages which link to it    
    sources = {}

    #add every node to the dictionary
    for n in range(0,V) :
        line = next(reader)             #read the next line from the file
        index = int(line[0])            #cast the index to an integer
        urls[index] = line[1]           #add the data to the dictionary

    for n in range(0, V) :
        line = next(reader)             #read the next line from the file
        src = int(line[0])
        dst = int(line[1])
        #if the key has no value, set the value to an empty list
        #then append the destination node to the list
        destinations.setdefault(src, []).append(dst)
        sources.setdefault(dst, []).append(src)

    #create initial state vector p(0)
    initialVector = []
    for n in range(0,V) :
        initialVector.append(1/V)          #initialize the vector

    #initialize a dict of tuples as our matrix P
    #P = {}
    #for i in range(0,V) :
    #    for j in range(0,V) :
    #        P[(i,j)] = 0

    #iterate through and populate the matrix P
    #for j in range(0,V) :
    #    for i in range(0,V) :
    #        if i in destinations[j] :           #if i is in the list of destinations
    #            P[(i,j)] = 1/N[j]               #add 1/n_j to the matrix at (i,j)

    #Initialize an array/matrix P
    P = np.zeros(V,V)

    #populate the matrix
    for j in range(0,V) :
        for i in range(0,V) :
            if i in destinations[j] :
                P[j][i] = 1/len(destinations[j])

    P = P*damp + (1-damp)                       #modify P w/ dampening factor

    #Make vector (list) N to store all n_j values
    #N = []
    #for j in range(0,V) :
    #    if j in destinations :                   #need to check if it's in the dict
    #        N.append(len(destinations[j]))
    #    else :
    #        N.append(0)

#Time to rank the pages!
#PR(V, initialVector, N, damp)
def PageRank(verts, initVec, outgoing, damp) :
        
    nextVector = initVec
    for a in range(0,verts) :
        total = 0
        if a in sources :                       #first check if a exists
            links = sources[a]                  #links contains list of pages linking to page a
        else :
            continue                            #if not in sources, move on
        for j in links :
            try:
                if ((outgoing[j] !=0) & (initVec[j] !=0)) :
                    total += initVec[j]/outgoing[j] #add page rank/outbound links    
            except IndexError:
                print("error on j = ", j)
                break

            nextVector[a] = ((1-damp) + damp*total)
    print(nextVector)
    
    if (initVec != nextVector) :
        PageRank(verts, nextVector, outgoing, damp)
    else :
        print("success!")
        return nextVector

finalRank = PageRank(V, initialVector, N, .85)
finalRankDict = {}

#Now we need to create a printable list
#First we make finalRank a dictionary of index : rank
for i in range(1,len(finalRank)) :
    finalRankDict[i] = finalRank[i]
    
#now sort these by rank, in descending order; format is a list of (index, rank) tuples
sortedRanks = sorted(finalRankDict.items(), key=operator.itemgetter(1), reverse=True)

#Need to print these in order by searching through the urls dictionary
