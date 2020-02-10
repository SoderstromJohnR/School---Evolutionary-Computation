
import random, pprint 

#Fitness function for the project
#Returns sum of squares of all x values
def _fitness(listVal):
    sumVals = 0
    for x in listVal:
        sumVals += x * x
    return sumVals

#Obtain a list of fitness values for a generation
def _getFitnessValues(listVal):
    fitList = []
    for i in listVal:
        fitList.append(_fitness(i))
    return fitList

#Manipulate fitness values for processing minimum fitness
#Modifies given list, no return needed
def _minModFitness(fitList):
    #Store minimum and maximum fitness values to reverse them
    #without resulting in heavily exaggerated values
    minFit = 0
    maxFit = 0
    for index, i in enumerate(fitList):
        if index is 0:
            minFit = i
            maxFit = i
        else:
            if minFit > i:
                minFit = i
            if maxFit < i:
                maxFit = i
    #Sum of the min and max fitnesses will flip them and
    #keep other values in between
    modFit = minFit + maxFit
    for index, i in enumerate(fitList):
        fitList[index] = modFit - i

#Convert fitness values to percents for random selection
#Modifies given list, no return needed
def _percentFitness(fitList):
    #Calculate sum to convert all fitness values to percents
    sumFit = 0
    for i in fitList:
        sumFit += i

    #Store previous value to generate stacking percentages
    #A random number between 0 and 1 may be used to select a
    #single index
    prevVal = 0
    for index, i in enumerate(fitList):
        fitList[index] /= sumFit
        fitList[index] += prevVal
        prevVal = fitList[index]
    #Set final value to 2.0 instead of 1.0 to ensure no
    #edge case percent errors
    fitList[-1] = 2.0

#Obtain fitness data about a generation
#Returns a dictionary including indices of the best and worst chromosomes
def _getFitnessData(listVal):
    fitList = _getFitnessValues(listVal)
    fitData = {}
    for index, i in enumerate(fitList):
        #Initialize fitData to first fitness value
        if index is 0:
            fitData = {'High Fit' : i, 'High Fit Index' : index,
                       'Low Fit' : i, 'Low Fit Index' : index,
                       'Average Fit' : i}
        else:
            #Increment value for average fitness of generation
            fitData['Average Fit'] += i
            #Update best fitness and index values
            if fitData['High Fit'] < i:
                fitData['High Fit'] = i
                fitData['High Fit Index'] = index
            #Update worst fitness and index values
            if fitData['Low Fit'] > i:
                fitData['Low Fit'] = i
                fitData['Low Fit Index'] = index
    #Finalize average fitness and return list
    fitData['Average Fit'] /= len(listVal)
    return fitData

#Creates the initial generation for the GA
def _initialGen(popSize, chromoSize, minVal, maxVal):
    initGen = []
    #Creates a chromosome for the entire population size
    for n in range(popSize):
        xVals = []
        #Selects random values inside given range for each element
        #in the chromosome
        for i in range(chromoSize):
            xVals.append(random.uniform(minVal, maxVal))
        initGen.append(xVals)
    return initGen

#Selection process, proportional, for a new generation
def _selectNewGen(prevGen, isMaxFit = True):
    indices = range(len(prevGen))
    #Get a list of all fitness values and convert to percents
    #Reverse fitness values if attempting to minimize fitness
    fitnessVals = _getFitnessValues(prevGen)
    if not isMaxFit:
        _minModFitness(fitnessVals)
    _percentFitness(fitnessVals)
            
    #Create a new list using percentages in selection
    tempList = []
    for i in indices:
        copyIndex = 0
        randomChoice = random.random()
        #randomChoice will never be > 1, so this loop will always end before
        #out of range errors
        #Ends when we reach the percent range our randomChoice is in
        while randomChoice > fitnessVals[copyIndex]:
            copyIndex += 1
        tempList.append(prevGen[copyIndex])

    #Set our new selection list to the input
    for i in indices:
        prevGen[i] = tempList[i]

#Crossover process for a new generation
def _crossNewGen(prevGenSelect, pointCross, prob):
    #Warn if crossover will not change either point meaningfully
    #Expecting that all chromosomes will have the same length
    if pointCross is 0 or pointCross >= len(prevGenSelect[0]):
        print("Warning: crossover will not change points.")
        print("    Reconsider your point crossover value.")
        #If the line is too far right, lower it to avoid errors
        pointCross = len(prevGenSelect[0])
    #Working with pairs, not including the last element if length is odd
    halfLength = int(len(prevGenSelect) / 2)
    for i in range(halfLength):
        #Skip crossover of points based on given probability
        if random.random() < prob:
            #Calculate indices of two elements to swap
            firstVal = 2 * i
            secondVal = firstVal + 1
            #Swap all points up to crossover line
            for j in range(pointCross):
                swap = prevGenSelect[firstVal][j]
                prevGenSelect[firstVal][j] = prevGenSelect[secondVal][j]
                prevGenSelect[secondVal][j] = swap

#Mutation process for a new generation
def _mutateNewGen(prevGenCross, prob, alpha, minVal = -1.0, maxVal = 5.0):
    bounds = maxVal - minVal
    sign = 0
    for i in prevGenCross:
        #Skip mutation based on given probability
        if random.random() < prob:
            for index, j in enumerate(i):
                #Determine if the mutation will add or subtract
                if random.random() < .5:
                    sign = -1
                else:
                    sign = 1
                #Increment gene by the range of possible values times the modifier
                j += sign * alpha * bounds
                #If gene is outside the bounds, increment it by the extra amount
                #back inside the bounds
                if j < minVal:
                    j -= 2 * (j - minVal)
                if j > maxVal:
                    j -= 2 * (j - maxVal)
                #Assign new value to actual list
                i[index] = j

#Process a new generation using the previous one
#Cycles through selection, crossover, and mutation
#Manipulates list directly so no returns are needed
def _generateNewGen(prevGen, isMaxFitness = True, pointCross = 1, probC = .8, probM = .1, alpha = .01):
    _selectNewGen(prevGen, isMaxFitness)
    _crossNewGen(prevGen, pointCross, probC)
    _mutateNewGen(prevGen, probM, alpha)

#Run through a number of generations
#Report feedback every 10 generations, and on the final one
def singleRun(numGens = 30, isMaxFitness = True):
    cell = _initialGen(numGens, 3, -1.0, 5.0)
    fitData = _getFitnessData(cell)
    bestOfRun = {}
    if isMaxFitness:
        bestOfRun['Best Fitness'] = fitData['High Fit']
        bestOfRun['Best Vector'] = cell[fitData['High Fit Index']]
    else:
        bestOfRun['Best Fitness'] = fitData['Low Fit']
        bestOfRun['Best Vector'] = cell[fitData['Low Fit Index']]
    print("Generation 0")
    print(fitData)
    print(cell[fitData['High Fit Index']])
    print(cell[fitData['Low Fit Index']])
    print()
    for i in range(numGens):
        _generateNewGen(cell, isMaxFitness)
        fitData = _getFitnessData(cell)
        
        if isMaxFitness:
            if bestOfRun['Best Fitness'] < fitData['High Fit']:
                bestOfRun['Best Fitness'] = fitData['High Fit']
                bestOfRun['Best Vector'] = cell[fitData['High Fit Index']]
        else:
            if bestOfRun['Best Fitness'] > fitData['Low Fit']:
                bestOfRun['Best Fitness'] = fitData['Low Fit']
                bestOfRun['Best Vector'] = cell[fitData['Low Fit Index']]

        if ((i + 1) % 10) is 0:
            print("Generation %d" % (i + 1))
            print(fitData)
            print(cell[fitData['High Fit Index']])
            print(cell[fitData['Low Fit Index']])
            print()

    print(bestOfRun)

random.seed(54)

singleRun(isMaxFitness = False)



