#################################################
# Author: John Soderstrom
# Due: 5/1/2020
#
# Runs a GA multiple times to find the lowest possible
# value given 3 bitstrings that represent floating point
# numbers between 2 given numbers (-1.0 and 5.0 for the problem).
#
# usage:
# SoderstromJProject2.py
# SoderstromJProject2.py -f filename
# SoderstromJProject2.py [-h] -l L [-m {t,f}] [-s {0,1,2}] Minimum Maximum
#                           PopSize NumRuns NumGens CrossPoint PCross PMut RandomSeed
#
#       -l L        Repeatable, integers > 0. The number of bits for each value.
#       -m {t,f}    Maximum fitness value is preferred. True or False.
#       -s {0,1,2}  Selection method. Proportional, Binary Tournament, Linear Ranking.
#       Minimum     The minimum value a bitstring can be.
#       Maximum     The maximum value a bitstring can be.
#       PopSize     The number of chromosomes in a generation.
#       NumRuns     The number of runs the GA will run.
#       NumGens     The number of generations in each run.
#       CrossPoint  The splitting point to cross 2 chromosomes. 1 to full length - 1.
#       PCross      Probability that crossover will occur for each pair. 0 - 1.
#       PMut        Probability that mutation will occur on each bit. 0 - 1.
#       RandomSeed  Initial seed for randomizer, integer 0 - 999.
#
# File requirements to accept for input. Tag followed by description.
#   BitLength:      Integers > 0 separated by whitespace. At least 1 required.
#   Min:            The minimum value a bitstring can be.
#   Max:            The maximum value a bitstring can be.
#   Pop:            The number of chromosomes in a generation.
#   Runs:           The number of runs the GA will run.
#   Gens:           The number of generations in each run.
#   CrossPoint:     The splitting point to cross 2 chromosomes. 1 to full length - 1.
#   P_Cross:        Probability that crossover will occur for each pair. 0 - 1.
#   P_Mut:          Probability that mutation will occur on each bit. 0 - 1.
#   RandomSeed:     Initial seed for randomizer, integer 0 - 999.
#   (Optional below)
#   Selection:      Selection method. Proportional, Binary Tournament, Linear Ranking.
#                    {0, 1, 2} Defaults to 0, Proportional.
#   MaxFitness:     Maximum fitness value is preferred. {t, f} True or False.
#
# Not perfect, error reporting for input is not quite complete. But errors are checked,
# and multiple methods of input are allowed.
#
# Given lengths of bitstrings for all values in the problem, attempts multiple runs
# to find the best possible bitstrings to maximize or minimize fitness. The function
# will square the values of each bitstring and add them together.
#
# Once all runs are complete, the mean, standard deviation, and best of all
# best of runs are printed to the screen.
#################################################

import random, argparse, sys, getopt
from pprint import pprint as pp
from copy import deepcopy
from collections import OrderedDict as od

###
# Stores a dictionary of runs labeled by run number
# Will print data from all runs at once
###
class RunCollection:
    # Initialize with the number of runs, issuing a warning if the number is exceeded
    # Sets up a dictionary to store individual run data
    def __init__(self, maxRuns, vectorLengths):
        self.maxRuns = maxRuns
        self.currentRun = 0
        self.allRunData = od()
        self.vectorLengths = vectorLengths

    # Adds an empty run to the dictionary if there is room and returns it
    # Issues a warning if another would exceed the maximum number
    # Increments currentRun so it always points to the most recent
    def addAndUseRun(self, numGens, randomSeed, isMaxFitness = True):
        if self.currentRun < self.maxRuns:
            newRun = SingleRunResults(numGens, randomSeed, isMaxFitness)
            self.currentRun += 1
            self.allRunData['Run ' + str(self.currentRun)] = newRun
            return self.allRunData['Run ' + str(self.currentRun)]
        else:
            print("Warning: more runs than expected, user wanted max of %d runs." % self.numRuns)
            return None

    # Allows access to any run added before the current run in case it is needed
    def getRunNum(self, num):
        if num > 0 and num <= self.currentRun:
            return self.allRunData['Run ' + str(num)]
        else:
            print("Warning: run number %d does not exist." % num)
            return None

    # Gets the maximum number of runs allowed
    def getMaxRuns(self):
        return self.maxRuns

    # Gets the current number of runs stored
    def getCurrentRun(self):
        return self.currentRun

    # Calculate best, mean, and standard deviations of best of run fitness values
    def prepareData(self):
        self.bestOfBest = self.getRunNum(3).bestOfRun['Best Fitness']
        self.vecOfBest = self.getRunNum(3).bestOfRun['Best Vector']
        self.meanOfBest = 0
        self.stdOfBest = 0

        # Get average of best of runs, and store the best of the best
        for key, val in self.allRunData.items():
            self.meanOfBest += val.bestOfRun['Best Fitness']
            if self.bestOfBest > val.bestOfRun['Best Fitness']:
                self.bestOfBest = val.bestOfRun['Best Fitness']
                self.vecOfBest = val.bestOfRun['Best Vector']
        self.meanOfBest /= self.maxRuns
        
        # Use average to calculate standard deviation of bests
        for key, val in self.allRunData.items():
            self.stdOfBest += (val.bestOfRun['Best Fitness'] - self.meanOfBest) ** 2
            
        self.stdOfBest /= (self.maxRuns - 1)
        self.stdOfBest = self.stdOfBest ** .5
        
    # Print all data for all best of runs
    def print(self):
        self.prepareData()
        print("Mean of Best of Runs: {}".format(self.meanOfBest))
        print("Standard Deviation of Best of Runs: {}".format(self.stdOfBest))
        print("Best of Best of Runs: {}".format(self.bestOfBest))

        # Separate vector into bit strings
        breakPoint = sum(self.vectorLengths)
        for count, i in enumerate(self.vectorLengths):
            breakPoint -= i
            tempVal = int(self.vecOfBest / (2 ** breakPoint))
            tempVal = int(tempVal % (2 ** i))
            state = "  X{}: ".format(count)
            formatLength = "0{}b".format(i)
            state += format(tempVal, formatLength)
            print(state)

###        
# Stores data from a single GA run
# Initializes with the number of generations to run, stores the random seed,
# and if we want to min or max the fitness values
###
class SingleRunResults:
    def __init__(self, numGens, randomSeed, isMaxFitness = True):
        self.numGens = numGens
        self.randomSeed = randomSeed
        self.isMaxFitness = isMaxFitness
        self.bestOfRun = {'Best Fitness' : None}
        self.genResults = od()

    # Returns the dictionary of all data from the run
    def getGenResults(self):
        return self.genResults

    # Stores data by current generation of the best, worst, and average fitness values
    # Also stores the vectors that generated the best and worst fitness values
    def addGenResults(self, currentGen, highFit, hfVector, lowFit, lfVector, avgFit):
        tempDict = {'High Fitness' : highFit, 'High Fitness Vector' : hfVector,
                    'Low Fitness' : lowFit, 'Low Fitness Vector' : lfVector,
                    'Average Fitness' : avgFit}
        self.genResults['Generation ' + str(currentGen)] = tempDict

    # Returns the fitness value and vector of the current best of run, if any exist
    def getBestOfRun(self):
        return self.bestOfRun

    # Compares either the highest or lowest fitness value, based on desire to min or max,
    # with current best and replaces if it improves it
    def addBestOfRun(self, highFitness, highVector, lowFitness, lowVector):
        if self.isMaxFitness:
            if self.bestOfRun['Best Fitness'] is None or self.bestOfRun['Best Fitness'] < highFitness:
                self.bestOfRun['Best Fitness'] = highFitness
                self.bestOfRun['Best Vector'] = highVector
        else:
            if self.bestOfRun['Best Fitness'] is None or self.bestOfRun['Best Fitness'] > lowFitness:
                self.bestOfRun['Best Fitness'] = lowFitness
                self.bestOfRun['Best Vector'] = lowVector

    # Returns true for maximizing fitness, false for minimizing
    def getIsMaxFitness(self):
        return self.isMaxFitness

###
# Fitness function for the project
# Returns fitness value of a bit string
# Takes full bitstring, list of bit string lengths, and min/max values
###
def _fitness(chromo, lengths, minVal, maxVal):
    fit = 0
    diff = maxVal - minVal
    if diff < 0:
        print("WARNING: min and max values are reversed")
    breakPoint = sum(lengths)
    for i in lengths:
        breakPoint -= i
        tempVal = int(chromo / (2 ** breakPoint))
        tempVal = int(tempVal % (2 ** i))
        tempVal /= (2 ** i)
        fit += (diff * tempVal + minVal) ** 2
    return fit

###
# Obtain a list of fitness values for a generation
###
def _getFitnessValues(listVal, lengths, minVal, maxVal):
    fitList = []
    for i in listVal:
        fitList.append(_fitness(i, lengths, minVal, maxVal))
    return fitList

###
# Manipulate fitness values for processing minimum fitness
# Modifies given list, no return needed
###
def _minModFitness(fitList):
    # Store minimum and maximum fitness values to reverse them
    # without resulting in heavily exaggerated values
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
    # Sum of the min and max fitnesses will flip them and
    # keep other values in between
    modFit = minFit + maxFit
    for index, i in enumerate(fitList):
        fitList[index] = modFit - i
        
###
# Convert fitness values to percents for random selection
# Modifies given list, no return needed
###
def _percentFitness(fitList):
    # Calculate sum to convert all fitness values to percents
    sumFit = 0
    for i in fitList:
        sumFit += i

    # Store previous value to generate stacking percentages
    # A random number between 0 and 1 may be used to select a
    # single index
    prevVal = 0
    for index, i in enumerate(fitList):
        fitList[index] /= sumFit
        fitList[index] += prevVal
        prevVal = fitList[index]
    # Set final value to 2.0 instead of 1.0 to ensure no
    # edge case percent errors
    fitList[-1] = 2.0

###
# Obtain fitness data about a generation
# Returns a dictionary including indices of the best and worst chromosomes
###
def _getFitnessData(listVal, vectorLengths, minVal, maxVal):
    fitList = _getFitnessValues(listVal, vectorLengths, minVal, maxVal)
    fitData = {}
    for index, i in enumerate(fitList):
        # Initialize fitData to first fitness value
        if index is 0:
            fitData = {'High Fit' : i, 'High Fit Index' : index,
                       'Low Fit' : i, 'Low Fit Index' : index,
                       'Average Fit' : i}
        else:
            # Increment value for average fitness of generation
            fitData['Average Fit'] += i
            # Update best fitness and index values
            if fitData['High Fit'] < i:
                fitData['High Fit'] = i
                fitData['High Fit Index'] = index
            # Update worst fitness and index values
            if fitData['Low Fit'] > i:
                fitData['Low Fit'] = i
                fitData['Low Fit Index'] = index
    # Finalize average fitness and return list
    fitData['Average Fit'] /= len(listVal)
    return fitData

###
# Creates the initial generation for the GA
###
def _initialGen(popSize, chromoSize):
    initGen = []
    # Creates a chromosome for the entire population size
    for n in range(popSize):
        initial = 0
        tempSize = chromoSize
        # Randomly flags bits in length of chromosome
        while tempSize > 0:
            tempSize = tempSize - 1
            if random.random() < .5:
                initial = initial | 1<<tempSize
        initGen.append(initial)
    return initGen

###
# Selection process, proportional, for a new generation
###
def _selectProportNewGen(prevGen, lengths, minVal, maxVal, isMaxFit):
    indices = range(len(prevGen))
    # Get a list of all fitness values and convert to percents
    # Reverse fitness values if attempting to minimize fitness
    fitnessVals = _getFitnessValues(prevGen, lengths, minVal, maxVal)
    if not isMaxFit:
        _minModFitness(fitnessVals)
    _percentFitness(fitnessVals)
            
    # Create a new list using percentages in selection
    tempList = []
    for i in indices:
        copyIndex = 0
        randomChoice = random.random()
        # randomChoice will never be > 1, so this loop will always end before
        # out of range errors
        # Ends when we reach the percent range our randomChoice is in
        while randomChoice > fitnessVals[copyIndex]:
            copyIndex += 1
        # Avoids copying references, prevents manipulating multiple lines at once
        tempList.append(deepcopy(prevGen[copyIndex]))

    # Set our new selection list to the input
    for i in indices:
        prevGen[i] = tempList[i]

###
# Selection process, binary tournament, for a new generation
###
def _selectBinTourNewGen(prevGen, lengths, minVal, maxVal, isMaxFit):
    popSize = len(prevGen)
    tempList = []

    for i in range(popSize):
        tour1 = random.randint(0, popSize - 1)
        tour2 = random.randint(0, popSize - 1)
        # Ensure that two different entries are selected
        while tour1 is tour2:
            tour2 = random.randint(0, popSize - 1)
        fit1 = _fitness(prevGen[tour1], lengths, minVal, maxVal)
        fit2 = _fitness(prevGen[tour2], lengths, minVal, maxVal)

        # Flip fitness values for consideration if the smaller is better
        if not isMaxFit:
            fit1 *= -1
            fit2 *= -1

        # Select the chromosome with better fitness of the two to add
        if fit1 > fit2:
            tempList.append(deepcopy(prevGen[tour1]))
        else:
            tempList.append(deepcopy(prevGen[tour2]))

    # Set our new selection list to the input
    for i in range(popSize):
        prevGen[i] = tempList[i]

###
# Selection process, linear ranking, for a new generation
###
def _selectLinRankNewGen(prevGen, lengths, minVal, maxVal, isMaxFit):
    fitnessVals = _getFitnessValues(prevGen, lengths, minVal, maxVal)
    totalVals = len(prevGen)
    #Flip fitness values for ranking if smaller fitness values are better
    if not isMaxFit:
        for count, i in enumerate(fitnessVals):
            fitnessVals[count] = i * -1
    
    # Replace fitness values with ranks from 0 to number of chromosomes - 1
    # A separate list is needed to store ranks while keeping values to check against
    tempFit = fitnessVals.copy()
    for count, i in enumerate(tempFit):
        rank = 0
        for j in tempFit:
            if i > j:
                rank += 1
        fitnessVals[count] = rank
    
    tempInc = {}
    # Fill blanks with values based on duplicate ranks
    # Use a dictionary to store the number of times each value comes up
    # and increment a duplicate by that number
    for count, i in enumerate(fitnessVals):
        if i not in tempInc.keys():
            tempInc[i] = 0
        else:
            tempInc[i] += 1
            fitnessVals[count] += tempInc[i]

    probSelect = fitnessVals.copy()
    # Set probability for each rank, then make it cumulative
    # Cumulative probability will make selecting an entry easier
    cumulProb = 0
    for count, i in enumerate(probSelect):
        probSelect[count] = cumulProb + ((2 * count / (totalVals - 1)) / totalVals)
        cumulProb = probSelect[count]
    # Increase last probability in case of edge case errors
    probSelect[totalVals - 1] = 2.0
    
    tempList = []
    # Select entries for a new generation
    for i in range(totalVals):
        copyIndex = 0
        randomChoice = random.random()
        while randomChoice > probSelect[copyIndex]:
            copyIndex += 1
        print(copyIndex)
        # Use copy index to get the index of our actual selection from fitnessVals
        # fitnessVals replaced values with ranks from 0 to total chromosomes - 1
        # in order to get the correct index now
        tempList.append(deepcopy(prevGen[fitnessVals[copyIndex]]))

    # Set our new selection list to the input
    for i in range(totalVals):
        prevGen[i] = tempList[i]

###
# Crossover process for a new generation
###
def _crossNewGen(prevGenSelect, totalLength, pointCross, prob):
    crossCount = 0
    pointCross = totalLength - pointCross
    # Working with pairs, not including the last element if length is odd
    halfLength = int(len(prevGenSelect) / 2)
    for i in range(halfLength):
        # Skip crossover of points based on given probability
        if random.random() < prob:
            crossCount += 1
            # Calculate indices of two elements to swap
            firstVal = 2 * i
            secondVal = firstVal + 1
            # Swap bitstrings at crossover point
            # Two variables used to avoid copying issues with list references
            swap1 = prevGenSelect[firstVal]
            swap2 = prevGenSelect[secondVal]
            prevGenSelect[secondVal] = int((prevGenSelect[secondVal] / (2 ** pointCross)))<<pointCross
            prevGenSelect[firstVal] = int((prevGenSelect[firstVal] / (2 ** pointCross)))<<pointCross
            for j in range(pointCross + 1):
                prevGenSelect[secondVal] = prevGenSelect[secondVal] | (swap1 % (2 ** j))
                prevGenSelect[firstVal] = prevGenSelect[firstVal] | (swap2 % (2 ** j))

###
# Mutation process for a new generation
###
def _mutateNewGen(prevGenCross, totalLength, prob):
    mutateCount = 0
    for index, i in enumerate(prevGenCross):
        for n in range(totalLength):
            # Flip each bit based on random chance and given probability
            if random.random() < prob:
                i = i ^ 1<<n
        # Assign mutated bit string to the list
        prevGenCross[index] = i

###
# Process a new generation using the previous one
# Cycles through selection, crossover, and mutation
# Manipulates list directly so no returns are needed
###
def _generateNewGen(prevGen, isMaxFitness, lengths, pointCross, probC, probM, minVal, maxVal, selChoice):
    if selChoice is 0:
        _selectProportNewGen(prevGen, lengths, minVal, maxVal, isMaxFitness)
    elif selChoice is 1:
        _selectBinTourNewGen(prevGen, lengths, minVal, maxVal, isMaxFitness)
    else:
        _selectLinRankNewGen(prevGen, lengths, minVal, maxVal, isMaxFitness)
    _crossNewGen(prevGen, sum(lengths), pointCross, probC)
    _mutateNewGen(prevGen, sum(lengths), probM)

###
# Run through a number of generations
# Expects a SingleRunResults class
###
def singleRun(storeRun, numGens, vectorLengths, pointCross, probCross, probMut, 
              minVal, maxVal, selChoice):
    isMaxFitness = storeRun.getIsMaxFitness()
    cell = _initialGen(30, sum(vectorLengths))
    fitData = _getFitnessData(cell, vectorLengths, minVal, maxVal)
    storeRun.addBestOfRun(fitData['High Fit'], cell[fitData['High Fit Index']],
                          fitData['Low Fit'], cell[fitData['Low Fit Index']])
    for i in range(numGens):
        _generateNewGen(cell, isMaxFitness, vectorLengths, pointCross, probCross, probMut,
                        minVal, maxVal, selChoice)
        storeRun.addBestOfRun(fitData['High Fit'], cell[fitData['High Fit Index']],
                              fitData['Low Fit'], cell[fitData['Low Fit Index']])

# Initialize values and begin reading data from the user
xLen = []
minX = 0
maxX = 0
popSize = 0
isMaxFitness = True
pointCross = 0
probCross = 0
probMut = 0
numRuns = 0
numGens = 0
selectionChoice = 0
rSeed = 0

# Get list of arguments for first two cases, -f filename or none
argList = sys.argv[1:]

manInput = False
fileName = None
try:
    # No command line arguments pushes to manual input
    if len(argList) is 0:
        manInput = True

    # If exactly 2 arguments are given, expect a filename
    elif len(argList) is 2:
        options = "hfs:"
        args, values = getopt.getopt(argList, options)
        for curArg, curVal in args:
            if curArg in ('-f'):
                fileName = argList[-1]

    # With any other number, expect specific arguments to detail everything
    else:
        parser = argparse.ArgumentParser(description = 'Taking user input')
        parser.add_argument('-l', action = 'append', required = True)
        parser.add_argument('-m', default = 't', choices = ['t', 'f'])
        parser.add_argument('-s', default = '0', choices = ['0', '1', '2'])
        parser.add_argument('Minimum')
        parser.add_argument('Maximum')
        parser.add_argument('PopSize')
        parser.add_argument('NumRuns')
        parser.add_argument('NumGens')
        parser.add_argument('CrossPoint')
        parser.add_argument('PCross')
        parser.add_argument('PMut')
        parser.add_argument('RandomSeed')

        args = parser.parse_args()

        xLen = [int(i) for i in args.l]
        if args.m is 't':
            isMaxFitness = True
        else:
            isMaxFitness = False
        selectionChoice = int(args.s)

        try:
            minX = float(args.Minimum)
            maxX = float(args.Maximum)
            popSize = int(args.PopSize)
            numRuns = int(args.NumRuns)
            numGens = int(args.NumGens)
            pointCross = int(args.CrossPoint)
            probCross = float(args.PCross)
            probMut = float(args.PMut)
            rSeed = int(args.RandomSeed)
        except ValueError:
            print("Invalid values given, check usage statement")
            sys.exit()

except getopt.error as err:
    print(str(err))
    sys.exit()

# If two arguments were passed, attempt to open file for reading input
if fileName:
    try:
        file = open(fileName, "r")
        boolCheck = [False] * 10
        readLine = file.readlines()
        # Read all lines from file and split by spaces
        for li in readLine:
            tok = li.split()
            # Test markers for all lines. Expects all required arguments
            # and will exit if not all are given. Some defaults.
            if tok[0] == "BitLength:":
                for i in range(len(tok) - 1):
                    xLen.append(int(tok[i + 1]))
                boolCheck[0] = True
                
            if tok[0] == "Min:":
                minX = float(tok[1])
                boolCheck[1] = True
                
            if tok[0] == "Max:":
                maxX = float(tok[1])
                boolCheck[2] = True
                
            if tok[0] == "Pop:":
                popSize = int(tok[1])
                boolCheck[3] = True
                
            if tok[0] == "Runs:":
                numRuns = int(tok[1])
                boolCheck[4] = True
                
            if tok[0] == "Gens:":
                numGens = int(tok[1])
                boolCheck[5] = True
                
            if tok[0] == "CrossPoint:":
                pointCross = int(tok[1])
                boolCheck[6] = True
                
            if tok[0] == "P_Cross:":
                probCross = float(tok[1])
                boolCheck[7] = True
                
            if tok[0] == "P_Mut:":
                probMut = float(tok[1])
                boolCheck[8] = True
                
            if tok[0] == "RandomSeed:":
                rSeed = int(tok[1])
                boolCheck[9] = True
                
            if tok[0] == "Selection:":
                selectionChoice = int(tok[1])
                if selectionChoice < 0 and selectionChoice > 2:
                    selectionChoice = 0
                    
            if tok[0] == "MaxFitness:":
                if tok[1] == "f":
                    isMaxFitness = False
                else:
                    isMaxFitness = True

        # Exit if not all required arguments were given
        for check in boolCheck:
            if check is False:
                print("Missing a parameter in the file.")
                sys.exit()
             
    except IOError:
        print("Unable to open file.")
        sys.exit()
    except ValueError:
        print("Error accepting value, check them.")
        sys.exit()

# If the user chose manual input, go here. Allow
if manInput:
    choice = 0
    # Loop until user gives one of two choices
    while not (choice == "y" or choice == "n"):
        choice = input("Would you like to use default values? (y/n): ")

    # Accept default values used for the assignment
    if choice == "y":
        xLen = [10, 15, 20]
        minX = -1.0
        maxX = 5.0
        popSize = 30
        isMaxFitness = False
        pointCross = 25
        probCross = .8
        probMut = .1
        numRuns = 30
        numGens = 50
        selectionChoice = 0
        rSeed = 15
        print()

    # Allow user input for all variables
    else:
        badInput = True
        while badInput:
            try:
                minX = float(input("Please enter the minimum value for the problem: "))
                badInput = False
            except:
                pass
            
        badInput = True
        while badInput:
            try:
                maxX = float(input("Please enter the maximum value for the problem: "))
                if maxX > minX:
                    badInput = False
                else:
                    print("  Enter a value larger than {}.".format(minX))
            except:
                pass

        badInput = True
        while badInput:
            try:
                addVal = int(input("Please enter a bitstring size (at least once). Enter 0 to end: "))
                if addVal > 0:
                    xLen.append(addVal)
                elif addVal is 0 and len(xLen) > 0:
                    badInput = False
                elif addVal < 0:
                    badInput = True
            except:
                pass

        badInput = True
        while badInput:
            try:
                popSize = int(input("Please enter a population size (>0): "))
                if popSize > 0:
                    badInput = False
            except:
                pass

        badInput = True
        while badInput:
            try:
                isMax = input("Is a larger fitness value preferred? (t/f): ")
                if isMax is "t":
                    isMaxFitness = True
                    badInput = False
                elif isMax is "f":
                    isMaxFitness = False
                    badInput = False
            except:
                pass

        badInput = True
        while badInput:
            try:
                print("Which selection method do you prefer?")
                print("  Proportional, Tournament, or Linear Ranking?")
                selectionChoice = int(input("    (0, 1, 2): "))
                if selectionChoice in [0, 1, 2]:
                    badInput = False
            except:
                pass

        badInput = True
        while badInput:
            try:
                print("Where would you like the crossover point?")
                crossPoint = int(input("  (Integer from 1 - {}): ".format(sum(xLen))))
                if crossPoint > 0 and crossPoint < sum(xLen):
                    badInput = False
            except:
                pass

        badInput = True
        while badInput:
            try:
                numGens = int(input("How many generations would you like to use? "))
                if numGens > 0:
                    badInput = False
            except:
                pass

        badInput = True
        while badInput:
            try:
                numRuns = int(input("How many runs would you like to use? "))
                if numRuns > 0:
                    badInput = False
            except:
                pass

        badInput = True
        while badInput:
            try:
                probCross = float(input("What is the probability of crossover? (0-1): "))
                if probCross >= 0 and probCross <= 1:
                    badInput = False
            except:
                pass

        badInput = True
        while badInput:
            try:
                probMut = float(input("What is the probability of mutation? (0-1): "))
                if probMut >= 0 and probMut <= 1:
                    badInput = False
            except:
                pass

        badInput = True
        while badInput:
            try:
                rSeed = int(input("What initial random seed do you want? (Integer 0 - 999): "))
                if rSeed >= 0 and rSeed <= 999:
                    badInput = False
            except:
                pass
        print()
                    
# Error out for invalid values from file or command line arguments  
else:
    if len(xLen) is 0:
        print("No bitstrings are provided.")
        sys.exit()
                
    if pointCross <= 0 or pointCross >= sum(xLen):
        print("Crossover point must be between 0 and full bit length.")
        sys.exit()

    if probCross < 0 or probCross > 1 or probMut < 0 or probMut > 1:
        print("Probabilities must be between 0 and 1.")
        sys.exit()

    if maxX <= minX:
        print("The maximum value given is below the minimum.")
        sys.exit()

    if numRuns < 1 or numGens < 1:
        print("The number of runs and generations must be a positive integer.")
        sys.exit()

# Genereate a consistent block of random seeds to cover all runs
random.seed(rSeed)
seeds = []
for i in range(numRuns):
    seeds.append(random.randint(1, 999))

# Initialize all runs for given values and print out results
runs = RunCollection(numRuns, xLen)
for i in range(runs.getMaxRuns()):
    random.seed(seeds[i])
    singleRun(runs.addAndUseRun(numGens, seeds[i], False), numGens, xLen, pointCross, probCross,
              probMut, minX, maxX, selectionChoice)
runs.print()
