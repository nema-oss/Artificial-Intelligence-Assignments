from cmath import sqrt
import random
from numpy import number
import matplotlib.pyplot as plt


inputFile="Assignment 3 berlin52.tsp"
tau = 5
numberOfAnts = 20
max_iterations = 100
alfa = 1
beta = 1
evaporation  = 0.3

class City():
    def __init__(self,id, x, y) -> None:
        self.id=id
        self.x=x
        self.y=y


class Ant():
    def __init__(self, visited) -> None:
        self.visited=visited
        self.visitedEdges = []
        self.cost = 0

class Edge():
    def __init__(self, start, end) -> None:
        self.start=start
        self.end = end
        self.tau=tau
        self.cost = distance(start, end)


def initialize():
    ants = []
    for i in range(numberOfAnts):
        cit = []
        cit.append(cities[0])
        ant = Ant(cit)
        ants.append(ant)
    return ants

def distance(a, b):
    return sqrt(pow(b.x-a.x, 2) + pow(b.y-a.y,2)).real

def isItLastEdge(e, ant):
    return len(ant.visited)==len(cities)-1

def transitionRule(ant):
    probs = []
    selectedEdges = []
    r = ant.visited[-1]
    summ = 0
    for e in edges:
        s=e.end
        if s not in ant.visited and e.start == r and (s.id!=1 or (s.id==1 and isItLastEdge(e, ant))):
            eta = 1 / e.cost
            summ += pow(e.tau, alfa)*pow(eta, beta)

    for e in edges:
        s=e.end
        if s not in ant.visited and e.start == r and (s.id!=1 or (s.id==1 and isItLastEdge(e, ant))):
            selectedEdges.append(e)
            eta = 1 / e.cost
            p = pow(e.tau, alfa)*pow(eta, beta)/summ
            probs.append(p)
    if len(selectedEdges)>0:

        next = random.choices(selectedEdges, probs)[0]
        ant.visitedEdges.append(next)
        return next   
    return 0

def pheromoneUpdate(e):
    sumDeltas = 0
    for ant in ants:
        if e in ant.visitedEdges:
            sumDeltas+=1/ant.cost
    
    res = (1-evaporation)*e.tau+sumDeltas
    e.tau = res

f=open(inputFile, mode="r", encoding="utf-8")
cities=[]
for line in f.readlines():
    sL=line.split(" ")
    n = City(int(sL[0]), float(sL[1]), float(sL[2]))
    cities.append(n)
cities.append(City(1, cities[0].x, cities[0].y))
f.close()
#initialize the edges
edges = []
for i in range(len(cities)):
    for j in range(len(cities)):
        if cities[i].id!=cities[j].id:
            e = Edge(cities[i], cities[j])
            edges.append(e)
            

x=[]
y=[]
for i in range(max_iterations):
    print("iteration ", i)
    ants = initialize()
    print("transitioning")
    for j in range(0, len(cities)-1):
        #print("transition at city : ", cities[j].id)
        for k in range(numberOfAnts):
            e = transitionRule(ants[k])
            if e!=0:
                ants[k].cost+=e.cost
                ants[k].visited.append(e.end)
            #print("transition done for ant ", k, "/", numberOfAnts, "on city ", cities[j].id)
    
    actualBest = ants[0]
    print("cost update")
    for ant in ants:
        if ant.cost<actualBest.cost:
            actualBest = ant
    print("pheromone update")
    for edge in edges:
        pheromoneUpdate(edge)

    if i==0:
        globalBest = actualBest
    elif actualBest.cost < globalBest.cost:
        globalBest = actualBest
    y.append(globalBest.cost)
    x.append(i)
    print(globalBest.cost)
    for c in globalBest.visited:
        print(c.id, end="->")
    print("\n")


fig=plt.figure(figsize=(24, 24), dpi=60)
ax = fig.add_subplot(111)

s="Evolution of the cost of the global best over the generations"
ax.plot(x,y)
ax.set_title(s)

plt.savefig("ant.png")
plt.close()

