import datetime


fileName = "/home/nema/projectsAI/assignment1/Part 2/Assignment 1 Spain map.txt"
city1 = "Malaga"
city2 = "Valladolid"
mode=1 #1 for greedyBFS, 2 for Astar

class Connection:
    def __init__(self, A, B, distance):
        self.A=A
        self.B=B
        self.distance=distance

class Node:
    def __init__(self, city, straightLineDistance, parent) -> None:
        self.city=city
        self.straightLineDistance=straightLineDistance
        self.parent=parent

f = open(fileName, mode="r", encoding="utf-8")

def findNodeByCity(c, nodes):
    for node in nodes:
        if node.city==c:
            return node
    return None

def lowest(frontier): #returns the lowest distance node in the frontier
    min = frontier[0]
    minDistance = min.straightLineDistance
    for el in frontier:
        if el.straightLineDistance<minDistance:
            min = el
            minDistance = el.straightLineDistance
    return min

def expand(node, connections, nodes): #given a set of possible connections expands a node
    nextCities = []
    for connection in connections:
        if connection.A == node.city: # if there exists a connection from city A to another city B add B to the list of nodes => find B in the nodes
            nextNode=findNodeByCity(connection.B, nodes)
            nextCities.append(nextNode)
        elif connection.B == node.city:
            nextNode=findNodeByCity(connection.A, nodes)
            nextCities.append(nextNode)
    return nextCities

def findConnectionsByCity(node, connections, nodes):
    city = node.city
    result=[]
    for connection in connections:
        if connection.A == city:
            result.append(findNodeByCity(connection.B, nodes))
        elif connection.B == city:
            result.append(findNodeByCity(connection.A, nodes))
    return result

def refine1(solution, connections, nodes): #given the set of all lowest distance nodes
    i=len(solution)-1
    while i>=0:
        if i!=len(solution)-1 and i!=0: #simply check that the current city can be reached from the one before that
            followers = findConnectionsByCity(solution[i], connections, nodes) #followers of the current city
            if solution[i+1] not in followers:
                solution.remove(solution[i])
        i-=1
    return solution


def invertList(list):
    tmp = []
    i=len(list)-1
    while i>=0:
        tmp.append(list[i])
        i-=1;
    return tmp

def refine(solution):
    last = solution[-1] #start from the end node and find the parents
    newSol = []
    newSol.append(last)
    curr = last.parent
    while curr!=None and curr.city!=city1:
        newSol.append(curr)
        curr = curr.parent
    if curr.city==city1:
        newSol.append(curr)
    lst = invertList(newSol)
    return lst       

def GreedyBestFirstSearch(nodes, connections):
    frontier = [] #list of all possible nodes from which the one with the lowest distance shall be picked
    frontier.append(findNodeByCity(city1, nodes)) #initially only the starting city is in the frontier
    solution = [] #the solution will be composed of the lowest distance connections
    while not findNodeByCity(city2, frontier) and frontier!=None and len(frontier)!=0: 
        greedyChoice = lowest(frontier)
        nextCities = expand (greedyChoice, connections, nodes)
        frontier.remove(greedyChoice)
        solution.append(greedyChoice)
        for node in nextCities:
            node.parent = greedyChoice
            frontier.append(node)
            
    n2=findNodeByCity(city2, nodes)
    n2.parent = solution[-1]
    if n2 in frontier:
        solution.append(n2)
    solution = refine1(solution, connections, nodes)
    return solution


def AStar(nodes, connections): 
    solution=[]
    frontier=[]
    frontier.append(findNodeByCity(city1, nodes))
    while not findNodeByCity(city2, frontier) and frontier!=None and len(frontier)!=0: #while the arriving city is not in the frontier
        greedyChoice = lowest(frontier)
        nextCities = expand (greedyChoice, connections, nodes)
        frontier.remove(greedyChoice)
        if greedyChoice!=None:
            solution.append(greedyChoice)
        for node in nextCities:
            if node!=None:
                newNode = Node(node.city, node.straightLineDistance +computeDistanceAtoB(node, greedyChoice, connections), greedyChoice) 
                frontier.append(newNode)
                
    n2=findNodeByCity(city2, nodes)
    n2.parent = solution[-1]

    solution.append(n2)
    
    #solution = refine(solution, connections, nodes)
    solution = refine(solution)
    return solution



def getConnectionAtoB(A, B, connections):
    for con in connections:
        if con.A== A.city and con.B==B.city or con.B==A.city and con.A==B.city:
            return con
    return None

def computeDistanceAtoB(A, B, connections): # where A and B are nodes
    c1 = getConnectionAtoB(A, B, connections)
    if c1!=None:
            return c1.distance
    return 0



line=""
while line!="\n":
    line=f.readline()

line=f.readline()
connections=[]
#start parsing
line=f.readline()
while line!="\n":
    elems=line.split(" ")
    connection=Connection(elems[0], elems[1], int(elems[2]))
    connections.append(connection)
    line=f.readline()

straightLines = []
line=f.readline()
for line in f.readlines():
    elems=line.split(" ")
    straightLine=Node(elems[0], int(elems[1]), None)
    straightLines.append(straightLine)
f.close()

#start timer
start = datetime.datetime.now()
if mode==1:
    sol = GreedyBestFirstSearch(straightLines, connections)
else:
    sol = AStar(straightLines, connections)
i=0
totDist=0
while i<len(sol)-1:
    dist = computeDistanceAtoB(sol[i], sol[i+1], connections)
    print(sol[i].city,"->",sol[i+1].city, dist)
    totDist+=dist
    i+=1
print(sol[i].city, 0)
print("total distance=", totDist)

end = datetime.datetime.now()
print(end - start)

    