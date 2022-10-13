from cmath import sqrt
from math import ceil, floor
import random   
import matplotlib.pyplot as plt



inputFile="Assignment 3 berlin52.tsp"
maxFitness = 250000
out = "output.txt"
out2 = "params.txt"
mutationThreshold = 1#if the best solution doesn't decrease by this parameter during genBetterRate generation(s), make the mutation rate higher; but if it does, decrease the population
genBetterRate = 1#every x generations the best solution should decrease of at least mutationRate
runs=10
startSize = 2
delta = 128
fm = open(out2, mode="a", encoding="utf-8")
genFitnesses=[]
f2 = open(out, mode="w", encoding="utf-8")
failed=0
class City():
    def __init__(self,id, x, y) -> None:
        self.id=id
        self.x=x
        self.y=y

class Individual():
    def __init__(self, cities):
        self.cities=cities
        self.fitness=0
        self.probability=0.0
    def setFitness(self, value):
        self.fitness=value
    def setProbability(self, probability):
        self.probability=probability
    def copy(self):
        cits = []
        for city in self.cities:
            newC = City(city.id, city.x, city.y)
            cits.append(newC)
        return Individual(cits)

    

def randomize(l):
    elems=l.copy()
    res=[]
    res.append(elems[0])
    elems.remove(elems[0])
    while len(elems)!=0:
        i=random.randint(0, len(elems)-1)
        res.append(elems[i])
        elems.remove(elems[i])
    res.append(res[0])
    return res

def distance(a,b):
    return sqrt(pow(b.x-a.x, 2) + pow(b.y-a.y,2))

def fitness(cities):
    global fitnessValuations
    fitnessValuations+=1
    d=0
    for i in range(len(cities)-1):
        d+=distance(cities[i], cities[i+1])

    return d.real

def getParents(generation):
    parents=[]
    while len(parents)<len(generation):
        probs = [o.probability for o in generation]
        parent1 = random.choices(generation, probs)[0]
        parent2 = random.choices(generation, probs)[0]
        while parent1==parent2:
            parent2 = random.choices(generation, probs)[0]
        if([parent1, parent2] not in parents):
            parents.append([parent1, parent2])
    return parents

def seeIndividual(individual):
    for c in individual.cities:
        print(c.id, end=" ")
    print("\n", end="")

def crossover(parents):
    offsprings=[]

    for p in parents:
        crossoverStartIndex = random.randint(1, len(cities)-3)
        crossoverStopIndex = random.randint(crossoverStartIndex+1, len(cities)-2)
     
        offspringCities = []
        offspringCitiesIds = []
        recombinationKept = []
        recombinationKeptIds=[]
        for i in range(crossoverStartIndex, crossoverStopIndex+1):
            recombinationKept.append(p[0].cities[i])
            recombinationKeptIds.append(p[0].cities[i].id)
            
        offspringCities.append(cities[0])
        j=0
        forgot = []
        for i in range(1, len(cities)):
            if i==crossoverStopIndex+1:
                for el in forgot:
                    if el.id not in offspringCitiesIds:
                        offspringCities.append(el)
                        offspringCitiesIds.append(el.id)
                        
            if (i>crossoverStopIndex or i<crossoverStartIndex) and p[1].cities[i].id not in recombinationKeptIds:
                offspringCities.append(p[1].cities[i])
                offspringCitiesIds.append(p[1].cities[i])
            elif i<=crossoverStopIndex and i>=crossoverStartIndex:
                if recombinationKept[j] not in offspringCities:
                    offspringCities.append(recombinationKept[j])
                    offspringCitiesIds.append(recombinationKept[j].id)
                    if p[1].cities[i] not in recombinationKept:
                        forgot.append(p[1].cities[i])
                j+=1
                
                
        offspringCities.append(cities[0])
        offspring = Individual(offspringCities)
        
        offsprings.append(offspring)
    return offsprings


def mutate(generation):
    mutated=[]
    
    i=0
    while len(mutated)<len(generation):
        individual = generation[i]
        i1 = random.randint(1, len(individual.cities)-2)
        i2 = random.randint(1, len(individual.cities)-2)
        
        while i2==i1:
            i2=random.randint(1, len(individual.cities)-2)
        
        newInd=individual.copy()
        tmp = newInd.cities[i1]
        newInd.cities[i1]=newInd.cities[i2]
        newInd.cities[i2]=tmp
        if(newInd not in mutated):
            mutated.append(newInd)
            i+=1

    return mutated

def log(generation):
    f2.write("Gen "+str(genId)+" with popsize = "+str(len(generation))+"\n")
    for ind in generation:
        f2.write(str(ind.fitness)+" ")
    f2.write("\n")

def plotBest(best):
    x = [o.x for o in best.cities]

    y = [o.y for o in best.cities]
    
   
    plt.plot(x, y)
    for i in range(len(x)):
        plt.annotate(best.cities[i].id, (x[i],y[i]))    
    plt.savefig("tmp.png")

#representation: list of cities in which the order is the visiting order, city 1 will have to appear at the start and at the end 
#to fill it in first I need to parse the file and initialize each individual
f=open(inputFile, mode="r", encoding="utf-8")
cities=[]
for line in f.readlines():
    sL=line.split(" ")
    n = City(int(sL[0]), float(sL[1]), float(sL[2]))
    cities.append(n)

f.close()

fm.write("Starting new run\nrun\tmt\tgbr\tps\td\toutcome\n")
for i in range(runs):
    popSize=delta
    elitism=startSize
    print("Popsize = ", elitism, "run: ", i)
    fitnessValuations=0
    generation=[]
    genId=0
    genFitnesses=[]
    toplot= "ao"
               
    sumOfFitness=0.0

    for j in range(elitism):
        individual = Individual(randomize(cities))
        generation.append(individual)
        genFitnesses.append(individual.fitness)
        individual.setFitness(fitness(individual.cities))
        sumOfFitness+=1/individual.fitness
    generation = sorted(generation, key=lambda x:x.fitness)
                
    x=[]
    y=[]
    best = generation[0]
    log(generation)
    x.append(genId)
    y.append(generation[0].fitness) #y is the history of the best solutions

    for el in generation:
        el.setProbability(1/el.fitness/sumOfFitness)

    while fitnessValuations<maxFitness and best.fitness>9000:
        childdisc=0

        sumOfFitness=0.0
        #print("Getting parents at gen:", genId)       
        parents=getParents(generation)
        #print("Getting offsprings")  
        offsprings=crossover(parents)
        backup = offsprings.copy()
        for offspring in backup:
            val = fitness(offspring.cities)
            if val not in genFitnesses:
                offspring.setFitness(val)
                genFitnesses.append(offspring.fitness)
            else:
                offsprings.remove(offspring)
                childdisc+=1
        #print("Extending generation")
        generation.extend(offsprings)
        generation = sorted(generation, key=lambda x:x.fitness)

                    
        if genId>genBetterRate and y[genId-genBetterRate]-y[genId]<mutationThreshold and genId%genBetterRate==0:
            #print("Getting mutants")
            mutated = mutate(generation)
            elitism+=popSize
            
            bm = mutated.copy()
            for mutant in bm:
                val = fitness(mutant.cities) 
                if val in genFitnesses:
                    mutated.remove(mutant)
                               
                else:
                    mutant.setFitness(val)
                genFitnesses.append(mutant.fitness)
            generation.extend(mutated)
        elif genId>genBetterRate and y[genId-genBetterRate]-y[genId]>=mutationThreshold and genId%genBetterRate==0:
            elitism = max(popSize, elitism-popSize)
           

        generation = sorted(generation, key=lambda x:x.fitness)
        best = generation[0]
                
        x.append(genId)
        y.append(generation[0].fitness)

        genId+=1
        generation=generation[:elitism]
        for g in generation:
            sumOfFitness+=1/g.fitness
        for g in generation:
            g.probability=1/g.fitness/sumOfFitness
        log(generation)
        if genId%genBetterRate==0:
            print("gen", genId, "best: ", best.fitness, "current fitness: ", fitnessValuations, "/", maxFitness, "population: ",len(generation))

                        
    
    fig=plt.figure(figsize=(24, 24), dpi=60)
    ax = fig.add_subplot(111)

    s="Population: "+str(popSize)+" best solution: "+str(round(best.fitness, 2))
    ax.plot(x,y)
    ax.set_title(s)

    plt.savefig(toplot)
    plt.close()

    plotBest(best)
    for city in best.cities:
        f2.write(str(city.id)+" -> ")
    f2.write("\n")
    print(best.fitness, "after ", genId, " generations")
    fm.write(str(i)+"\t"+str(mutationThreshold)+"\t"+str(genBetterRate)+"\t"+str(startSize)+"\t"+str(delta)+"\t"+str(round(best.fitness, 2)))
    if(best.fitness>9000):
        fm.write("\tFAIL")
        failed+=1
    fm.write("\n")
    if failed>1:
        fm.write("Stopping as this instance has failed more than twice\n")
        quit()

fm.close()
    
    