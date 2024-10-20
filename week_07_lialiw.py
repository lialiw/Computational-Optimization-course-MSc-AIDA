# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 23:37:56 2021

@author: Fik
"""

"""
It only works for problems found in:
    http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/index.html
"""

"""
Sources:
    https://github.com/tsartsaris/TSPLIB-python-parser/blob/3519054d71f726750238de5807d51aafccc9bbf8/parser.py
    
    http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsplib.html
    http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/index.html
    http://elib.zib.de/pub/mp-testdata/tsp/tsplib/stsp-sol.html
    
    https://www.w3schools.com/python/ref_string_lstrip.asp
    https://www.techiedelight.com/remove-last-element-from-list-python/
    https://pynative.com/python-regex-compile/
    https://www.programiz.com/python-programming/methods/list/pop
    https://stackoverflow.com/questions/6416131/add-a-new-item-to-a-dictionary-in-python
    https://www.w3schools.com/python/ref_string_partition.asp
    https://www.tutorialspoint.com/python/python_tuples.htm
    

Code used from:
    https://github.com/tsartsaris/TSPLIB-python-parser/blob/3519054d71f726750238de5807d51aafccc9bbf8/parser.py
"""

import re

   
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
    
    
def write_tcps_elements(f,tspName, dimension, nodes_dict):

    s = "File's name : "+str(tspName)+ "\nProblem's dimension: "+str(dimension )+"\nProblem's nodes:\n"
    f.write(s)
    for el in nodes_dict:
        s = "node's id: "+str(el)+" coordinates: ("+str(nodes_dict[el][0])+", "+str(nodes_dict[el][0])+")\n"
        f.write(s)
    f.write('\n')

    
def main():
    f = open("tcpProblems.txt", "a+")
    
    tspFileNames = ["a280.tsp","att532.tsp", "u1817.tsp","ulysses16.tsp"]
    '''
    numProblems=3
    tspFileNames=[]
    for j in range(numProblems):
        tspFileNames.append('problem'+str(j)+'.tsp')
    print(tspFileNames)
    #'''    
    

    intFlag,floatFlag= False, True
    
    for tspName in tspFileNames:
        nodes_dict = {}
        data = read_tsp_data(tspName)
        dimension = detect_dimension(data)
        start_from = detect_start_from(data) #; print(start_from)
        nodes_dict = get_nodes_cords(data, start_from, intFlag, floatFlag)
        #print_tcps_elements(tspName, dimension, nodes_dict)        
        write_tcps_elements(f, tspName, dimension, nodes_dict)
    f.close()

if __name__ == '__main__':
    main()
