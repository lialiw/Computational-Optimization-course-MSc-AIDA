# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 13:35:30 2021

@author: Fik
"""

"""

Code used from:
    https://github.com/jmaerte/pysmps/tree/master/pysmps

Sources:
    https://pypi.org/project/pysmps/
    https://github.com/jmaerte/pysmps
    https://www.cenapad.unicamp.br/parque/manuais/OSL/oslweb/features/featur11.htm
    https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/
    https://stackoverflow.com/questions/1038824/how-do-i-remove-a-substring-from-the-end-of-a-string
    
Instructions: 
    If the package pysmps is nοt already installed in your 
    computer, install it by using PyPI with the command:
        pip install pysmps
        
"""


from pysmps import smps_loader as smps
import numpy as np
from math import *


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
    
    '''
    print(aDic)
    print(LO_list)
    print(UP_list)
    print(xNames)
    '''
    
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
 
    
def main():

    #mpsFile_names = ['afiro.mps', 'aircraft.mps', 'deter0.mps', 'deter1.mps','sc205-2r-8.mps','sc205-2r-50.mps','scagr7-2b-64.mps']
    mpsFile_names =  ['example1.mps']
    #mpsFile_names = ['Lp01.mps', 'Lp02.mps']
    problem_matrices_names = ['A','b','c', 'Eqin']
    
    for fileName in mpsFile_names:
        
        mps = smps.load_mps(fileName)
        #print_mps_elements(mps)
        eqinArray= convert_eqin(mps[5])
        problem_elements_numpyArrays = [mps[7], mps[9].get(mps[8][0]), mps[6], eqinArray ]
        write_txt(fileName,problem_matrices_names, problem_elements_numpyArrays, mps)           

        

if __name__ == "__main__":
    main()
