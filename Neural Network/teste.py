
from random import random
from math import e
from math import pow

class Neuronium:

    def __init__(self):
        self.receive = None
        self.tendency = None
        self.value = None        
        self.goesTo = []
    
    def setTendency(self, newTendency):
        self.tendency = newTendency

    def getTendency(self):
        return self.tendency

    def setValue(self, newValue):
        self.value = newValue

    def getValue(self):
        return self.value

    def getEdges(self):
        return self.goesTo

    def getEdge(self, pos):
        if 0 <= pos < len(self.goesTo) or  0 - len(self.goesTo) <= pos <= -1:
            return self.goesTo[pos]
        return [];

    def addEdge(self, node, weight):
        for i in range(len(self.goesTo)):
            if node in self.goesTo[i]:
                return False
        self.goesTo.append([node, weight])
        return True



class NeuralNetwork():
    def __init__(self, internalLayers, nOfinternalN, nOffinalN):
        self.startN  = []
        self.internalN = []
        for i in range(internalLayers):
            self.internalN.append([])
        self.finalN  = []
        self.numberOfInternalLayers = internalLayers
        self.numberOfstartN = None
        self.numberOfinternalN = nOfinternalN
        self.numberOfFinalN = nOffinalN
        self.age = 0

    def setStartN(self, data):
        # Setting the finals
        for i in range(self.numberOfFinalN):
            self.finalN.append(Neuronium())
            self.finalN[i].setTendency(random())
            self.finalN[i].setValue(data[-1])

        # Setting the internals
        for i in range(self.numberOfInternalLayers):
            for j in range(self.numberOfinternalN):
                self.internalN[0 - (i + 1)].append(Neuronium())
                self.internalN[0 - (i + 1)][j].setTendency(random())
                if(i == 0):
                    for k in range(self.numberOfFinalN):
                        self.internalN[0 - (i + 1)][j].addEdge(self.finalN[k], random())
                else:
                    for k in range(self.numberOfinternalN):
                        self.internalN[0 - (i + 1)][j].addEdge(self.internalN[0 - i][k],random())

        # Setting the starting
        self.numberOfstartN = len(data) - 1
        for i in range(self.numberOfstartN):
            self.startN.append(Neuronium())
            self.startN[i].setValue(data[i])
            for j in range(self.numberOfinternalN):
                self.startN[i].addEdge(self.internalN[0][j], random())

    def evaluate(self, x):
        return 1 / (1 + pow(e, 0 - x))
        

    def trainOnce(self):
        self.age += 1

        # Forward
        for i in range(self.numberOfInternalLayers):
            for j in range(self.numberOfinternalN):
                if  i == 0:
                    helper = 0
                    for k in range(self.numberOfstartN):
                        for l in self.startN[k].goesTo:
                            if self.internalN[i][j] == l[0]:
                                helper += l[1] * self.startN[k].getValue()
                                break
                    self.internalN[i][j].receives = helper + self.internalN[i][j].tendency
                else:
                    helper = 0
                    for k in range(self.numberOfinternalN):
                        for l in self.internalN[i - 1][k].goesTo:
                            if self.internalN[i][j] == l[0]:
                                helper += l[1] * self.evaluate(self.internalN[i - 1][k].receives)
                                break
                                
        for i in range(self.numberOfFinalN):
            helper = 0
            for j in range(self.numberOfinternalN):
                for k in self.internalN[-1][j].goesTo:
                    if self.finalN[i] == k[0]:
                        helper += k[1] * self.evaluate(self.internalN[-1][j].receeives)
                        break
            self.finalN[i].value = helper + self.finalN[i].tendency

        # Backward
        for i in range(self.)
        

    
        
    def print(self):
        for i in range(self.numberOfstartN):
            print(id(self.startN[i]), end=' [')
            for j in range(len(self.startN[i].goesTo)):
                print(id(self.startN[i].goesTo[j][0]),end=' ')
            print("]")
        print("")

        for i in range(self.numberOfInternalLayers):
            for j in range(self.numberOfinternalN):
                print(id(self.internalN[i][j]), end=' [')
                for k in range(len(self.internalN[i][j].goesTo)):
                    print(id(self.internalN[i][j].goesTo[k][0]),end=' ')
                print("]")
            print("")
            
        for i in range(self.numberOfFinalN):
            print(id(self.finalN[i]), end=' ')
            
        

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




a = NeuralNetwork(2, 5, 4)

a.setStartN([preEnsolarado,  temQuente,  umiAlta,    venFraco, resNegativo])






