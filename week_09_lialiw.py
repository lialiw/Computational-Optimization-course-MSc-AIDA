# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 05:35:55 2021

@author: Fik
"""

'''
Sources:
    https://github.com/aniketbiprojit/TSP-2OPT-NN/blob/master/2_opt.py

Code used from:
    https://github.com/aniketbiprojit/TSP-2OPT-NN/blob/master/2_opt.py
  
'''
import re
from random import random,shuffle,seed
import math


def read_tsp_data(tsp_name):
    """
    Open the TSP file and put each line cleaned of spaces and newline characters in a list
    Returns a list like:
        ['NAME: ulysses16.tsp', 'TYPE: TSP', 'COMMENT: Odyssey of Ulysses (Groetschel/Padberg)', 'DIMENSION: 16', 'EDGE_WEIGHT_TYPE: GEO', 
         'DISPLAY_DATA_TYPE: COORD_DISPLAY','NODE_COORD_SECTION', '1 38.24 20.42', '2 39.57 26.15', '3 40.56 25.32', ................ 'EOF']
    """
    cleaned = []
    with open(tsp_name) as f:
        content = f.read().splitlines()
        #cleaned = [x.lstrip() for x in content if x != ""]
        cleaned = [x.lstrip() for x in content] #; print(type(cleaned)); print(cleaned)
        pop_el=''
        while pop_el!='EOF':
            pop_el = cleaned.pop()
        #print(type(cleaned)); print(cleaned)
        return cleaned


def detect_dimension(in_list):
    #Use a regex here to clean characters and keep only numerics
    #Check for the line DIMENSION in the file and keeps the numeric value
    non_numeric = re.compile(r'[^\d]+')#; print(non_numeric)
    for element in in_list:
        if element.startswith("DIMENSION"):
            dimension = non_numeric.sub("",element) #; print(type(dimension))
            return int(dimension)
        

def detect_start_from(in_list):
    #Use a regex here to clean characters and keep only numerics
    #Check for the line DIMENSION in the file and keeps the numeric value
    start_from=1
    for element in in_list:
        if element.startswith("NODE_COORD_SECTION"):
            break
        start_from+=1
    return start_from
        
        
def get_nodes_cords(data, start_from, intFlag, floatFlag):
    """
    Iterate through the list of line from the file if the line starts with a numeric value within the range of 
    the dimension, we keep the rest which are the coordinates of each city 1 33.00 44.00 results to 33.00 44.00
    """
    #print(data)
    aDict={}
    for i in range(start_from, len(data)):
        index, space, rest = data[i].partition(' ')
        #print(rest)
        x, space, y = rest.partition(' ') #; print(i-start_from+1, "x: ", x, " space: ", space, " y: ", y)
        while (x==''):
            x,space,y=y.partition(' ')
    
        #print(i-start_from+1, "x: ", x, " space: ", space, " y: ", y)
        #'''
        if intFlag:
            aDict[i-start_from+1] = [int(x),int(y)]
        if floatFlag:
            aDict[i-start_from+1] = [float(x),float(y)]
        #'''
    #print(aDict)        
    return aDict         
              

def print_tcps_elements(tspName, dimension, nodes_dict):
    print("File's name : ",tspName, "\nProblem's dimension: ",dimension, "\nProblem's nodes:"); 
    for el in nodes_dict:
        print("node's id: ", el, " coordinates: ", nodes_dict[el])
    print('\n\n')
    
    
def euclidean(a, b):
    x, y = 0, 1
    return (((a[x]-b[x])**2)+((a[y]-b[y])**2))**0.5


def route_dist(route,coordinates):
    dist=0
    for i in range(1,len(route)):
        dist+=euclidean(coordinates[route[i]],coordinates[route[i-1]])
    return dist


def nearest_neighbour(coordinates, numNodes):

    visited = [False]*len(coordinates)
    i = 1
    dist = 0
    order = [i]

    while(sum(visited) < numNodes):
        visited[i] = True
        dmin = math.inf
        for j in range(len(coordinates)):
            if(visited[j] == False):
                d = euclidean(coordinates[j], coordinates[i])
                if(d < dmin):
                    dmin = d
                    k = j
        i = k
        order.append(k)
        dist += dmin
        visited[k] = True
    return order, dist


def writeRoute(tspName, route, dist):
    
    f = open(tspName+'_route.txt', 'w')
    s='Distance from Nearest Neighbour: '+ str(dist)+'\nPath:\n'
    f.write(s)
    
    s=''
    for i in range(len(route)):
        s+= str(route[i]+1)+' -> '
        if i % 100 ==0 and i!=0:
            s+='\n'
    s+= str(route[0]+1)+'\n'
    f.write(s)
    
    f.close()

    
def main():
        
    tspFileNames = ["a280.tsp","att532.tsp", "u1817.tsp","ulysses16.tsp"]
    #tspFileNames = ["ulysses16.tsp"]
    
    '''
    numProblems=3
    tspFileNames=[]
    for j in range(numProblems):
        tspFileNames.append('problem'+str(j)+'.tsp')
    print(tspFileNames)
    #'''    
    
    intFlag, floatFlag= False, True
    #list_flag = True
    
    for tspName in tspFileNames:
        
        nodes_dict = {}
        data = read_tsp_data(tspName)
        dimension = detect_dimension(data)
        start_from = detect_start_from(data) #; print(start_from)
        
        nodes_dict = get_nodes_cords(data, start_from, intFlag, floatFlag)
        
        nodes_list = list(nodes_dict.values())#; print(nodes_list)
        
        route, dist = nearest_neighbour(nodes_list, len(nodes_list))
        #print("Distance from Nearest Neighbour:",dist); print(route,'\n', len(route),'\n\n')        
        writeRoute(tspName, route, dist)    
    
    
if __name__ == '__main__':
    main()