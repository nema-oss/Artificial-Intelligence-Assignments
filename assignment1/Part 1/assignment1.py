import datetime

maximumWeight = 420
nameFile="/home/nema/projectsAI/assignment1/Part 1/Assignment 1 knapsack.txt"
mode = 2

class Item:
    def __init__(self, id, benefit, weight):
        self.id=id
        self.benefit=benefit
        self.weight=weight

class Node:
    def __init__(self, benefit, depth):
        self.items=[]
        self.benefit=benefit
        self.depth=depth
    def addItems(self,items):
        self.items.append(items)

def findItemById(id, items):
    for item in items:
        if item.id==id:
            return item
    return 0

def computeNodeWeight(node):
    w=0
    for item in node.items:
        w+=item.weight
    return w

def expand(node, items):
    result=[]

    lastItem=node.items[-1]
    i=1
    nextItem = findItemById(lastItem.id + 1, items)
    while nextItem != 0:
        newNode=Node(0, node.depth+1)
        for item in node.items:
            newNode.addItems(item)
        newNode.addItems(nextItem)
    
        newNode.benefit=node.benefit + nextItem.benefit
        if computeNodeWeight(newNode)<maximumWeight:
            result.append(newNode)
        i+=1
        nextItem = findItemById(lastItem.id + i, items)
              
    return result 


def bfs(items):
    queue=[]
    for i in items:
        initialNode = Node(i.benefit, 1)
        initialNode.addItems(i)
        queue.append(initialNode)

    exploredNodes=[]
    maxBenefit=queue[0].benefit
    solution=queue[0]
    #continue to expand nodes until there is no other node in queue
    while len(queue)>0:
        node=queue[0]
        exploredNodes.append(node)
        if node.benefit>maxBenefit:
            maxBenefit=node.benefit
            solution=node
        result = expand(node, items)
        for newNode in result:
            queue.append(newNode)

        queue.remove(node)
    return solution


def dfs(items):
    stack=[]
    for i in items:
        initialNode = Node(i.benefit, 1)
        initialNode.addItems(i)
        stack.append(initialNode)
    exploredNodes=[]
    maxBenefit=stack[0].benefit
    solution=stack[0]

    while len(stack)>0:
        node=stack[0]
        exploredNodes.append(node)
        if node.benefit>maxBenefit:
            maxBenefit=node.benefit
            solution=node
        result = expand(node, items)
        newStack=[]
        for newNode in result:
            newStack.append(newNode)

        stack.remove(node)
        for el in stack:
            newStack.append(el)
        stack=newStack    
    return solution

#every node is a list of possible combinations of the items s.t their weight is <= total allowed weight
#initial state is the empty knapsack

items = []

#parse items from file
f = open(nameFile, mode="r", encoding="utf-8")
for line in f.readlines():
    id = int(line.split(" ")[0])
    ben = int(line.split(" ")[1])
    w = int(line.split(" ")[2])
    item = Item(id, ben, w)
    items.append(item)
f.close()
#start timer
start = datetime.datetime.now().microsecond

if mode==1:
    sol = bfs(items)
else:
    sol = dfs(items)

end = datetime.datetime.now().microsecond
print("max benefit=", sol.benefit, ", weight=", computeNodeWeight(sol),"d = ", sol.depth, " with items: ")
for item in sol.items:
    print(item.id)
print((end - start)*pow(10,-6))
