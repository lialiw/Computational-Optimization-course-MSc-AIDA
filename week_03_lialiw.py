# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 18:27:09 2021

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
Sources kouskouveli_week(3):
    https://numpy.org/doc/stable/reference/generated/numpy.count_nonzero.html
    https://numpy.org/doc/stable/reference/generated/numpy.divide.html
    https://thispointer.com/delete-elements-rows-or-columns-from-a-numpy-array-by-index-positions-using-numpy-delete-in-python/
    https://note.nkmk.me/en/python-numpy-delete/
    https://stackoverflow.com/questions/18688948/numpy-how-do-i-find-total-rows-in-a-2d-array-and-total-column-in-a-1d-array
    https://numpy.org/doc/stable/reference/generated/numpy.copy.html
"""


from pysmps import smps_loader as smps
import numpy as np
from math import *
import gc

def print_mps_elements(mps):
    for i in range(len(mps)):
        if i!=4:
            print( i, type(mps[i]), mps[i])
    
    
def convert_eqin(eqin_list):
    eqin_dict= {'G':1, 'L':-1, 'E':0}
    eqinArray=[]
    for eqin in eqin_list:
        eqinArray.append(eqin_dict[eqin])
    return np.array(eqinArray)


def create_boundMatrix(aDic, xNames):
    LO_list=list(aDic['LO'])
    UP_list=list(aDic['UP'])
    #print(aDic); print(LO_list); print(UP_list); print(xNames)    
    
    varNames, bound_type, value = [],[],[]
    
    for i in range(len(LO_list)):
        if LO_list[i]==UP_list[i]:
            varNames.append(xNames[i])
            bound_type.append('FX')
            value.append(LO_list[i])
        elif LO_list[i]==-inf and UP_list[i]==inf:
            varNames.append(xNames[i])
            bound_type.append('FR')
            value.append('None')
        elif not(LO_list[i]==0 and UP_list[i]==inf):
            if LO_list[i]!=-inf:
                varNames.append(xNames[i])
                bound_type.append('LO')
                value.append(LO_list[i])         
            if  UP_list[i]!=inf:
                varNames.append(xNames[i])
                bound_type.append('UP')
                value.append(UP_list[i])            
    #print(varNames, bound_type, value)
    return varNames, bound_type, value


def write_txt(fileName,problem_matrices_names, problem_elements_numpyArrays, mps):
    
        txtName = fileName.strip('mps')+'txt'
        f = open(txtName, "w")
        
        for i in range(len(problem_elements_numpyArrays)):
            f.write(problem_matrices_names[i])      
            np.savetxt(f,problem_elements_numpyArrays[i], delimiter='\t', fmt='%s', header=' = [', footer = ']', comments='')
            f.write('\n')        
        f.write('MinMax= -1\n')
        

        print(problem_elements_numpyArrays)#A,b,c,Eqin
        
        if mps[10]:
            f.write('\n')
            f.write('BS = [')
            aDic=mps[11].get(mps[10][0])
            #print(aDic)
            varNames, bound_type, value = create_boundMatrix(aDic, mps[3])
            #print(varNames, bound_type, value)
            for i in range(len(varNames)):
                f.write(varNames[i] +' '+ bound_type[i]+ ' '+str(value[i]) +"\n")
            f.write(']\n')    
        f.close()


def find_k_ton_candidateRow(Eqin,A,k):
    #traversing from the last to the first row
    i,j = A.shape
    i-=1; j-=1
    while(i>-1):
        if Eqin[i]==0 and np.count_nonzero(A[i])==k:
            break
        i-=1
    if i!=-1:
        while(j>-1):
            if A[i][j] !=0:
                break
            j-=1        
    return i,j


def apply_k_or_single_ton_inRow(k, c0, A, b, c, Eqin, candidate_row, candidate_col):
    #print(A, b)
    m,n= A.shape# number of rows, number of cols
    b[candidate_row] = b[candidate_row] / A[candidate_row][candidate_col]
    A[candidate_row] = np.true_divide(A[candidate_row], A[candidate_row][candidate_col])#; print( np.true_divide(A[candidate_row], A[candidate_row][candidate_col]) )
    #print(A); print(b)

    if c[candidate_col]!=0:
        c0 += b[candidate_row] * c[candidate_col]
        c-= A[candidate_row] * c[candidate_col]
    c = np.delete(c, candidate_col)
    
    for i in range(m):
        if i!=candidate_row:
            if A[i][candidate_col]!=0:
                b[i] -=  b[candidate_row] * A[i][candidate_col]
                A[i] -=  A[candidate_row] * A[i][candidate_col]
    #A[candidate_row][candidate_col], Eqin[candidate_row] = 0, -1

    A = np.delete(A, candidate_col, 1)
    if k==1:
        A = np.delete(A, candidate_row, 0)
        b = np.delete(b, candidate_row, 0)
        Eqin = np.delete(Eqin, candidate_row, 0)
    else:
        Eqin[candidate_row] = -1
    gc.collect()
    return A, b, c, Eqin, c0
    

def applyK_ton(k, A, b, c, Eqin):
    c0 = 0
    if not k:
        k = int(input("Please enter k to apply k-ton for all ks in range (k,1,-1):\n"))  
    while(True):
        candidate_row, candidate_col = find_k_ton_candidateRow(Eqin, A, k)#; print(candidate_row, candidate_col)
        if candidate_row==-1:
            if k>1 :
                k-=1
                continue
            else:
                break 
        A, b , c, Eqin, c0 = apply_k_or_single_ton_inRow(k, c0, A, b, c, Eqin, candidate_row, candidate_col)
    gc.collect()
    return A,b,c,Eqin,c0


def main():

    mpsFile_names = ['afiro.mps', 'aircraft.mps', 'deter0.mps', 'deter1.mps','sc205-2r-8.mps','sc205-2r-50.mps','scagr7-2b-64.mps']
    #mpsFile_names =  ['example1.mps']# page 17, Lecture03.pdf
    #mpsFile_names = ['afiro.mps']
    problem_matrices_names = ['A','b','c', 'Eqin']
    txtName = 'computational_study.txt'
    
    k=6
    f = open(txtName, "a+")
    f.write('Problem \tBefore presolve')
    for i in range(1,k):
        f.write(' \tAfter presolve k='+str(i))
    f.write('\n\t')
    for i in range(1,k):
        f.write(' \tRows Cols Nonzeros')
    f.write('\n')
    
   
    for fileName in mpsFile_names:
            
        mps = smps.load_mps(fileName)
        #print_mps_elements(mps)
        eqinArray= convert_eqin(mps[5])
        problem_elements_numpyArrays = [mps[7], mps[9].get(mps[8][0]), mps[6], eqinArray ] #A,b,c,Eqin
        #write_txt(fileName,problem_matrices_names, problem_elements_numpyArrays, mps) 

        #Applying k-ton

        for i in range(1,k):
            A, b = np.array(problem_elements_numpyArrays[0], copy=True), np.array(problem_elements_numpyArrays[1], copy=True)
            c, Eqin = np.array(problem_elements_numpyArrays[2], copy=True), np.array(eqinArray, copy=True)
            if i==1:
                f.write(fileName.strip('.mps')+' \t\t'+str(A.shape[0])+'    '+str(A.shape[1])+'    '+str(np.count_nonzero(A))+'    ')
            #print(A); print(b); print(c); print(Eqin);
            A, b, c, Eqin, c0 = applyK_ton(i, A, b, c, Eqin)#; print(i+1, A.shape,np.count_nonzero(A))
            f.write(' \t'+str(A.shape[0])+'    '+str(A.shape[1])+'    '+str(np.count_nonzero(A))+'    ')
            #print(A); print(b); print(c); print(Eqin); print(c0); print('\n\n')
        f.write('\n\n') 
            
        '''
        A, b = np.array(problem_elements_numpyArrays[0], copy=True), np.array(problem_elements_numpyArrays[1], copy=True)
        c, Eqin = np.array(problem_elements_numpyArrays[2], copy=True), np.array(eqinArray, copy=True)
        A, b, c, Eqin, c0 = applyK_ton(k, A, b, c, Eqin)#; print(i+1, A.shape,np.count_nonzero(A))
        print(A); print(b); print(c); print(Eqin); print(c0); print('\n\n')
        print(np.count_nonzero(A))
        '''
        
    f.close()


        
        
if __name__ == "__main__":
    main()
