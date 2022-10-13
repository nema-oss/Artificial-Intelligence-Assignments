from parser import parse
import time

from debugger import example, seeDeltas, seeNetwork, seeOutputs, showImage, showImages
from network import Network, compute, createNetwork, getWeights, out
from onehot import compare, oneHot
import numpy

from training import train
#æssumption: all biases set to 1, thus taking into account only their weights
flag = input("Do the training? 1 for yes, 0 for no\n")

images = parse()
if int(flag)==1:
    readFrom = int(input("Use pre-trained weights? 1 for yes, 0 for no\nATTENTION: IT WILL DELETE OLD WEIGHTS IF PRESENT\n"))
    network=train(images, readFrom)
else:
    network=createNetwork(getWeights("weights.txt"))

testing = images[33600:]#20% 

ii=1
start = time.time()
acc = 0
actualDic = {}
correctDic = {} #represents the labels and how many times they are encountered: in the form of label : number
for image in testing:
    y = compute(image.pixels, network.input, network.layers[0])
    for i in range(len(network.layers)-1):
            layer = network.layers[i]
            y = compute(y, layer, network.layers[i+1])  
    y = out(y,network.layers[-1], network.output)
    gotIt = 0
    if compare(y, image.label, ii, len(images)-33600, 0):
        acc+=1
        gotIt = 1
    if image.label in correctDic:
        correctDic[image.label]+=1
    else:
        correctDic[image.label]=1
    
    if image.label in actualDic:
        if gotIt==1:
            actualDic[image.label]+=1
    else:
        if gotIt==1:
            actualDic[image.label]=1
        else:
            actualDic[image.label]=0 
    ii+=1
end = time.time()

print("total accuracy: ", acc/(len(images)- 33600)*100, "%", "total testing time: ", end-start)

for i in range(10):
    print("Accuracy for class ", i, "=", actualDic[i]/correctDic[i])