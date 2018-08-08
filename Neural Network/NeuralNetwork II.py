from random import random
from math import e, pow, floor

#
#
#

def fix(x):
    return floor(x * 1000) / 1000
    
class Neuronium:
    def __init__(self):
        self.goesTo = []
        self.tendency = None
        self.receives = None
        self.value = None
        self.error = None

    def addEdge(self, node, weight):
        for i in self.goesTo:
            if node in i:
                return False
        self.goesTo.append([node, weight])
        return True

    def getActivationFunction(self):
        return fix(1.0 / (1.0 + e**-self.receives))

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
#
#
#
class NeuralNetwork:
    def __init__(self, numberOfInternalLayers, numberOfFinalNeuronium):
        self.startNeuronium = []
        self.internalNeuronium = []
        for i in range(numberOfInternalLayers):
            self.internalNeuronium.append([])
        self.finalNeuronium = []
        self.numberOfInternalLayers = numberOfInternalLayers
        self.numberOfFinalNeuronium = numberOfFinalNeuronium
        self.age = 0

    def getRandom(self):
        return random() * 2 - 1

    def getNumberOfStartNeuronium(self):
        return len(self.startNeuronium)

    def getNumberOfInternalNeuronium(self):
        return len(self.internalNeuronium[0])

    def getNumberOfInternalNeuroniumLLayers(self):
        return len(self.internalNeuronium)

    def getNumberOfFinalNeuronium(self):
        return len(self.finalNeuronium)

    def print(self):
        print("\nInitial Neuronium:")
        for i in self.startNeuronium:
            i.print()
        print("\nInternal Neuronium:")
        for i in range(len(self.internalNeuronium)):
            print("Layer", i + 1)
            for j in self.internalNeuronium[i]:
                j.print()
        print("\nFinal Neuronium:")
        for i in self.finalNeuronium:
            i.print()

    def setStartValues(self, dataSet, expectedValue, numberOfInternalNeuronium):
        for i in range(self.numberOfFinalNeuronium):
            self.finalNeuronium.append(Neuronium())
            self.finalNeuronium[i].tendency = self.getRandom()
            self.finalNeuronium[i].value = expectedValue
        for i in range(self.numberOfInternalLayers):
            for j in range(numberOfInternalNeuronium):
                self.internalNeuronium[i].insert(0, Neuronium())
                self.internalNeuronium[i][-(j + 1)].tendency = self.getRandom()
                if i == 0:
                    for k in range(self.numberOfFinalNeuronium):
                        self.internalNeuronium[i][-(j + 1)].addEdge(self.finalNeuronium[k], self.getRandom())
                else:
                    for k in range(numberOfInternalNeuronium):
                        self.internalNeuronium[i][-(j + 1)].addEdge(self.internalNeuronium[i][-j], self.getRandom())
        for i in range(len(dataSet)):
            self.startNeuronium.append(Neuronium())
            self.startNeuronium[i].value = dataSet[i]
            for j in self.internalNeuronium[0]:
                self.startNeuronium[i].addEdge(j, self.getRandom())
                            
    def trainOnce(self, learningTax, acceptableErrorTax):
        self.age += 1        
        # Forward
        for i in range(self.getNumberOfInternalNeuroniumLLayers()):
            for j in range(self.getNumberOfInternalNeuronium()):
                self.internalNeuronium[i][j].receives = self.internalNeuronium[i][j].tendency
                if i == 0:
                    groupToSearch = self.startNeuronium
                else:
                    groupToSearch = self.internalNeuronium[i - 1]
                for k in groupToSearch:
                    for l in k.goesTo:
                        if self.internalNeuronium[i][j] == l[0]:
                            self.internalNeuronium[i][j].receives += l[1] * k.value
                            break
                if i == self.getNumberOfInternalNeuroniumLLayers() - 1:
                    for k in self.finalNeuronium:
                        if j == 0:
                            k.receives = k.tendency

                            
                        self.internalNeuronium[i][j].value = self.internalNeuronium[i][j].getActivationFunction()

                        
                        k.receives += self.internalNeuronium[i][j].getActivationFunction() * self.internalNeuronium[i][j].goesTo[0][1];

        keep = True
        for k in self.finalNeuronium:
            k.error = k.receives * (1 - k.receives) * (k.value - k.receives)
#            if k.error < acceptableErrorTax:
#               keep = False

        # Backward
        if keep:
            # Errors
            for i in range(self.getNumberOfInternalNeuroniumLLayers()):
                for j in range(self.getNumberOfInternalNeuronium()):
                    self.internalNeuronium[-(i + 1)][j].error = self.internalNeuronium[-(i + 1)][j].getActivationFunction() * (1 - self.internalNeuronium[-(i + 1)][j].getActivationFunction())
                    helper = 0
                    if i == 0:
                        groupToSearch = self.finalNeuronium
                    else:
                        groupToSearch = self.internalNeuronium[-i]
                    for k in groupToSearch:
                        for l in self.internalNeuronium[-(i + 1)][j].goesTo:
                            if k == l[0]:
                                helper  += k.error * l[1]
                    self.internalNeuronium[-(i + 1)][j].error *= helper
                    self.internalNeuronium[-(i + 1)][j].error = fix(self.internalNeuronium[-(i + 1)][j].error)
                    print("Erro do", id(self.internalNeuronium[-(i + 1)][j]), " é ", self.internalNeuronium[-(i + 1)][j].error)
            # Weights
            for i in range(self.getNumberOfInternalNeuroniumLLayers()):
                for j in range(self.getNumberOfInternalNeuronium()):
                    for k in self.internalNeuronium[-(i + 1)][j].goesTo:
                        k[1] += learningTax * k[0].error * self.internalNeuronium[-(i + 1)][j].getActivationFunction()
                        k[1] = fix(k[1])
            for i in self.startNeuronium:
                for j in i.goesTo:
                    j[1] += learningTax * j[0].error * i.value
                    j[1] = fix(j[1])
            # Tendencies
            for i in self.finalNeuronium:
                i.tendency += learningTax * i.error
                i.tendency = fix(i.tendency)
            for i in self.internalNeuronium:
                for j in i:
                    j.tendency += learningTax * j.error
                    j.tendency = fix(j.tendency)
        self.print()
            
        


###
###
###

#Previsão
preEnsolarado, preNublado, preChuvoso = 0, 1, 2

#Temperatura
temQuente, temMedia, temFria = 0, 1, 2

#Umidade
umiAlta, umiNormal = 0, 1

#Vento
venForte, venFraco = 0, 1

#Resultados
resNegativo, resPositivo = 0, 1

# 14 days
dataSet = [[preEnsolarado,  temQuente,  umiAlta,    venFraco, resNegativo],
           [preEnsolarado,  temQuente,  umiAlta,    venForte, resNegativo],
           [preNublado,     temQuente,  umiAlta,    venFraco, resPositivo],
           [preChuvoso,     temMedia,   umiAlta,    venFraco, resPositivo],
           [preChuvoso,     temFria,    umiNormal,  venFraco, resPositivo],
           [preChuvoso,     temFria,    umiNormal,  venForte, resNegativo],
           [preNublado,     temFria,    umiNormal,  venForte, resPositivo],
           [preEnsolarado,  temMedia,   umiAlta,    venFraco, resNegativo],
           [preEnsolarado,  temFria,    umiNormal,  venFraco, resPositivo],
           [preChuvoso,     temMedia,   umiNormal,  venFraco, resPositivo],
           [preEnsolarado,  temMedia,   umiNormal,  venForte, resPositivo],
           [preNublado,     temMedia,   umiAlta,    venForte, resPositivo],
           [preNublado,     temQuente,  umiNormal,  venFraco, resPositivo],
           [preChuvoso,     temMedia,   umiAlta,    venForte, resNegativo]]
        
        

a = NeuralNetwork(1, 1)
a.setStartValues([1,  0,  1], 1, 2)
    

a.startNeuronium[0].goesTo[0][1] = 0.2
a.startNeuronium[0].goesTo[1][1] = -0.3
a.startNeuronium[1].goesTo[0][1] = 0.4
a.startNeuronium[1].goesTo[1][1] = 0.1
a.startNeuronium[2].goesTo[0][1] = -0.5
a.startNeuronium[2].goesTo[1][1] = 0.2

a.internalNeuronium[0][0].goesTo[0][1] = -0.3
a.internalNeuronium[0][1].goesTo[0][1] = -0.2

a.internalNeuronium[0][0].tendency = -0.4
a.internalNeuronium[0][1].tendency = 0.2

a.finalNeuronium[0].tendency = 0.1


a.trainOnce(0.9, 1)



