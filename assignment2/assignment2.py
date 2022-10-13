import datetime


squareStart = [0, 3, 6, 27, 30, 33, 54, 57, 60] #starting indexes of each square
fileName = "Assignment 2 sudoku.txt"


def complete(currSol):
    for el in currSol:
        if el==0:
            return False
    return True

def selectUnassignedVariable(currentSolution):
    i=0
    while i<len(currentSolution):
        if currentSolution[i]==0:
            return i
        i+=1

def orderDomainValues(currentSolution, var):
    i=currentSolution[var]
    if i!=0:
        return i
    
    
   

def checkRows(currentSolution, value, var):
    row=0
    for h in range(0, 73, 9):
        if var in range(h, h+9):
            row=h
            break
    for i in range(row, row+9):
        if currentSolution[i]==value and i!=var:
            return False
    return True

def checkColumns(currentSolution, value, var):
    col=0
    for h in range(0, 9):
        if var in range(h, h+73, 9):
            col=h
            break
    for i in range(col, col+73, 9):
        if currentSolution[i]==value and i!=var:
            return False
    return True

def checkSquare(currentSolution, value, var):
    square=0
    flag=0
    for i in squareStart: 
        for j in range(i, i+19, 9):
            if var in range(j, j+3):
                square=i
                flag=1
                break
        if flag==1:
            break
        
    
    for i in range(square, square+19, 9):
        for j in range(i, i+3):
            if currentSolution[j]==value and j!=var:
                return False
    return True


def consistent(value, currentSolution, var):
    if checkRows(currentSolution, value, var) and checkColumns(currentSolution, value, var) and checkSquare(currentSolution, value, var):
        return True
    return False

def emptyCells(set):
    i=0
    empty=[]
    while i<len(set):
        if set[i]==0:
            empty.append(i)
        i+=1
    return empty   

def getRow(currentSolution, i):
    res = currentSolution[i*9: i*9+(i+9)-i]
    return res

def getColumn(sol, i):
    res = []
    for j in range(i, i+73, 9):
        res.append(sol[j])
    return res

def missingValue(collection):
    target = list(range(1,10))
    for el in collection:
        if el in target:
            target.remove(el)
    return target[0] #there should be just 1 missing element 

def getCommonValues(rows):#only works with a 3*9 matrix
    if(len(rows)!=3):
        return "Failure"
    common=[]
    for el in rows[0]:
        if (el in rows[1] or el in rows[2]) and el!=0:
            common.append(el)


def inference(currentSolution): #if in the currentSolution just 1 cell (in a row, column or square) is not filled i'm able to infer what to fill a certain cell with
    inferredSolution = currentSolution.copy()
    selectedRowValues=[]
    selectedRows=[]

    for i in range(0, 9): #check every row and see if it has just 1 empty cell, check every column and see if it has just 1 empty cell
        row=getRow(inferredSolution, i)
        if len(emptyCells(row))==1:
            var = selectUnassignedVariable(row)
            inferredSolution[i*9+var]=missingValue(row)
           
        col = getColumn(inferredSolution, i)
        if len(emptyCells(col))==1:
            var = selectUnassignedVariable(col)
            inferredSolution[i+var*9]=missingValue(col)
            

    for i in squareStart:
        square=[]
        for j in range(i, i+19, 9):
            for k in range(j, j+3):
                square.append(inferredSolution[k])
        if len(emptyCells(square))==1:

            var = selectUnassignedVariable(square)
            if var in list(range(0,3)):
                inferredSolution[var+i] = missingValue(square)
            elif var in list(range(3, 6)):
                inferredSolution[var%3+i+9] = missingValue(square)
            elif var in list(range(6, 9)):
                inferredSolution[var%3+i+18] = missingValue(square)
            else:
                print("Error in inferring missing value of square: ", square)
        
    for i in range(len(inferredSolution)):
        if inferredSolution[i]!=0 and not consistent(inferredSolution[i],inferredSolution,i):
            #print("value ", i, "made me fail :(")
            return "failure"
    return inferredSolution
    


def backtrack(currentSolution):
    if complete(currentSolution): 
        return currentSolution
    var = selectUnassignedVariable(currentSolution)
    for value in orderDomainValues(currentSolution, var):
        backup = currentSolution.copy()
        if consistent(value, currentSolution, var):
            currentSolution[var]=value
            inferences = inference(currentSolution)
            if inferences != "failure":
                currentSolution = inferences.copy()
                result = backtrack(currentSolution)
                if result != "failure":
                    return result
        currentSolution = backup.copy()
    return "failure"

#parsing
f = open(fileName, mode="r", encoding="utf-8")  
sudokus=[]

line=f.readline()
while line!="\n":
    line=f.readline()

line=f.readline()
while line!="EOF\n":
    line=f.readline()
    sudoku=[]
    while line!="\n":
        for c in line:
            if c!="\n":
                sudoku.append(int(c))
        line=f.readline()
    sudokus.append(sudoku)
    line=f.readline()

f.close()

#start timer
start = datetime.datetime.now().second

for sudoku in sudokus:
    print(backtrack(sudoku))

end = datetime.datetime.now().second
print((end - start))

