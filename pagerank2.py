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

    #create a list to know how many values in each outgoing node
    outgoing = [0 for i in range(V)]

    #also create a set so that if there are multiple links, you don't double count
    incoming = [set() for i in range(V)]

    #add every node to the dictionary
    for n in range(0,V) :
        line = next(reader)             #read the next line from the file
        index = int(line[0])            #cast the index to an integer
        urls[index] = line[1]           #add the data to the dictionary

    for n in range(0, E) :
        line = next(reader)             #read the next line from the file
        src = int(line[0])
        dst = int(line[1])
        #add one to the number of outgoing links
        outgoing[src-1] += 1
        #add the source node to the set of sources for this destination
        incoming[dst-1].add(src-1)

    #create initial state vector p(0)
    initialVector = []
    for n in range(0,V) :
        initialVector.append(1/V)          #initialize the vector


    #Initialize an array/matrix P
    P = np.zeros((V,V))

    #populate the matrix
    for i in range(V) :
        #only care about when we have outgoing links from j to i
        #incoming[i] holds a set of all nodes (j) which link to i
        for j in incoming[i] :
                P[i][j] = 1/outgoing[j]

#PR(P, initialVector, damp, incoming, iterations)
def PageRank(trans, initVec, damp, incoming, n=0) :

    length = len(initVec)
    
    nextVector = [0] * length
    
    for i in range(length) :
        total = 0
        #use incoming to only look at nonzero locations and lower comp. time
        for j in incoming[i] :
            total += initVec[j]*trans[i][j]
        nextVector[i] = (1-damp) + damp*total
    
    if (initVec != nextVector and n<1000) :
        return PageRank(trans, nextVector, damp, incoming, n+1)
    else :
        print("success!", n)
        return nextVector
    
finalRank = PageRank(P, initialVector, .85, incoming)

#turn this into a dictionary of final rank value : index
rankOrder = {}
for i in range(len(finalRank)) :
    string = str(finalRank[i])          #keys need to be a string
    string = string[:10]                #truncate to length 10
    rankOrder[string] = i
print(list(rankOrder.keys())[0])

#now write the answer to a text file
file = open("ranking.txt", "w")

#need to print out in order of max to min keys of the dict
#we sort finalRank from min to max
finalRank.sort()

for i in finalRank :
    index = finalRank.pop()
    index = str(index)                  #cast the index to a string
    index = index[:10]                  #truncate to length 10
    print(index)
    file.write(index, urls[index])

file.close()

