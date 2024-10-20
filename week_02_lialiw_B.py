# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 05:39:12 2021

@author: Fik
"""

'''
This code "reads" a linear sparse problem's matrix A and compresses it (by CSC).
.txt files  were created based on the matrices described in pages 16-17 of Lecture_02.pdf of Computational Optimization, 
in order to be tested as an input
'''

def readProblem(fileName, charsDropped, problemElems, toInt):
    '''
    lines = string_with_empty_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    
    '''
    f = open(fileName, "r")
    lines = f.readlines()
    flag=''
    for line in lines:
        #if not line.strip():
        #if line.strip(): #non-empty lines
        for char in charsDropped:
            line = line.replace(char, '')
            #print(type(line))
        for key in problemElems.keys():
            if key in line:
                #print(line)
                flag=key
                line = line.replace(key, '')
            #print(flag,line)
        if line.split():
            if toInt: #if toInt==true, matrix' numbers, which are type: string, are converted to type: int
                problemElems[flag].append(list(map(int, line.split())))
                #print(type(line.split()))
            else:
                problemElems[flag].append( line.split())
    f.close()        
    return problemElems


def create_CSC(matrixA):
    
    Anz, JA, IA = [], [], []
    numRows, numCols = len(matrixA), len(matrixA[0])
    nz=1 #non zero elements of matrix
    for j in range(numCols):
        IA.append(nz)
        for i in range(numRows):
            if matrixA[i][j]!=0:
                Anz.append(matrixA[i][j])
                JA.append(j)
                nz+=1
    IA.append( len(Anz)+1 )
    
    return Anz, JA, IA
   
      
def main():

    
    fileName='practice_1_lec2_pa16.txt'
    #fileName='practice_1_lec2_pa16_i.txt'
    #fileName='practice_1_lec2_pa16_ii.txt'
    #fileName='practice_1_lec2_pa16_iii.txt'
    
    charsDropped = '=[]'
    problemElems ={'A': []}
    
    problemElems = readProblem(fileName, charsDropped, problemElems,1) #; print(problemElems)
    
    #'''
    Anz, JA, IA = create_CSC(problemElems['A'])
    print("Anz: ", Anz)
    print("JA: ",JA)
    print("IA: ",IA)
    #'''


if __name__ == "__main__":
    main()

            