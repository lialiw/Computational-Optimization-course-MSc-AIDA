# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 06:56:02 2021

@author: Fik
"""

'''
Sources:
    https://github.com/5ymmetric/Travelling-Salesman-Problem-Generator/blob/main/problem_generator.py
    https://www.w3schools.com/python/module_random.asp
    https://www.w3schools.com/python/python_file_open.asp
    
'''

from random import uniform, randrange


def generate_random_points(numPoints, rangeFlag, uniformFlag, rangeX=[-1,-1,-1], rangeY=[-1,-1,-1], mX=-1, sX=-1, mY=-1, sY=-1):
    
    problemDataPoints = []
    generatorUsed= -1 #Default: X~uniform(0, 1), Y~uniform(0, 1)
    edgeType = -1   #Default: EUC_2D
    if  rangeFlag:
        for i in range(numPoints):
            problemDataPoints.append([i+1, randrange(rangeX[0], rangeX[1], rangeX[2]), randrange(rangeY[0], rangeY[1], rangeY[2]) ])
        generatorUsed = 1
    elif uniformFlag:
        for i in range(numPoints):
            problemDataPoints.append([i+1, uniform(mX, sX), uniform(mY, mY) ])
        generatorUsed = 0
    else:
        for i in range(numPoints):
            problemDataPoints.append([i+1, uniform(0, 1), uniform(0, 1) ])
    
    return problemDataPoints, generatorUsed, edgeType


def createTSP_file(problemName, problemDataPoints, generatorUsed, edgeType, rangeX=[-1,-1,-1], rangeY=[-1,-1,-1], mX=-1, sX=-1, mY=-1, sY=-1):
    f = open(problemName+'.tsp', 'w')
    s = 'NAME : '+problemName+'\nCOMMENT : '
    if generatorUsed==-1:
        s+= 'X ~ uniform(0, 1), Y ~ uniform(0, 1)'
    elif generatorUsed==1:
        s+='X ~ random in range('+str(rangeX[0])+', '+str(rangeX[1])+'), step = '+str(rangeX[2]) + ' Y ~ random in range('+str(rangeY[0])+', '+str(rangeY[1])+'), step = '+str(rangeY[2])
    elif generatorUsed==0:
        s+='X ~ uniform('+str(mX)+', '+str(sX)+') Y ~ uniform('+str(mY)+', '+str(sY)+')'
    s+='\nTYPE : TSP\nDIMENSION : '+str(len(problemDataPoints))+'\nEDGE_WEIGHT_TYPE : '
    if edgeType==-1:
        s+= 'EUC_2D'
    s+= '\nNODE_COORD_SECTION\n'
    f.write(s)
    
    for i in range(len(problemDataPoints)):
        s = str(problemDataPoints[i][0])+' '+str(problemDataPoints[i][1])+' '+str(problemDataPoints[i][2])+'\n'
        f.write(s)
    f.write('EOF')
    f.close()
        
          
def main():
    
    numProblems = 3
    numPoints, generatorUsed, edgeType = 16, -1, -1
    problemDataPoints=[]
    
    rangeFlag, uniformFlag = True, False
    rangeX=[0,100,1]; rangeY=[0,1000,10]; mX=-1; sX=-1; mY=-1; sY=-1
    
    for j in range(numProblems):
        problemName = 'problem'+str(j)
        #problemDataPoints, generatorUsed, edgeType = generate_random_points(numPoints, rangeFlag, uniformFlag)
        problemDataPoints, generatorUsed, edgeType = generate_random_points(numPoints, rangeFlag, uniformFlag, rangeX, rangeY)
        
        createTSP_file(problemName, problemDataPoints, generatorUsed, edgeType)

    
if __name__ == '__main__':
    main()

        