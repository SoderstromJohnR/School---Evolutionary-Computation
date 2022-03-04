######################################
# Author: John Soderstrom
# Due: 5/11/2020
#
# Uses the Jaya algorithm to solve a basic problem.
# The goal is to take three values and reduce the sums of the
# squares as low as possible - low fitness values are preferred to high.
#
# Each chromosome has three floating point values. The minimum for
# each is -1.0, and the maximum for each is 5.0. The answer to the solution
# is not simply to reduce each to their minimum, because the obvious
# best value, 0, is somewhere inbetween.
#
# Each run stores the best vector of the run and its fitness.
# A run collection object stores an ordered dictionary of
# all runs. It also takes a list of seeds to set up a new
# seed for each run. This allows a single seed to produce
# multiple variations with one change while still being predictable.
#####################################

import random
from pprint import pprint as pp
from copy import deepcopy
from collections import OrderedDict as od

###
# Stores a dictionary of runs labeled by run number
# Will print data from all runs at once
###
class RunCollection:
    ###
    # Initialize with the number of runs, issuing a warning if the number is exceeded
    # Sets up a dictionary to store individual run data
    ###
    def __init__(self, numRuns, numGens, popSize, chromeSize, minVal, maxVal,
                 randomSeeds, isMaxFitness = True):
        self.numRuns = numRuns
        self.numGens = numGens
        self.populationSize = popSize
        self.chromeSize = chromeSize
        self.minVal = minVal
        self.maxVal = maxVal
        self.isMaxFitness = isMaxFitness
        self.randomSeeds = randomSeeds
        self.allRunData = od()
        self._generateRuns()

    ###
    # Fill ordered dictionary with each run
    ###
    def _generateRuns(self):
        for i in range(self.numRuns):
            self.allRunData[i] = SingleRun(self.numGens, self.populationSize,
                                           self.chromeSize, self.minVal, self.maxVal,
                                           self.randomSeeds[i], self.isMaxFitness)
        self._prepareData()

    ###
    # Set up average and standard deviation values of all best of runs
    ###
    def _prepareData(self):
        # Set up average both to have it, and for standard deviation next
        self.avgFit = 0
        for i in range(self.numRuns):
            self.avgFit += self.allRunData[i].bestOfRun['Best Fitness']
        self.avgFit /= self.numRuns

        # Set up standard deviation of all best of runs
        self.stdFit = 0
        for i in range(self.numRuns):
            tempVal = self.allRunData[i].bestOfRun['Best Fitness']
            self.stdFit = tempVal * tempVal
        self.stdFit /= self.numRuns - 1
        self.stdFit = pow(self.stdFit, .5)
        
    ###
    # Print best of run data across all runs, then average and standard deviation
    ###
    def print(self):
        for i in range(self.numRuns):
            print('Run', i + 1)
            self.allRunData[i].print()
            print()

        print('Average Fitness:', self.avgFit)
        print('Standard Deviation:', self.stdFit)

###
# Stores data from a single GA run
# Initializes with the number of generations to run, stores the random seed,
# and if we want to min or max the fitness values.
# Then runs all generations, tracking the best of the entire run.
###
class SingleRun:
    def __init__(self, numGens, popSize, chromeSize, minVal, maxVal,
                 randomSeed, isMaxFitness = True):
        self.numGens = numGens
        self.populationSize = popSize
        self.chromeSize = chromeSize
        self.isMaxFitness = isMaxFitness
        random.seed(randomSeed)
        self.bestOfRun = {'Best Fitness' : None, 'Best Vector' : None}
        self.genResults = od()
        self._initialGen(minVal, maxVal)
        self._addBestOfRun()
        self._generateGens(minVal, maxVal)

    ###
    # Creates the initial generation for the GA
    ###
    def _initialGen(self, minVal, maxVal):
        self.generation = []
        # Creates a chromosome for the entire population size
        for i in range(self.populationSize):
            initial = []
            for j in range(self.chromeSize):
                newVal = random.random()
                newVal *= maxVal - minVal
                newVal += minVal
                initial.append(newVal)
            self.generation.append(initial)

    ###
    # Generate new generations with the Jaya Algorithm
    ###
    def _generateGens(self, minVal, maxVal):
        # Repeat for all generations we want
        for i in range(self.numGens):
            extremes = self._genExtremes()
            # Generate new random vectors r1, r2 from 0 to 1 for each generation
            r1, r2 = [], []
            for i in range(len(self.generation[0])):
                r1.append(random.random())
                r2.append(random.random())

            # Loop through all members of the population to test for a new vector
            for countChrome, chrome in enumerate(self.generation):
                newVector = []
                # Build up a new potential vector using the same random values
                # for all chromosomes in one generation
                for countGene, gene in enumerate(chrome):
                    newVal = gene + r1[countGene] * (extremes[0][countGene] - abs(gene))
                    newVal -= r2[countGene] * (extremes[1][countGene] - abs(gene))
                    # Clamp new value if necessary
                    if newVal < minVal:
                        newVal = minVal
                    if newVal > maxVal:
                        newVal = maxVal
                    newVector.append(newVal)
                
                # If the new vector's fitness is better, replace the old one.
                if self.isMaxFitness:
                    if self._fitness(chrome, False) < self._fitness(newVector, False):
                        self.generation[countChrome] = newVector
                else:
                    if self._fitness(chrome, False) > self._fitness(newVector, False):
                        self.generation[countChrome] = newVector

            # Check for a new best of run
            self._addBestOfRun()

    ###
    # Get best and worst fitness vectors of a generation.
    # Returns results[BestVector, Worst Vector] depending on
    # preference for high or low fitness.
    # Returns copies so the vectors will not be altered while
    # generating a new generation.
    ###
    def _genExtremes(self):
        # Get fitness values and start count at the first in the generation
        startFit = self._fitness(0)
        high = 0
        highFit = startFit
        low = 0
        lowFit = startFit

        # Check fitness values for later entries against the first
        for i in range(1, self.populationSize):
            newFit = self._fitness(i)
            if newFit > highFit:
                highFit = newFit
                high = i
            if newFit < lowFit:
                lowFit = newFit
                low = i
        results = []

        # Order extreme vectors best first, worst second. Return them.
        if self.isMaxFitness:
            results.append(self.generation[high].copy())
            results.append(self.generation[low].copy())
        else:
            results.append(self.generation[low].copy())
            results.append(self.generation[high].copy())
        return results

    ###
    # Fitness function for the project
    # Returns sum of squares of all x values of a chromosome
    # Usually expects val to be the index of the generation.
    # Will sometimes see it as a potential new vector (list) instead.
    ###
    def _fitness(self, val, isInt = True):
        sumVals = 0
        if isInt:
            for x in self.generation[val]:
                sumVals += x * x
        else:
            for x in val:
                sumVals += x * x
        return sumVals

    ###
    # Gets the best bitstring of the run.
    ###
    def _addBestOfRun(self):
        if self.bestOfRun['Best Fitness'] is None:
            self.bestOfRun['Best Fitness'] = self._fitness(0)
            self.bestOfRun['Best Vector'] = self.generation[0]

        # If min fitness is better, use a temporary modifier for checking
        # which fitness values are better with one check.
        modifier = -1
        if self.isMaxFitness:
            modifier = 1

        # Check for better fitness values. Always check for greater values,
        # if min are better we multiple each by -1 first.
        for i in range(self.populationSize):
            fit = self._fitness(i)
            if self.bestOfRun['Best Fitness'] * modifier <= fit * modifier:
                self.bestOfRun['Best Fitness'] = fit
                self.bestOfRun['Best Vector'] = self.generation[i]

    ###
    # Returns the fitness value and vector of the current best of run, if any exist
    ###
    def getBestOfRun(self):
        return self.bestOfRun

    ###
    # Prints the best of run, its fitness and the actual vector
    ###
    def print(self):
        pp(self.bestOfRun)


random.seed(15)
seeds = []
numRuns = 30
numGens = 50
popSize = 20
chromeSize = 3
minVal = -1.0
maxVal = 5.0

for i in range(numRuns):
    seeds.append(random.randint(0, 999))

fullRuns = RunCollection(numRuns, numGens, popSize, chromeSize, minVal, maxVal, seeds, False)
fullRuns.print()
