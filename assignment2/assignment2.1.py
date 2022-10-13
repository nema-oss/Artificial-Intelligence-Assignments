import datetime
import time

fileName = "Assignment 2 sudoku.txt"

def complete(currSol):
    for row in currSol:
        for el in row:
            if el==0:
                return False
    return True

def getSquare(var):
    square=[0,0]
    if var[0]<=2 :
        if var[1]<=2:
            square=[0,0] #[0,0]->[2,2]
        elif var[1]<=5:
            square=[0,3] #[0,3]->[2,5]
        elif var[1]<=8:
            square=[0,6] #[0,6]->[2,8]
    elif var[0]<=5:
        if var[1]<=2:
            square = [3,0] #[3,0]->[5,2]
        elif var[1]<=5:
            square = [3,3] #[3,3]->[5,5]
        elif var[1]<=8:
            square=[3,6] #[3,6]->[5,8]
    elif var[0]<=8:
        if var[1]<=2:
            square = [6,0]
        elif var[1]<=5:
            square = [6,3]
        elif var[1]<=8:
            square=[6,6]
    return square

def getSquares(currentSolution):
    squares=[]
    for i in range(0, 9, 3):
        for h in range(0,9,3):
            square=[]
            for j in range(0,3):
                for k in range(3):
                    square.append(currentSolution[i+j][k+h])
            squares.append(square)
    return squares

def emptyCells(set):
    i=0
    empty=[]
    while i<len(set):
        if set[i]==0:
            empty.append(i)
        i+=1
    return empty  

def missingValue(collection):
    target = list(range(1,10))
    for el in collection:
        if el in target:
            target.remove(el)
    return target[0] #there should be just 1 missing element  

def getLowest(e):
    m=max(e)
    target=0

    for i in range(9):
        if e[i]<=m and e[i]!=0:
            target=i
            m=e[i]
    return [m, target]

def selectUnassignedVariable(currentSolution):
    #find the square that has the fewest free cells -> find the unit with the fewest free cells, it's better.
    squares=getSquares(currentSolution)
    emptyCellsRows=[]
    for i in range(9):
        emptyCellsRows.append(len(emptyCells(currentSolution[i])))

    emptyCellsColumns=[]
    for i in range(9):
        emptyCellsColumns.append(len(emptyCells(getColumn(currentSolution, i))))

    emptyCellsSquares=[]
    for square in squares:
        emptyCellsSquares.append(len(emptyCells(square)))

    
    lowestSquare=getLowest(emptyCellsSquares)
    lowestRow = getLowest(emptyCellsRows)
    lowestColumn = getLowest(emptyCellsColumns)

    if lowestColumn[0]<lowestRow[0] and lowestColumn[0]<lowestSquare[0] and lowestColumn[0]!=0:
        j = lowestColumn[1]
        for i in range(9):
            if currentSolution[i][j]==0:
                return [i, j]

    elif lowestRow[0]<lowestColumn[0] and lowestRow[0]<lowestSquare[0] and lowestRow[0]!=0:
        i = lowestRow[1]
        for j in range(9):
            if currentSolution[i][j]==0:
                return [i, j]
    
    target = lowestSquare[1]
    startI=target//3*3
    startJ=target%3*3
    for i in range(startI, startI+3):
        for j in range(startJ, startJ+3):
            if currentSolution[i][j]==0:
                return [i,j]

def getColumn(matrix, j):
    col=[]
    for i in range(0, len(matrix)):
        col.append(matrix[i][j])
    return col


class Node:
    def __init__(self, id, value) -> None:
        self.id=id
        self.value=value

def best(solution):
    res=[]
    for i in range(1, 10):
        node=Node(i, 0)
        count=0
        for row in solution:
            for el in row:
                if el==i:
                    count+=1
        node.value=count
        res.append(node)
    sol=[]
    for node in sorted(res, key=lambda x: x.value, reverse=True):
        sol.append(node.id)
    return sol

def orderDomainValues(currentSolution, var):
    h=currentSolution[var[0]][var[1]]
    if h!=0:
        return [h]
    domain=[]
    col = getColumn(currentSolution, var[1])
    square = getSquare(var)
    submatrix = []
    for i in range(square[0], square[0]+3):
        for j in range(square[1], square[1]+3):
            submatrix.append(currentSolution[i][j])
        
    for n in best(currentSolution):
        if n not in currentSolution[var[0]] and n not in col and n not in submatrix:
            domain.append(n)
        
    return domain
    
    
   

def checkRows(currentSolution, value, var):
    row=currentSolution[var[0]]
    for i in range(len(row)):
        if row[i]==value and i!=var[1]:
            return False
    return True

def checkColumns(currentSolution, value, var):
    col=[]
    for i in range(len(currentSolution)):
        for j in range(len(currentSolution[i])):
            if j==var[1]:
                col.append(currentSolution[i][j])
    
    for i in range(len(col)):
        if col[i]==value and i!=var[0]:
            return False
    return True

def checkSquare(currentSolution, value, var):
    square=getSquare(var)
    
    for i in range(square[0], square[0]+3):
        for j in range(square[1], square[1]+3):
            if currentSolution[i][j]==value and i!=var[0] and j!=var[1]:
                return False
    return True
    



def inference(currentSolution): #if in the currentSolution just 1 cell (in a row, column or square) is not filled i'm able to infer what to fill a certain cell with
    inferredSolution = [row[:] for row in currentSolution]
    
    for i in range(len(inferredSolution)):
        for j in range(len(inferredSolution[i])):
            d = orderDomainValues(inferredSolution, [i,j])
            if len(d)==1:
                inferredSolution[i][j] = d[0]

    for i in range(0, 9): #check every row and see if it has just 1 empty cell, check every column and see if it has just 1 empty cell
        row=inferredSolution[i]
        empty=emptyCells(row)
        if len(empty)==1:
            inferredSolution[i][empty[0]]=missingValue(row)
         
        col = getColumn(inferredSolution, i)
        empty=emptyCells(col) 
        if len(empty)==1:
            inferredSolution[empty[0]][i]=missingValue(col)

    squares=getSquares(currentSolution)
    for i in range(9):
        empty=emptyCells(squares[i])
        if len(empty)==1:
            index = empty[0]
            if index<3:
                inferredSolution[i//3*3][i%3*3+index]=missingValue(squares[i])
            else:
                inferredSolution[i//3*3+index//3][i%3*3+index%3]=missingValue(squares[i])

       
    for i in range(len(inferredSolution)):
        for j in range(len(inferredSolution[i])):
            if inferredSolution[i][j]!=0 and not consistent(inferredSolution[i] [j],inferredSolution,[i,j]):
            #print("value ", i, "made me fail :(")
                return "failure"
    return inferredSolution


def consistent(value, currentSolution, var):
    if checkRows(currentSolution, value, var) and checkColumns(currentSolution, value, var) and checkSquare(currentSolution, value, var):
        return True
    return False

def backtrack(currentSolution):
    if complete(currentSolution): 
        return currentSolution
    var = selectUnassignedVariable(currentSolution)
    for value in orderDomainValues(currentSolution, var):
        backup = [row[:] for row in currentSolution]
        if consistent(value, currentSolution, var):
            currentSolution[var[0]][var[1]]=value
            inferences = inference(currentSolution)
            if inferences != "failure":
                currentSolution = [row[:] for row in inferences]
                result = backtrack(currentSolution)
                if result != "failure":
                    return result
        currentSolution = [row[:] for row in backup]
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
        row=[]
        for c in line:
            if c!="\n":
                row.append(int(c))
        sudoku.append(row)
        line=f.readline()
    sudokus.append(sudoku)
    line=f.readline()

f.close()

#start timer
start = datetime.datetime.now()

for sudoku in sudokus:
    print(backtrack(sudoku))

end = datetime.datetime.now()

print(end - start)
