# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 04:27:31 2021

@author: Fik
"""

"""
Code used from:
    https://github.com/jmaerte/pysmps/tree/master/pysmps

Sources kouskouveli_week(1)_A:
    https://pypi.org/project/pysmps/
    https://github.com/jmaerte/pysmps
    https://www.cenapad.unicamp.br/parque/manuais/OSL/oslweb/features/featur11.htm
    https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/
    https://stackoverflow.com/questions/1038824/how-do-i-remove-a-substring-from-the-end-of-a-string
    
Instructions kouskouveli_week(1)_A: 
    If the package pysmps is nοt already installed in your 
    computer, install it by using PyPI with the command:
        pip install pysmps
"""

"""
Sources kouskouveli_week(5):
    https://www.codegrepper.com/code-examples/python/how+to+create+vector+in+numpy+of+zeros
    https://www.kite.com/python/answers/how-to-add-a-column-to-a-numpy-array-in-python
    https://stackoverflow.com/questions/7332841/add-single-element-to-array-in-numpy
    https://pypi.org/project/ordered-set/
    https://stackoverflow.com/questions/35681054/how-do-i-extract-a-sub-array-from-a-numpy-2d-array
    https://stackoverflow.com/questions/4455076/how-to-access-the-ith-column-of-a-numpy-multidimensional-array
    https://blog.finxter.com/how-to-convert-list-of-lists-to-numpy-array/
    https://numpy.org/doc/stable/reference/generated/numpy.transpose.html
    https://www.tutorialspoint.com/numpy/numpy_inv.htm
    https://scipy-lectures.org/intro/numpy/operations.html
    https://newbedev.com/python-how-to-check-if-a-numpy-array-has-negative-values-code-example
    https://www.delftstack.com/howto/numpy/sum-of-columns-matrix-numpy/
    https://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
    https://www.geeksforgeeks.org/python-infinity/
    https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
    https://stackoverflow.com/questions/11303225/how-to-remove-multiple-indexes-from-a-list-at-the-same-time/41079803
    https://www.programiz.com/python-programming/methods/list/index
    

Instructions kouskouveli_week(5):
    If the package ordered-set is nοt already installed in your 
    computer, install it by using PyPI with the command:
        pip install ordered-set

"""

from pysmps import smps_loader as smps
import numpy as np
from ordered_set import OrderedSet
from more_itertools import locate
import copy
import time

    
    
def convert_eqin(eqin_list):
    eqin_dict= {'G':1, 'L':-1, 'E':0}
    eqinArray=[]
    for eqin in eqin_list:
        eqinArray.append(eqin_dict[eqin])
    return np.array(eqinArray)


def standarize_problem(A, Eqin, c):
    #print(A.shape[0])
    for i in range(len(Eqin)):
        unit_col = np.zeros((A.shape[0],1))
        if Eqin[i]==-1:
            unit_col[i][0]=1
        elif Eqin[i]==1:
            unit_col[i][0]=-1
        A = np.append(A, unit_col, axis=1)
        Eqin[i]=0
        c = np.append(c,0)

    return A, Eqin, c


def createArray_of_columns_indexed(matrix, indexes_ordSet, vectorFlag):
        subArray = []
        for i in range(len(indexes_ordSet)):
            if vectorFlag:
                subArray.append(matrix[ indexes_ordSet[i] ])
            else:
                subArray.append(matrix[:,indexes_ordSet[i]]) #; print(matrix[:,indexes_ordSet[i]])
        subArray = np.array(subArray) 
        if not vectorFlag:
            subArray = np.transpose(subArray) #; print(subArray)

        return subArray
    

def compute_partitioned_matrices_vectors(A, b, c, B, N):
    
    A_B = createArray_of_columns_indexed(A, B, False) #; print(A_B)
    A_N = createArray_of_columns_indexed(A, N, False) #; print(A_N)
    A_B_inv = np.linalg.inv(A_B)
    
    x_B = A_B_inv.dot(b) #; print(x_B)

    c_B = createArray_of_columns_indexed(c, B, True) #; print(c_B)
    c_N = createArray_of_columns_indexed(c, N, True) #; print(c_N)
    w = c_B.dot(A_B_inv) #; print(w)
    s_N = c_N - (w.dot(A_N))
    
    return A_B, A_N, A_B_inv, x_B, c_B, c_N, w, s_N



def compute_exteriorAlgorithms_elements(A,P,A_B_inv,s_N, thetaFlag, r):
    
    A_P = createArray_of_columns_indexed(A, P, False) #; print(A_P)
    d_B_products = A_B_inv.dot(-A_P)
    d_B = s = np.sum(d_B_products, axis=1) #; print(d_B)
    
    s0=0
    for p in P:
        s0+=s_N[p]
    #print(s0)
    
    if thetaFlag:
        d_B[r]+=1
        
    return  A_P, d_B, s0


def  handle_B_N(m,n, B, N, r, k, l, index_forN):
    
    if not B:
        #initialization, B and N are empty
        A_indexes = OrderedSet([i for i in range(n)])
        B = OrderedSet([i for i in range(n-m, n)])
        N = A_indexes-B
        #print(A_indexes, B, N)
    else:
        aList=list(copy.deepcopy(B)); aList[r]=l
        B = OrderedSet(aList)
        aList=list(copy.deepcopy(N)); aList[ index_forN ] = k
        N = OrderedSet(aList)
        
    return B,N
    

def  handle_P_Q(N, s_N, P, Q, k, l, t1, t2, thetaFlag):
    if (not P) and (not Q):
        #initialization, B and N are empty
        P, Q = OrderedSet([]), OrderedSet([])
        for i in range((len(N))):
            if s_N[i]<0:
                P.append(N[i])
        Q=N-P
        #print(P,Q)
        return P,Q
    else:
        if thetaFlag:
            #print(t1, P[t1])
            index_forN= N.index( P[t1] ) #; print(index_forN)
            P -= {l}
            Q |= {k}
        else:
            index_forN= N.index( Q[t2] )
            aList=list(copy.deepcopy(Q)); aList[t2]=k
            Q = OrderedSet(aList) 
            
        return P,Q, index_forN   

           
def computeMinRatiosIndex_checkTies(numeratorVector, denominatorVector, index_ordSet, greater_thanFlag, min_elFlag):
    
    candidates = []
    for i in range(len(denominatorVector)):
        if greater_thanFlag and denominatorVector[i]>0:
            candidates.append( numeratorVector[i] / (- denominatorVector[i]))
        elif not greater_thanFlag and denominatorVector[i]<0:
            candidates.append( numeratorVector[i] / (- denominatorVector[i]))
        else:
            candidates.append(float('inf'))#positive infinity
            
    if candidates:
        min_el = min(candidates) #; print(min_el)
    else:
        min_el = float('inf')
    index, element = -1, -1
    
    if min_el!=float('inf'):
        index_ordSet_temp = copy.deepcopy(index_ordSet) 
        pos = list(locate(candidates, lambda x: x == min_el)) #; print(pos, type(pos))
        
        if len(pos)>1:
            #check for ties
            index_ordSet_temp = [i for j, i in enumerate(index_ordSet_temp) if j in pos] #remove all elements except the competitives, which create the tie
            element = min(index_ordSet_temp)
            index = index_ordSet.index(element)
            #print(index_ordSet_temp)
        else:
            index=pos[0]
            element = index_ordSet[index]
        #print('index, element: ', index, element)
    if min_elFlag:
       return index, element, min_el 
    return index, element


def read_and_transform_problem(fileName):
        mps = smps.load_mps(fileName) #; print_mps_elements(mps)
        Eqin = convert_eqin(mps[5]) #; print(Eqin)
        A,c = mps[7], mps[6]
        if np.any(Eqin):
            A, Eqin, c = standarize_problem(mps[7], Eqin, mps[6])                  
        return A,  mps[9].get(mps[8][0]), c, Eqin, A.shape[0], A.shape[1] #A,b,c,Eqin,m,n
    
        
def main():
    '''
    partitioned_matrices_vectors: A_B, A_N, A_B_inv, x_B, c_B, c_N, w, s_N
    exteriorAlgorithms_elements: d_B, s0
    '''
    #mpsFile_names = ['sdata1_100x100.mps','sdata1_200x200.mps','sdata1_300x300.mps','sdata1_400x400.mps','sdata1_500x500.mps']
    mpsFile_names = ['example22.mps']
    #mpsFile_names = ['sdata1_100x100.mps']
    txtName='computational_study.txt'
    f= open(txtName, 'a')
    
    for fileName in mpsFile_names:
        
        '''
        Read mps and bring the problem in standard form. 
        '''
        A,b,c,Eqin,m,n = read_and_transform_problem(fileName) ; print(A, Eqin, b, c, m, n)   
        #print(A[:m, n-m:]) #A[2,:] --> row #test[:,0] --> column
        
        '''
        Initialize variable's values
        '''
        r, k, l, index_forN, t1, t2 = -1, -1, -1, -1, -1, -1
        initializationFlag, thetaFlag = True, False
        B,N, P, Q = OrderedSet(), OrderedSet(), OrderedSet(), OrderedSet()
        
        iterCount = 1 #count number of iterations
        f.write(fileName.strip('.mps')+':\t')
        
        start_time = time.time()
        while(True):

            if initializationFlag:
                B, N = handle_B_N(m, n, B, N, r, k, l, index_forN) #; print(B,N)
                A_B, A_N, A_B_inv, x_B, c_B, c_N, w, s_N = compute_partitioned_matrices_vectors(A, b, c, B, N) 
                P, Q = handle_P_Q(N, s_N, P, Q, k, l, t1, t2, thetaFlag) #; print(P,Q)
                initializationFlag=False
            else:
                P,Q, index_forN = handle_P_Q(N, s_N, P, Q, k, l, t1, t2, thetaFlag)
                B,N = handle_B_N(m, n, B, N, r, k, l, index_forN)
                A_B, A_N, A_B_inv, x_B, c_B, c_N, w, s_N = compute_partitioned_matrices_vectors(A, b, c, B, N) 
                
            #print(A_B);print(A_N); print(A_B_inv); print(x_B, c_B, c_N, w, s_N)
            #print(r); print(B,N,P,Q)  
            
            #optimality test
            if len(P)==0:
                s="The problem has optimal solution. (P == empty set)"
                print(s+'\n'); f.write(s+'\t')                
                break
            
            A_P, d_B, s0 = compute_exteriorAlgorithms_elements(A,P,A_B_inv,s_N, thetaFlag, r) #; print(d_B, s0) 
            #optimality test
            if not(np.any(d_B<0)) and s0==0:
                s="The problem has optimal solution. (d_B>=0 and s0==0)"
                print(s+'\n'); f.write(s+'\t')                
                break 
            
            ##### Pivoting
            
            '''
            Outcoming variable
            '''
            r,k = computeMinRatiosIndex_checkTies(x_B, d_B, B, False, False) #; print(r,k)
            #infinite solutions' test
            if r==-1:
                s="The problem is unbounded."
                print(s+'\n'); f.write(s+'\t')                  
                break
            
            '''
            Incoming variable
            '''            
            Hrp = A_B_inv[r,:].dot(A_P)
            A_Q = createArray_of_columns_indexed(A, Q, False) #; print(A_Q)
            Hrq=[]
            if Q:
                Hrq = A_B_inv[r,:].dot(A_Q)
            #print(Hrp, Hrq)
            
            #print('N: ', N, ' P: ',P, ' Q: ',Q); print('s_N: ',s_N)
            s_P = createArray_of_columns_indexed(s_N, N.index(P), True) #; print(s_P)
            s_Q = createArray_of_columns_indexed(s_N, N.index(Q), True) #; print(s_Q)
            t1, dummy, theta_1 = computeMinRatiosIndex_checkTies(s_P, Hrp, P, True, True)
            t2, dummy, theta_2 = computeMinRatiosIndex_checkTies(s_Q, Hrq, Q, False, True)            
            #print(t1, theta_1 ); print(t2, theta_2 )      
            '''
            comparing theta values
            '''
            if theta_1<=theta_2:
                l=P[t1]
                thetaFlag=True
            else:
                l=Q[t2]
                thetaFlag=False
            #print(l)
            
            iterCount+=1
          
        #while-loop has ended    
        totalTime=time.time() - start_time
        f.write('cpu time: '+str(totalTime)+'\ttotal number of iterations: '+str(iterCount) +'\n')
        
    #for-loop has ended        
    f.close()




if __name__ == "__main__":
    main()
