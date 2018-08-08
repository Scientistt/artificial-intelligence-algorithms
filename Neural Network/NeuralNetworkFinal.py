# Created by Fabio Vitor at 20-05-2017
# Neural Network Algorithm

from random import random
from math import e, pow

class Neuron:
    def __init__(self):
        self.goesTo = []
        self.tendency = None
        self.receives = None
        self.value = None
        self.error = None
        self.correct = None

    def addEdge(self, node, weight):
        for i in self.goesTo:
            if node in i:
                return False
        self.goesTo.append([node, weight])
        return True

    def getActivationFunction(self):
        return 1.0 / (1.0 + e**-self.receives)

    def print(self):
        print("iD =", id(self))
        print("tendency =", self.tendency, "\nReceives =", self.receives, "\nvalue =", self.value, "\nError =", self.error)
        print("Output =", self.value)
        if len(self.goesTo) != 0:
            print(" and goes to = [", end='')
            for i in self.goesTo:
                print("[", end='')
                print(id(i[0]), end='')
                print(", ",end='')
                print(i[1], end='')
                print("] ", end='')
            print("")

class NeuralNetwork:
    def __init__(self, numberOfInternalLayers, numberOfFinalNeurons):
        self.startNeurons = []
        self.internalNeurons = []
        for i in range(numberOfInternalLayers):
            self.internalNeurons.append([])
        self.finalNeurons = []
        self.numberOfInternalLayers = numberOfInternalLayers
        self.numberOfFinalNeurons = numberOfFinalNeurons
        self.age = 0
        self.keep = True

    def getRandom(self):
        return random() * 2 - 1
        
    def getNumberOfStartNeurons(self):
        return len(self.startNeurons)

    def getNumberOfInternalNeurons(self):
        return len(self.internalNeurons[0])

    def getNumberOfInternalNeuronsLLayers(self):
        return len(self.internalNeurons)

    def getNumberOfFinalNeurons(self):
        return len(self.finalNeurons)

    def print(self):
        print("\nInitial Neurons:")
        for i in self.startNeurons:
            i.print()
        print("\nInternal Neurons:")
        for i in range(len(self.internalNeurons)):
            print("Layer", i + 1)
            for j in self.internalNeurons[i]:
                j.print()
        print("\nFinal Neurons:")
        for i in self.finalNeurons:
            i.print()

    def setStartValues(self, dataSet, expectedValue, numberOfInternalNeurons):
        for i in range(self.numberOfFinalNeurons):
            self.finalNeurons.append(Neuron())
            self.finalNeurons[i].tendency = self.getRandom()
            self.finalNeurons[i].correct = expectedValue
        for i in range(self.numberOfInternalLayers):
            for j in range(numberOfInternalNeurons):
                self.internalNeurons[i].insert(0, Neuron())
                self.internalNeurons[i][-(j + 1)].tendency = self.getRandom()
                if i == 0:
                    for k in range(self.numberOfFinalNeurons):
                        self.internalNeurons[i][-(j + 1)].addEdge(self.finalNeurons[k], self.getRandom())
                else:
                    for k in range(numberOfInternalNeurons):
                        self.internalNeurons[i][-(j + 1)].addEdge(self.internalNeurons[i][-j], self.getRandom())
        for i in range(len(dataSet)):
            self.startNeurons.append(Neuron())
            self.startNeurons[i].value = dataSet[i]
            for j in self.internalNeurons[0]:
                self.startNeurons[i].addEdge(j, self.getRandom())

    def setNewValues(self, dataSet, expectedValue):
        for i in range(self.getNumberOfStartNeurons()):
            self.startNeurons[i].value = dataSet[i]
        for i in range(self.getNumberOfFinalNeurons()):
            self.finalNeurons[i].correct = expectedValue

    def testNetwork(self):
        for i in range(self.getNumberOfInternalNeuronsLLayers()):
            for j in range(self.getNumberOfInternalNeurons()):
                self.internalNeurons[i][j].receives = self.internalNeurons[i][j].tendency
                if i == 0:
                    groupToSearch = self.startNeurons
                else:
                    groupToSearch = self.internalNeurons[i - 1]
                for k in groupToSearch:
                    for l in k.goesTo:
                        if self.internalNeurons[i][j] == l[0]:
                            self.internalNeurons[i][j].receives += l[1] * k.value
                            break
                if i == self.getNumberOfInternalNeuronsLLayers() - 1:
                    for k in self.finalNeurons:
                        if j == 0:
                            k.receives = k.tendency
                        self.internalNeurons[i][j].value = self.internalNeurons[i][j].getActivationFunction()
                        k.receives += self.internalNeurons[i][j].getActivationFunction() * self.internalNeurons[i][j].goesTo[0][1];
                    k.value = k.getActivationFunction()
        res = []
        for k in self.finalNeurons:
            res.append(k.value)
        return res

    def trainFor(self, times, learningTax, acceptableErrorTax):
        for i in range(times):
            self.trainOnce(learningTax, acceptableErrorTax)
                            
    def trainOnce(self, learningTax, acceptableErrorTax):
        self.age += 1
        for i in range(self.getNumberOfInternalNeuronsLLayers()):
            for j in range(self.getNumberOfInternalNeurons()):
                self.internalNeurons[i][j].receives = self.internalNeurons[i][j].tendency
                if i == 0:
                    groupToSearch = self.startNeurons
                else:
                    groupToSearch = self.internalNeurons[i - 1]
                for k in groupToSearch:
                    for l in k.goesTo:
                        if self.internalNeurons[i][j] == l[0]:
                            self.internalNeurons[i][j].receives += l[1] * k.value
                            break
                if i == self.getNumberOfInternalNeuronsLLayers() - 1:
                    for k in self.finalNeurons:
                        if j == 0:
                            k.receives = k.tendency
                        self.internalNeurons[i][j].value = self.internalNeurons[i][j].getActivationFunction()
                        k.receives += self.internalNeurons[i][j].getActivationFunction() * self.internalNeurons[i][j].goesTo[0][1];
                        k.value = k.getActivationFunction()
        self.keep = True
        for k in self.finalNeurons:
            k.error = k.value * (1 - k.value) * (k.correct - k.value)
            if k.error < acceptableErrorTax:
               self.keep = False
        if self.keep:
            for i in range(self.getNumberOfInternalNeuronsLLayers()):
                for j in range(self.getNumberOfInternalNeurons()):
                    self.internalNeurons[-(i + 1)][j].error = self.internalNeurons[-(i + 1)][j].getActivationFunction() * (1 - self.internalNeurons[-(i + 1)][j].getActivationFunction())
                    helper = 0
                    if i == 0:
                        groupToSearch = self.finalNeurons
                    else:
                        groupToSearch = self.internalNeurons[-i]
                    for k in groupToSearch:
                        for l in self.internalNeurons[-(i + 1)][j].goesTo:
                            if k == l[0]:
                                helper  += k.error * l[1]
                    self.internalNeurons[-(i + 1)][j].error *= helper
            for i in range(self.getNumberOfInternalNeuronsLLayers()):
                for j in range(self.getNumberOfInternalNeurons()):
                    for k in self.internalNeurons[-(i + 1)][j].goesTo:
                        k[1] += learningTax * k[0].error * self.internalNeurons[-(i + 1)][j].getActivationFunction()
            for i in self.startNeurons:
                for j in i.goesTo:
                    j[1] += learningTax * j[0].error * i.value
            for i in self.finalNeurons:
                i.tendency += learningTax * i.error
            for i in self.internalNeurons:
                for j in i:
                    j.tendency += learningTax * j.error
