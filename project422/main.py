# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import numpy as np
import itertools

"""Author: Yuhang Zhang & Rintaro Nomura"""

# It works on Google Colab. 


def main():
    file_path = input("Please input file path: ")
    reliabilityGoal = float(input("Please enter reliability goal: "))
    costGoal = int(input("Please enter cost constraint: "))

    # Initial Operations
    inputValues = readInputFile(file_path)
    numOfNodes = inputValues[0]
    reliability = inputValues[1]
    cost = inputValues[2]
    edgeNum = inputValues[3]

    # Create edge array
    edge = [None] * edgeNum
    z = 0
    for x in range(numOfNodes):
        for y in range(x + 1, numOfNodes, 1):
            edge[z] = Edge(x+1, y+1, reliability[z], cost[z])
            z = z + 1

    edge.sort(key=decreasingMode, reverse=True)


    # Meet a given reliability goal.
    print("Computing: Solutions satisfy the reliability goal")
    print("Note: Please be patient... it takes a while...")
    fhA = open("Section1.txt", "a")
    fhA.write(60 * "-" + "\n")
    fhA.write("Solutions satisfy the reliability goal: ")
    fhA.write(str(reliabilityGoal) + "\n")
    sln = meetReliabilityGoal(edge, numOfNodes, reliabilityGoal, costGoal, False)
    output(fhA, sln, numOfNodes)
    fhA.close()
    print("Completed! See ./Section1.txt for the result. \n\n")

    # Maximize reliability subject to a given cost constraint
    print("Computing: Maximize reliability subject to a given cost constraint\n")
    temp = meetReliabilityGoal(edge, numOfNodes, reliabilityGoal, costGoal, True)
    fhB = open("Section2.txt", "a")
    fhB.write(60 * "-" + "\n")
    fhB.write("Solution for maximum reliability given cost constraint: ")
    fhB.write(str(costGoal) + "\n")
    findMaxReliability(fhB, temp, numOfNodes)
    fhB.close()
    print("Completed! See ./Section2.txt for the result. \n\n")
    print("Bye! ")

class Edge:
	def __init__(self,nodeA,nodeB,reliability,cost):
		self.nodeA = nodeA
		self.nodeB = nodeB
		self.reliability = reliability
		self.cost = cost


def readInputFile(file_path):
    lines = [line for line in open(file_path) if not line.startswith('#') and
             len(line.strip())]
    numOfNodes = int(lines[0].split("\n")[0])
    reliability = list(map(float, lines[1].split("\n")[0].split(" ")))
    cost = list(map(float, lines[2].split("\n")[0].split(" ")))
    edgeNum = len(reliability)

    return [numOfNodes, reliability, cost, edgeNum]


def decreasingMode(elem):
    return elem.reliability


def getCost(list):
    i = 0
    cost = 0
    for i in range(len(list)):
        cost = cost + list[i].cost
    return cost


def getReliability(edge, numOfNodes):
    # Performs a simple algorithm to trace down the reliability from a graph
    combination = list(itertools.product([0, 1], repeat = len(edge)))

    i = 0
    while True:
        if i == (len(combination) - 1):
            break 
        elif sum(combination[i]) < numOfNodes-1:
            del combination[i]
        else:
            i += 1
    
    outputReliability = 0

    # Also check the subgraph
    for i in range(len(combination)):
        subGraph = []
        for j in range(len(edge)):
            if combination[i][j] == 1: 
                subGraph.append(edge[j])
                 
        if not isAllConnected(subGraph, numOfNodes):
            continue


        subGraphReliability = 1
        for j in range(len(combination[0])):
            if combination[i][j] == 1: 
                subGraphReliability *= edge[j].reliability
            else:
                 subGraphReliability *= (1 - edge[j].reliability)

        outputReliability += subGraphReliability

    return outputReliability


def isAllConnected(edge, numOfNodes):
    # Attempts to make have a walk in the graph
    connectedNode = []
    connectedNode.append(1)
    i = 0

    # Essentially just a simple search algorithm
    while i < numOfNodes:
        if len(connectedNode) <= i:
            return False
        if len(connectedNode) == numOfNodes:
            return True
        for x in range(len(edge)):
            
            if edge[x].nodeA == connectedNode[i] and edge[x].nodeB not in connectedNode: 
                connectedNode.append(edge[x].nodeB)

            if edge[x].nodeB == connectedNode[i] and edge[x].nodeA not in connectedNode:
                connectedNode.append(edge[x].nodeA)
        i += 1


def buildSpanningTree(edge, numOfNodes):
    connectedNode = []
    pickedEdge = []
    i = 0
    while len(connectedNode) < numOfNodes:
        if i == 0:
            pickedEdge.append(edge[i])
            connectedNode.append(edge[i].nodeA)
            connectedNode.append(edge[i].nodeB)

        elif edge[i].nodeA in connectedNode and edge[i].nodeB in connectedNode:
            i += 1
            continue

        else:
            pickedEdge.append(edge[i])
            if edge[i].nodeA not in connectedNode:
                connectedNode.append(edge[i].nodeA)
            if edge[i].nodeB not in connectedNode:
                connectedNode.append(edge[i].nodeB)
        i += 1
    return pickedEdge


def meetReliabilityGoal(edge, numOfNodes, reliabilityGoal, costGoal, costContrained):
    
    combination = list(itertools.product([0, 1], repeat = len(edge)))

    graphSet = []
    i = 0
    while True:
        if i == (len(combination) - 1):
            break 
        elif sum(combination[i]) < numOfNodes-1:
            del combination[i]
        else:
            i += 1

    for i in range(len(combination)):
        
        graph = []
        for j in range(len(edge)):
            if combination[i][j] == 1: 
                graph.append(edge[j])
                 
        if not isAllConnected(graph, numOfNodes):
            continue

        if costContrained and costGoal > 0:
            if getCost(graph) > costGoal:
                continue

        if getReliability(graph, numOfNodes) >= reliabilityGoal:
            graphSet.append(graph)
    return graphSet


def findMaxReliability(outputFile, graphSet, numOfNodes):
    outputGraph = []
    MaxReli = 0
    for x in range(len(graphSet)):      # Traverse the graph set and take the maximum
        if getReliability(graphSet[x], numOfNodes) > MaxReli:
            outputGraph = graphSet[x]
            MaxReli = getReliability(graphSet[x], numOfNodes)

    outputFile.write("\n")

    for x in range(len(outputGraph)):
        outputFile.write("Edge # " + str(x+1) + " : " + str(outputGraph[x].nodeA) + " - " + str(outputGraph[x].nodeB) + " Reliability: " + str(outputGraph[x].reliability) + " Cost: " + str(outputGraph[x].cost) + "\n")
    outputFile.write("Total cost: " + str(getCost(outputGraph)) + "\n")
    outputFile.write("Max Reliability " + str(getReliability(outputGraph,numOfNodes)) + "\n")


def output(file,sol, numOfNodes):
    for x in range(len(sol)):
        #file.write("Solution # " + str(x+1) + "\n")
        file.write("Total reliability:" + str(getReliability(sol[x], numOfNodes)) + "\n")
        for i in range(len(sol[x])):
            file.write("Edge" + str(i+1) + ": " + str(sol[x][i].nodeA) + " <-> " + str(sol[x][i].nodeB) + " Reliability: " + str(sol[x][i].reliability) + " Cost: " + str(sol[x][i].cost) + "\n")
        file.write("\n")


if __name__ == "__main__":
    main()



