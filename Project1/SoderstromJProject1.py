
import random
from pprint import pprint as pp
from copy import deepcopy
from collections import OrderedDict as od

#Stores a dictionary of runs labeled by run number
#Will print data from all runs at once
class RunCollection:
    #Initialize with the number of runs, issuing a warning if the number is exceeded
    #Sets up a dictionary to store individual run data
    def __init__(self, maxRuns):
        self.maxRuns = maxRuns
        self.currentRun = 0
        self.allRunData = od()

    #Adds an empty run to the dictionary if there is room and returns it
    #Issues a warning if another would exceed the maximum number
    #Increments currentRun so it always points to the most recent
    def addAndUseRun(self, numGens, randomSeed, isMaxFitness = True):
        if self.currentRun < self.maxRuns:
            newRun = SingleRunResults(numGens, randomSeed, isMaxFitness)
            self.currentRun += 1
            self.allRunData['Run ' + str(self.currentRun)] = newRun
            return self.allRunData['Run ' + str(self.currentRun)]
        else:
            print("Warning: more runs than expected, user wanted max of %d runs." % self.numRuns)
            return None

    #Allows access to any run added before the current run in case it is needed
    def getRunNum(self, num):
        if num > 0 and num <= self.currentRun:
            return self.allRunData['Run ' + str(num)]
        else:
            print("Warning: run number %d does not exist." % num)
            return None

    #Gets the maximum number of runs allowed
    def getMaxRuns(self):
        return self.maxRuns

    #Gets the current number of runs stored
    def getCurrentRun(self):
        return self.currentRun

    #Calculate averages for data across all runs
    def prepareAverages(self):
        self.averageRunData = {}
        avgOfAvgGen = {}
        avgOfBestGen = {}
        bestRuns = []

        #Initializes values for all generations stored in runs
        #Required so we may increment them in one loop
        for i in self.allRunData['Run 1'].getGenResults():
            avgOfAvgGen[i] = 0
            avgOfBestGen[i] = 0

        #Increments values for all generations from each run, stored in a dictionary
        #and labeled by generation number, for averages across generations
        for key, run in self.allRunData.items():
            tempData = run.getGenResults()
            for genKey, value in tempData.items():
                avgOfAvgGen[genKey] += value['Average Fitness']
                #Checks if we wanted to minimize or maximize fitness before incrementing
                #with the correct value
                if run.getIsMaxFitness():
                    avgOfBestGen[genKey] += value['High Fitness']
                else:
                    avgOfBestGen[genKey] += value['Low Fitness']

            #Stores all the best of run fitness values. Keeps them all to calculate
            #standard deviation in addition to the average. Not a dictionary because
            #there is only one type of value to track.
            tempBest = run.getBestOfRun()
            bestRuns.append(tempBest['Best Fitness'])

        #Finally, average out the values based on the current number of runs
        #Avoids cases of not using the maximum number of runs and getting data already
        for key, value in avgOfAvgGen.items():
            avgOfAvgGen[key] = value / self.currentRun
        for key, value in avgOfBestGen.items():
            avgOfBestGen[key] = value / self.currentRun

        #Calculated average and standard deviation of the best-of-run fitness values
        avgBest = sum(bestRuns) / len(bestRuns)
        sdBest = 0
        for i in bestRuns:
            sdBest += (i - avgBest) ** 2
        sdBest / len(bestRuns)
        sdBest **= .5
        
        tempDict = {'Average Fitness' : avgBest, 'Standard Deviation' : sdBest}

        #Places calculated values in one dictionary
        self.averageRunData['Average Avg-of-Generation Fitness'] = avgOfAvgGen
        self.averageRunData['Average Best-of-Generation Fitness'] = avgOfBestGen
        self.averageRunData['Best-of-Runs'] = tempDict

    #Prints all data for all runs and averages across runs
    #Prints a label for each run, then
    #uses the print function of the SingleRunResults class
    #and prints the average run data calculated based on results so far
    def print(self):
        self.prepareAverages()
        for key, value in self.allRunData.items():
            print(key + ":")
            value.print()
        print("\nAverages Across All {} Runs:".format(self.currentRun))
        pp(self.averageRunData)

    #Specialized for this project, needs work to generalize
    def csvPrint(self):
        self.prepareAverages()
        
        print("Averages Across All {} Runs".format(self.currentRun))
        print("Average Avg-of-Generation Fitness")
        for key, value in self.averageRunData['Average Avg-of-Generation Fitness'].items():
            print(key + ", " + str(value))
        print()
        print("Average Best-of-Generation Fitness")
        for key, value in self.averageRunData['Average Best-of-Generation Fitness'].items():
            print(key + ", " + str(value))
        print()
        print("Best-of-Runs")
        for key, value in self.averageRunData['Best-of-Runs'].items():
            print(key + ", " + str(value))
        print()
        
        for key, value in self.allRunData.items():
            print("," + key)
            value.csvPrint()

#Stores data from a single EA run
#Initializes with the number of generations to run, stores the random seed,
#and if we want to min or max the fitness values
class SingleRunResults:
    def __init__(self, numGens, randomSeed, isMaxFitness = True):
        self.numGens = numGens
        self.randomSeed = randomSeed
        self.isMaxFitness = isMaxFitness
        self.bestOfRun = {'Best Fitness' : None}
        self.genResults = od()

    #Returns the dictionary of all data from the run
    def getGenResults(self):
        return self.genResults

    #Stores data by current generation of the best, worst, and average fitness values
    #Also stores the vectors that generated the best and worst fitness values
    def addGenResults(self, currentGen, highFit, hfVector, lowFit, lfVector, avgFit):
        tempDict = {'High Fitness' : highFit, 'High Fitness Vector' : hfVector,
                    'Low Fitness' : lowFit, 'Low Fitness Vector' : lfVector,
                    'Average Fitness' : avgFit}
        self.genResults['Generation ' + str(currentGen)] = tempDict

    #Returns the fitness value and vector of the current best of run, if any exist
    def getBestOfRun(self):
        return self.bestOfRun

    #Compares either the highest or lowest fitness value, based on desire to min or max,
    #with current best and replaces if it improves it
    def addBestOfRun(self, highFitness, highVector, lowFitness, lowVector):
        if self.isMaxFitness:
            if self.bestOfRun['Best Fitness'] is None or self.bestOfRun['Best Fitness'] < highFitness:
                self.bestOfRun['Best Fitness'] = highFitness
                self.bestOfRun['Best Vector'] = highVector
        else:
            if self.bestOfRun['Best Fitness'] is None or self.bestOfRun['Best Fitness'] > lowFitness:
                self.bestOfRun['Best Fitness'] = lowFitness
                self.bestOfRun['Best Vector'] = lowVector

    #Returns true for maximizing fitness, false for minimizing
    def getIsMaxFitness(self):
        return self.isMaxFitness

    #Prints the random seed, best of run results, and then the overall results
    def print(self):
        print("Random Seed: {}".format(self.randomSeed))
        pp(self.bestOfRun)
        pp(self.genResults)

    #Specialized for printing this particular project format to a csv, needs adjusting
    #for general use
    def csvPrint(self):
        print("Random Seed:,{0},Best Fitness:,{1:.6f},Best Vector:,\"{2:.6f}".format(self.randomSeed,
                                                                    self.bestOfRun['Best Fitness'],
                                                                    self.bestOfRun['Best Vector'][0]) +
              chr(10) + "{0:.6f}".format(self.bestOfRun['Best Vector'][1]) +
              chr(10) + "{0:.6f}\"".format(self.bestOfRun['Best Vector'][2]))
        print("Generation,\"Average" + chr(10) + "Fitness\",\"Worst" + chr(10) + "Fitness\",\"Worst" +
              chr(10) + "Fitness" + chr(10) + "Vector\",\"Best" + chr(10) + "Fitness\",\"Best" +
              chr(10) + "Fitness" + chr(10) + "Vector\"")
        for key, value in self.genResults.items():
            print(key.rsplit(" ")[1] + ",{0:.6f},{1:.6f},\"{2:.6f}".format(value['Average Fitness'],value['High Fitness'],
                                                          value['High Fitness Vector'][0]) +
                  chr(10) + "{0:.6f}".format(value['High Fitness Vector'][1]) + 
                  chr(10) + "{0:.6f}\",{1:.6f},\"{2:.6f}".format(value['High Fitness Vector'][2], value['Low Fitness'],
                                              value['Low Fitness Vector'][0]) + 
                  chr(10) + "{0:.6f}".format(value['Low Fitness Vector'][1]) +
                  chr(10) + "{0:.6f}\"".format(value['Low Fitness Vector'][2]))
        print()
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
        #Avoids copying references, prevents manipulating multiple lines at once
        tempList.append(deepcopy(prevGen[copyIndex]))

    #Set our new selection list to the input
    for i in indices:
        prevGen[i] = tempList[i]

#Crossover process for a new generation
def _crossNewGen(prevGenSelect, pointCross, prob):
    crossCount = 0
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
            crossCount += 1
            #Calculate indices of two elements to swap
            firstVal = 2 * i
            secondVal = firstVal + 1
            #Swap all points up to crossover line
            for j in range(pointCross):
                swap = prevGenSelect[firstVal][j]
                prevGenSelect[firstVal][j] = prevGenSelect[secondVal][j]
                prevGenSelect[secondVal][j] = swap
    #print("Number of Crossovers: %d" % crossCount)

#Get the mutated value of an input, making sure to keep it within bounds
def _getMutatedValue(value, alpha, minVal, maxVal):
    count = 0
    bounds = maxVal - minVal
    sign = 1
    if random.random() < .5:
        sign = -1
    tempVal = maxVal + 1
    #Continue looping until mutated value is within bounds or 5 attempts are made
    while count < 5 and (tempVal < minVal or tempVal > maxVal):
        count += 1
        #Set the modifier to a randomized value maxed at the alpha * bounds
        #and set to the appropriate sign
        modifier = random.random() * alpha * sign * bounds
        #print("Modifier: %f" % modifier)
        tempVal = value + modifier
    #Clamp mutated value to min or max if still outside bounds
    if tempVal < minVal:
        tempVal = minVal
    elif tempVal > maxVal:
        tempVal = maxVal
    return tempVal
        

#Mutation process for a new generation
def _mutateNewGen(prevGenCross, prob, alpha, minVal = -1.0, maxVal = 5.0):
    mutateCount = 0
    for index, i in enumerate(prevGenCross):
        for innerIndex, j in enumerate(i):
            #Skip mutation based on given probability
            if random.random() < prob:
                mutateCount += 1
                prevGenCross[index][innerIndex] = _getMutatedValue(j, alpha, minVal, maxVal)
    #print("Number of Mutations: %d" % mutateCount)

#Process a new generation using the previous one
#Cycles through selection, crossover, and mutation
#Manipulates list directly so no returns are needed
def _generateNewGen(prevGen, isMaxFitness = True, pointCross = 1, probC = .8, probM = .1, alpha = .01):
    _selectNewGen(prevGen, isMaxFitness)
    _crossNewGen(prevGen, pointCross, probC)
    _mutateNewGen(prevGen, probM, alpha)

#Run through a number of generations
#Report feedback every 10 generations, and on the final one
#Expects a SingleRunResults class
def singleRun(storeRun, numGens = 50):
    isMaxFitness = storeRun.getIsMaxFitness()
    cell = _initialGen(numGens, 3, -1.0, 5.0)
    fitData = _getFitnessData(cell)
    storeRun.addGenResults(0, fitData['High Fit'], cell[fitData['High Fit Index']],
                           fitData['Low Fit'], cell[fitData['Low Fit Index']],
                           fitData['Average Fit'])
    storeRun.addBestOfRun(fitData['High Fit'], cell[fitData['High Fit Index']],
                          fitData['Low Fit'], cell[fitData['Low Fit Index']])
    for i in range(numGens):
        _generateNewGen(cell, isMaxFitness)
        #print("\nCell # %d" % (i + 1))
        #pprint.pprint(cell)
        if (i + 1) % 10 is 0:
            fitData = _getFitnessData(cell)
            storeRun.addGenResults(i + 1, fitData['High Fit'], cell[fitData['High Fit Index']],
                                   fitData['Low Fit'], cell[fitData['Low Fit Index']],
                                   fitData['Average Fit'])
            storeRun.addBestOfRun(fitData['High Fit'], cell[fitData['High Fit Index']],
                                  fitData['Low Fit'], cell[fitData['Low Fit Index']])

seeds = [ 54,  30, 101,  67,  34,
          22,  99,  32,  43,  95,
           2, 145, 245, 723,  46,
         123, 823, 711, 911, 194,
           8, 238, 234, 995, 204,
         899, 375, 112, 276, 419]

moreRuns = RunCollection(30)
for i in range(moreRuns.getMaxRuns()):
    random.seed(seeds[i])
    singleRun(moreRuns.addAndUseRun(50, seeds[i], False))
moreRuns.print()
#moreRuns.csvPrint()


