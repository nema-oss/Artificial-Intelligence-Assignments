import random


l1 = [7,3,1,8,2,4,6,5]
l2= [7,5,2,8,4,3,1,6]
for i in range(100000):
    cI = random.randint(1, len(l1)-2)
    cV = random.randint(1, len(l1)-cI)
    print(cI, cV)

    rK=[]
    oC=[]
    oC.append(l1[0])
    for i in range(cI, cI+cV):
        rK.append(l1[i])

    p2G=[]
    for i in range(1, len(l1)):
        if l2[i] not in rK:
            p2G.append(l2[i])

    for i in range(0, cI-1):
        oC.append(p2G[i])

    for i in range(cV):
        oC.append(rK[i])
        
    for i in range(cI-1, len(p2G)):
        oC.append(p2G[i])

    print(oC)