# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 20:39:37 2021

@author: Fik
"""

'''
Sources:
    https://www.kite.com/python/answers/how-to-remove-empty-lines-from-a-string-in-python
    https://stackoverflow.com/questions/4435169/how-do-i-append-one-string-to-another-in-python
    
'''


def readProblem(fileName, charsDropped, problemElems):
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
            problemElems[flag].append( line.split())
    f.close()        
    return problemElems


    
def find_varNames(bounds, numVars):
    
    varNames = ['X'+str(i+1) for i in range(numVars)] #; print(varNames)
    if bounds:
        for bo in bounds:
            #print(type(bo[0]))
            if bo[0] not in varNames:
                #print(type(bo[0]))
                var_name=''.join( [char for char in bo[0] if char.isalpha()] )
                ith_var=''.join( [ char for char in bo[0] if char.isdigit()] )
                varNames[ int(ith_var)-1] = ''.join((var_name,ith_var))
                #print(var_name, ith_var); print(varNames)
        
        #print(bounds[0]); print(numVars)
    return varNames


def createRowsEqin(eqin_list):
    
    constraintNames = ['R'+str(i+1) for i in range(len(eqin_list))] #; print(constraintNames)
    eqin_dict= {'1':'G', '-1':'L', '0':'E'}
    eqinArray=[]
    for i in range(len(eqin_list)):
        eqinArray.append([ eqin_dict[eqin_list[i][0] ], constraintNames[i] ])
        
    eqinArray=[["N", "OBJ"]]+eqinArray
    #print(eqinArray)
    return constraintNames, eqinArray


def createRowsA(varNames, constraintNames, A, c):
    colArray = []
    for j in range(len(c)):
        for i in range(len(A)):
            if A[i][j]!=0:
                colArray.append([varNames[j], constraintNames[i], A[i][j]])
        colArray.append([varNames[j], "OBJ",c[j][0]])
    '''    
    for el in colArray:
        print(el)
    '''
    return colArray


def createRHS(constraintNames,b):
    
    rhs_section=[]
    for i in range(len(b)):
        rhs_section.append( [ "RHS1", constraintNames[i], b[i][0]])
    #print(rhs_section)
    return rhs_section


def createBounds(_BS):
    bounds_section=[]
    for i in range(len(_BS)):
        bounds_section.append([_BS[i][1],"BND1",_BS[i][0], _BS[i][2]])
    return bounds_section

    
def write_mps(fileName, minMax, varNames, constraintNames, row_section, cols_section, rhs_section, bounds_section):
        
    with open(fileName, "w") as f:
        f.write("*MinMax:" + minMax + "\n")
        f.write("NAME\t\t" + row_section[0][1]+ "\n")

        f.write("ROWS\n")
        for el in row_section:
            #print(el[0], el[1])
            f.write(' '+el[0]+'  '+el[1] +'\n' )
        #'''
        f.write("COLUMNS\n")
        for el in cols_section:
            f.write('    '+el[0]+' '+el[1] +'\t\t'+el[2]+'\n' )
        
        f.write("RHS\n")
        for el in rhs_section:
            f.write('\t'+el[0]+' '+el[1] +'\t\t'+el[2]+'\n' )
        
        if bounds_section:
            f.write("BOUNDS\n")
            for el in bounds_section:
                #print(el[0],el[3],el[2])
                if el[3]!='None':
                    f.write('\t'+el[0]+' '+el[1] +'\t\t'+el[2]+' '+el[3]+'\n' )
                else:
                    f.write('\t'+el[0]+' '+el[1] +'\t\t'+el[2]+'\n' )
        #'''
        f.write("ENDATA\n")


def main():

    txtNames=['Lp01.txt', 'Lp02.txt']
    #txtNames=['example1.txt']
    
    for fileName in txtNames:
        
        charsDropped = '=[]'
        problemElems ={'A': [],'b': [],'c': [],'Eqin': [],'MinMax':[],'Ran':[], 'BS':[]}
        problemElems = readProblem(fileName, charsDropped, problemElems) #; print(problemElems)
        
        '''
        for key in problemElems.keys():
            print(key, problemElems[key])
            print('\n')
        #'''
        

        varNames = find_varNames(problemElems['BS'], len(problemElems['c'])) #; print(varNames,'\n')
        
        '''
        print(problemElems['Eqin'])
        for i in range((len(problemElems['Eqin']))):
            print(problemElems['Eqin'][i])
        '''
        
        #'''
        constraintNames, row_section = createRowsEqin(problemElems['Eqin']) #; print(row_section, '\n')
        cols_section = createRowsA(varNames,constraintNames, problemElems['A'], problemElems['c']) #; print(cols_section, '\n')    
        rhs_section = createRHS(constraintNames, problemElems['b']) #; print(rhs_section, '\n')
        
        if problemElems['BS']:
            bounds_section = createBounds(problemElems['BS']) #; print(bounds_section, '\n')
        #print('\n')
        mpsName = fileName.strip('txt')+'mps'
        #print(problemElems['MinMax'][0][0])
        write_mps(mpsName, problemElems['MinMax'][0][0], varNames, constraintNames, row_section, cols_section, rhs_section, bounds_section)
       #''' 
        
if __name__ == "__main__":
    main()

    