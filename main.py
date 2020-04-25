# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import edge_generator
import numpy as np
import itertools

# try:
#  	file_path = raw_input("Please set input file path: ")
#  	reliability_goal = input("Please enter reliability goal: ")
#  	cost_constraint = input("Please enter cost constraint: ")
# except Exception, e:
#     print e
#     exit()

#city_list, edge_list = edge_generator.generate(file_path)

#print city_list
#print(edge_list[10].reliability)

#### Basic idea
# parse the input txt and list edges in descending order (by R)
# select an edge if it does not form a cycle with the existing subgraph
# (find minimum spanning tree)
# 

def decreasingReli(elem):
    return elem.reliability


# input a list of cities
def getCost(list):
    i = 0
    cost = 0
    for i in range(len(list)):
        cost = cost + list[i].cost
    return cost


def getReli(edge, number_of_cities):
    # to connect N nodes, we need at least N-1 edges
    # find all combination with N-1 edges (all kind of possible minimal spanning tree)
    combination = list(itertools.product([0, 1], repeat = len(edge)))

    i = 0
    while True:
        if i == (len(combination) - 1):
            break 
        elif sum(combination[i]) < number_of_cities-1:
            del combination[i]
        else:
            i += 1
    
    outputReliability = 0
    for i in range(len(combination)):
        subGraph = []
        for j in range(len(edge)):
            if combination[i][j] == 1: 
                subGraph.append(edge[j])
                 
        if not isAllConnected(subGraph, number_of_cities):
            continue


        # put all connected node in this combination into connectedNode array
        subGraphReliability = 1
        for j in range(len(combination[0])):
            # if that edge is on 
            if combination[i][j] == 1: 
                subGraphReliability *= edge[j].reliability
            # if the edge is off
            else:
                 subGraphReliability *= (1 - edge[j].reliability)

        outputReliability += subGraphReliability

    return outputReliability

def isAllConnected(edge, number_of_cities):
	# check if all is connected
    connectedNode = []
    # starting from 1
    connectedNode.append(1)
    i = 0
    while i < number_of_cities:
        if len(connectedNode) <= i:
            return False
        if len(connectedNode) == number_of_cities:
            return True
        for x in range(len(edge)):
            
            if edge[x].vertice_1 == connectedNode[i] and edge[x].vertice_2 not in connectedNode: 
                connectedNode.append(edge[x].vertice_2)

            if edge[x].vertice_2 == connectedNode[i] and edge[x].vertice_1 not in connectedNode:
                connectedNode.append(edge[x].vertice_1)
        i += 1

def buildSpanningTree(edge, number_of_cities):
    connectedNode = []
    pickedEdge = []
    i = 0
    while len(connectedNode) < number_of_cities:
        if i == 0:
            pickedEdge.append(edge[i])
            connectedNode.append(edge[i].vertice_1)
            connectedNode.append(edge[i].vertice_2)

        elif edge[i].vertice_1 in connectedNode and edge[i].vertice_2 in connectedNode:
            i += 1
            continue

        else:
            pickedEdge.append(edge[i])
            if edge[i].vertice_1 not in connectedNode:
                connectedNode.append(edge[i].vertice_1)
            if edge[i].vertice_2 not in connectedNode:
                connectedNode.append(edge[i].vertice_2)
        i += 1
    return pickedEdge


def meetReliabilityGoal(edge, numOfNodes, reliability_goal, cost_constraint, costContrained):
    
    # to connect N nodes, we need at least N-1 edges
    # find all combination with N-1 edges (all kind of possible minimal spanning tree)
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
   
        # declare an empty array to store connected nodes
        connectedNode = []
        offReliability = 1
        
        graph = []
        for j in range(len(edge)):
            if combination[i][j] == 1: 
                graph.append(edge[j])
                 
        if not isAllConnected(graph, numOfNodes):
            continue

        if costContrained and cost_constraint > 0:
            if getCost(graph) > cost_constraint:
                continue

        if getReli(graph, numOfNodes) >= reliability_goal:
            graphSet.append(graph)
            # if len(graphSet) == 210:
            #       return graphSet
    return graphSet

def findMaxReliability(outputFile, graphSet, number_of_cities):
    outputGraph = []
    MaxReli = 0
    for x in range(len(graphSet)):
        if getReli(graphSet[x], number_of_cities) > MaxReli:
            outputGraph = graphSet[x]
            MaxReli = getReli(graphSet[x], number_of_cities)

    outputFile.write("\n")

    for x in range(len(outputGraph)):
        outputFile.write("Edge # " + str(x+1) + " : " + str(outputGraph[x].vertice_1) + " - " + str(outputGraph[x].vertice_2) + " Reliability: " + str(outputGraph[x].reliability) + " Cost: " + str(outputGraph[x].cost) + "\n")
    outputFile.write("Total cost: " + str(getCost(outputGraph)) + "\n")
    outputFile.write("Max Reliability " + str(getReli(outputGraph,number_of_cities)) + "\n")


def printSolutions(file,sol, number_of_cities):
    for x in range(len(sol)):
        file.write("Solution # " + str(x+1) + "\n")
        file.write("Total reliability:" + str(getReli(sol[x], number_of_cities)) + "\n")
        for i in range(len(sol[x])):
            file.write("Edge # " + str(i+1) + ": " + str(sol[x][i].vertice_1) + " - " + str(sol[x][i].vertice_2) + " Reliability: " + str(sol[x][i].reliability) + " Cost: " + str(sol[x][i].cost) + "\n")
        file.write("\n")

def main():
	# try:
	# 	file_path = raw_input("Please set input file path: ")
	# 	reliability_goal = input("Please enter reliability goal: ")
	# 	cost_constraint = input("Please enter cost constraint: ")
	# except Exception, e:
	# 	print e
	# 	exit()
	
	file_path = input("Please set input file path: ")
	reliability_goal = input("Please enter reliability goal: ")
	cost_constraint = input("Please enter cost constraint: ")

    #reliabilityGoal = float(input("Please enter reliability goal (from 0 to 1): "))
    #costGoal = int(input("Please enter cost constraint (from 1 to 100): "))
	#runPartA = input("Would you like to run part A? (y/n)")
	#runPartB = input("Would you like to run part B? (y/n)")
	#runPartC = input("Would you like to run part C? (y/n)")
	
	# answer_list = []
	# for answer in [runPartA, runPartC]:
	# 	if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "YES":
	# 		answer = True
    #     else:
	# 		answer = False
    #     answer_list.append(answer)
	
	print(50 * "*")
    #print("Reliability goal set to: " + str(reliability_goal))
    #print("Cost constraint set to: " + str(cost_constraint))
	
	#inputValues = readInputFile(answer_list)
	#number_of_cities = inputValues[0]
	#reliability = inputValues[1]
	#cost = inputValues[2]
	#edgeNum = inputValues[3]
	#edge = [None] * edgeNum
	#z = 0

	# for x in range(number_of_cities):
	# 	for y in range(x + 1, number_of_cities, 1):
	# 		edge[z] = Edge(x+1, y+1, reliability[z], cost[z])
	# 		z = z + 1

	number_of_cities, costs, reliabilities = edge_generator.read_data(file_path)

	number_of_cities = int(number_of_cities)

	city_list, edge_list = edge_generator.generate(file_path)

    #edge.sort(key=decreasingReli, reverse=True)
	edge_list.sort(key=decreasingReli, reverse=True)

	#if answer_list[0]:
	
	outputFileA = open("resultPartA.txt", "a")
	outputFileA.write(50 * "*" + "\n")
	outputFileA.write("PART a) Solutions meeting reliability goal: " + str(reliability_goal) + "\n")
	solA = meetReliabilityGoal(edge_list, number_of_cities, reliability_goal, cost_constraint, False)
	printSolutions(outputFileA, solA, number_of_cities)
	outputFileA.write(50 * "*" + "\n")
	outputFileA.close()

    # Execute Part B
    # solB = None
    # if answer_list[1]:
    #     outputFileB = open("resultPartB.txt", "a")
    #     outputFileB.write(50 * "*" + "\n")
    #     outputFileB.write(
    #         "PART b) Solutions meeting reliability goal: " + str(reliabilityGoal) + " given cost constraint: " + str(
    #             costGoal) + "\n")
    #     solB = meetReliabilityGoal(edge, number_of_cities, reliabilityGoal, costGoal, True)
    #     printSolutions(outputFileB, solB, number_of_cities)
    #     outputFileB.write(50 * "*" + "\n")
    #     outputFileB.close()

    # Execute Part C

	#if answer_list[2]:
		#if solB is None: comment this line later
    
	solB = meetReliabilityGoal(edge_list, number_of_cities, reliability_goal, cost_constraint, True)
	outputFileC = open("resultPartC.txt", "a")
	outputFileC.write(50 * "*" + "\n")
	outputFileC.write("PART c) Solution for maximum reliability given cost constraint: " + str(cost_constraint) + "\n")
	findMaxReliability(outputFileC, solB, number_of_cities)
	outputFileC.write(50 * "*" + "\n")
	outputFileC.close()


if __name__ == "__main__":
    main()			

