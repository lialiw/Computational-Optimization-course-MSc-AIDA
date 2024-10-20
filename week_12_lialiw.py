# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 00:11:21 2022

@author: Fik
"""

"""
    Sources:
        https://careerkarma.com/blog/python-sort-a-dictionary-by-value/    
        
"""

import re, math, random, time


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


def euclidean(a, b):
    x, y = 0, 1
    return (((a[x]-b[x])**2)+((a[y]-b[y])**2))**0.5


def route_dist(route,coordinates): #starts from 0 to also count distance from last node (-1) to the first node (0)
    dist=0
    for i in range(len(route)):
        dist+=euclidean(coordinates[route[i]],coordinates[route[i-1]])
    return dist


def greedily_nextNode(coordinates, visited, i):
    dmin = math.inf
    for j in range(len(coordinates)):
        if(visited[j] == False):
            d = euclidean(coordinates[j], coordinates[i])
            if(d < dmin):
                dmin = d
                k = j
    return k, dmin
    

def rcl_nextNode(coordinates, visited, i, rcl_length):
    dists_from_node_i = {}
    for j in range(len(coordinates)):
        if(visited[j] == False):
            d = euclidean(coordinates[j], coordinates[i])
            dists_from_node_i[j]=d
    dists_from_node_i = sorted(dists_from_node_i.items(), key=lambda x: x[1])

    rcl_dists_from_node_i = dists_from_node_i[:rcl_length] #; print(rcl_dists_from_node_i)
    rand_eqProb_choice = random.choice(rcl_dists_from_node_i) #; print(rand_eqProb_choice)
    
    return rand_eqProb_choice #a tuple
    
        
def nearest_neighbour_v2(coordinates, numNodes, rand_startNodeFlag = False, rcl_length=0):

    visited = [False]*len(coordinates)
    if rand_startNodeFlag:
        i = random.choice([x for x in range(len(numNodes))])
    else:
        i = 0
    dist = 0
    order = [i]

    while(sum(visited) < numNodes):
        visited[i] = True
        if rcl_length:
            #print("skata")
            i, dmin = rcl_nextNode(coordinates, visited, i, rcl_length)
            #print(i, dmin)
        else:
            i, dmin = greedily_nextNode(coordinates, visited, i)
        order.append(i)
        dist += dmin
        visited[i] = True
    return order, dist


def opt_2_swap(route, i,  k):
    
    r1=route[:i]
    r2=route[i:k]
    r2=r2[::-1]
    r3=route[k:]
    
    return(r1+r2+r3)


def opt_2(times_applied, times_dist_same, nodes_list, route, dist):
    
    flagApplied, new_dist, flag_distSame= 0, 0, 0
    new_route=[]
    #print(dist)
    old_dist = 0
    while (flagApplied < times_applied):
        old_dist = dist
        for i in range(len(nodes_list)):
            for j in range(i,len(nodes_list)):
                
                new_route = opt_2_swap(route[:],i,j)
                new_dist = route_dist(new_route, nodes_list)
                
                if new_dist<dist:
                    dist=new_dist
                    route=new_route
            
        #print(old_dist, dist)
        if old_dist==dist:
            flag_distSame+=1
            if flag_distSame == times_dist_same:
                break
            
        flagApplied+=1
        
    return new_route, dist


def writeRoute(tspName, route, dist):
    
    f = open(tspName+'_route.txt', 'a')
    
    s='Distance of best route: ' +str(dist) +'\nBest route: \n'
    for i in range(len(route)):
        s+= str(route[i]+1)+' -> '
        if i % 100 ==0 and i!=0:
            s+='\n'
    s+= str(route[0]+1)+'\n\n'
    #print(s)
    f.write(s)
    
    f.close()
     

def grasp(tspName, nodes_list, time_limit, time_start, dimension, times_dist_same):
    
    best_route, best_dist = [], math.inf
    while time.time()-time_start < time_limit:
        route, dist = nearest_neighbour_v2(nodes_list, len(nodes_list), False, 4)
        print("(initialization) Distance from Nearest Neighbour: ", dist, '\n', route,'\n', len(route),'\n\n')
        
        if best_dist == math.inf:
            writeRoute(tspName, route, dist)
        
        ## 2_opt will be applied as many times as a quorter of the problem's dimension
        times_applied = dimension//4 #; print(times_applied)
        new_route, new_dist = opt_2(times_applied, times_dist_same, nodes_list, route, dist)
        print("Distance from Nearest Neighbour after 2-opt: ", new_dist, '\n', new_route,'\n', len(route),'\n\n')    
        if best_dist>new_dist:
            best_route, best_dist = new_route, new_dist
            
    print("Distance from Nearest Neighbour after 2-opt: ", best_dist, '\n', best_route,'\n', len(route),'\n\n')    
    writeRoute(tspName, best_route, best_dist)
  
    
def main():
        
    tspFileNames = ["ulysses16.tsp","a280.tsp","att532.tsp", "u1817.tsp"]
    #tspFileNames = ["ulysses16.tsp"]
    #tspFileNames=["a280.tsp"]

    intFlag, floatFlag= False, True
    times_dist_same = 5

    for tspName in tspFileNames:
        
        nodes_dict = {}
        data = read_tsp_data(tspName)
        dimension = detect_dimension(data)#; print(dimension)
        start_from = detect_start_from(data) #; print(start_from)
        
        nodes_dict = get_nodes_cords(data, start_from, intFlag, floatFlag)#; print(nodes_dict)
    
        nodes_list = list(nodes_dict.values())#; print(nodes_list)

        
        time_limit = dimension*5
        time_start = time.time()
        grasp(tspName, nodes_list, time_limit, time_start, dimension, times_dist_same)



if __name__ == '__main__':
    main()