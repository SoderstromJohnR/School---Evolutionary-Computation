#########################################
# Author: John Soderstrom
# Due: 5/1/2020
#
# EA for the knapsack problem. Set for size 20,
# each entry has its own weight and value. The goal
# is to maximize the value while staying under
# a weight cap. Bitstrings that go over the weight
# remain in the selection process but are penalized
# and not considered for the best of a run as long as
# one under the weight cap exists.
#
# Special cases provide similar values for elements in
# the knapsack, and trivial sets of weights that either
# allow all elements to be included, or none of them.
#
# In normal cases, values are randomized from 1 to 20
# (the size of the knapsack). Weights are also randomized,
# but more strictly regulated. The sum of the weights must be
# twice the weight cap or more. If it is not, the weights will
# increase incrementally until they are. The idea is that on
# average, half of the elements in the knapsack will make
# up the best solution, allowing the greatest possible
# variety of solutions (choosing 10 out of 20). The best solution
# will not necessarily use half of the elements, but it is
# more likely to be near that.
#
# The initial weights may be set from 1 to 4 times the capacity
# divided by size. On average, each element will be twice the
# capacity divided by size. Adding each element will negate the size,
# adding to what is, on average, twice the weight cap. That fits what I
# wanted in the previous section, with the incrementing covering when
# the sum isn't enough.
#
# For each instance (one normal, two trivial with tiny or large weights),
# the weights, values, weight cap (capacity), and average of the best of
# each run are output. Other print statements commented out cover
# listing the total value, penalty score (0 is best, followed by negative
# values near 0, with positives failing), and the actual bit string
# were included to help with debugging.
#########################################

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
    def __init__(self, maxRuns, knapsack, numGens, bitLength, popSize, pointCross, probCross,
                 probMut, randomSeeds):
        self.maxRuns = maxRuns
        self.numGens = numGens
        self.bitLength = bitLength
        self.populationSize = popSize
        self.pointCross = pointCross
        self.probCross = probCross
        self.probMut = probMut
        self.randomSeeds = randomSeeds
        self.allRunData = od()
        self._generateRuns(knapsack)

    ###
    # Fill ordered dictionary with each run
    ###
    def _generateRuns(self, knapsack):
        for i in range(self.maxRuns):
            newRun = SingleRun(knapsack, self.numGens, self.bitLength, self.populationSize,
                               self.pointCross, self.probCross, self.probMut, self.randomSeeds[i])
            self.allRunData['Run ' + str(i + 1)] = newRun

###
# Stores data from a single GA run
# Initializes with the number of generations to run, stores the random seed,
# and if we want to min or max the fitness values
###
class SingleRun:
    def __init__(self, knapsack, numGens, bitLength, popSize, pointCross, probCross, probMut, randomSeed):
        self.numGens = numGens
        self.bitLength = bitLength
        self.populationSize = popSize
        self.pointCross = bitLength - pointCross
        self.probCross = probCross
        self.probMut = probMut
        random.seed(randomSeed)
        self.bestOfRun = {'Best Value' : None, 'Best Penalty' : None, 'Best BitString' : None}
        self.genResults = od()
        self._initialGen()
        self._addBestOfRun(knapsack)
        if self.pointCross <= 0 or self.pointCross >= self.bitLength:
            print("WARNING: crossover point is not within the bit string.")
            print("    The crossover process will have no actual impact.")
        self._generateNewGen(knapsack)

    ###
    # Creates the initial generation for the GA
    ###
    def _initialGen(self):
        self.generation = []
        # Creates a chromosome for the entire population size
        for n in range(self.populationSize):
            initial = 0
            tempSize = self.bitLength
            # Randomly flags bits in length of chromosome
            while tempSize > 0:
                tempSize = tempSize - 1
                if random.random() < .5:
                    initial = initial | 1<<tempSize
            self.generation.append(initial)

    ###
    # Selection process, binary tournament, for a new generation
    ###
    def _selectNewGen(self, knapsack):
        tempList = []
        for i in range(popSize):
            tour1 = random.randint(0, self.populationSize - 1)
            tour2 = random.randint(0, self.populationSize - 1)
            # Ensure that two different entries are selected
            while tour1 is tour2:
                tour2 = random.randint(0, self.populationSize - 1)
                
            pen1 = self._penalty(knapsack, self.generation[tour1])
            pen2 = self._penalty(knapsack, self.generation[tour2])

            select = 0
            # If both are over capacity, take the lesser weight
            if pen1 > 0 and pen2 > 0:
                if pen1 < pen2:
                    select = tour1
                else:
                    select = tour2
            # If one is over capacity, take the other
            if pen1 < 0 or pen2 < 0:
                if pen1 < pen2:
                    select = tour1
                else:
                    select = tour2
            # If both are under capacity, take the higher value
            else:
                fit1 = knapsack.getTotalValue(self.generation[tour1])
                fit2 = knapsack.getTotalValue(self.generation[tour2])
                if fit1 > fit2:
                    select = tour1
                else:
                    select = tour2
                    
            tempList.append(deepcopy(self.generation[select]))
        self.generation = tempList

    ###
    # Crossover process for a new generation
    ###
    def _crossNewGen(self):
        # Ignore process if it would have no impact
        if self.pointCross <= 0 or self.pointCross >= self.bitLength:
            return
        
        # Working with pairs, not including the last element if length is odd
        halfLength = int(self.populationSize / 2)
        for i in range(halfLength):
            # Skip crossover of points based on given probability
            if random.random() < self.probCross:
                # Calculate indices of two elements to swap
                firstVal = 2 * i
                secondVal = firstVal + 1
                # Swap bitstrings at crossover point
                # Two variables used to avoid copying issues with list references
                swap1 = self.generation[firstVal]
                swap2 = self.generation[secondVal]
                self.generation[secondVal] = int((self.generation[secondVal] / (2 ** self.pointCross)))<<self.pointCross
                self.generation[firstVal] = int((self.generation[firstVal] / (2 ** self.pointCross)))<<self.pointCross
                for j in range(self.pointCross + 1):
                    self.generation[secondVal] = self.generation[secondVal] | (swap1 % (2 ** j))
                    self.generation[firstVal] = self.generation[firstVal] | (swap2 % (2 ** j))

    ###
    # Mutation process for a new generation
    ###
    def _mutateNewGen(self):
        for index, i in enumerate(self.generation):
            for n in range(self.bitLength):
                # Flip each bit based on random chance and given probability
                if random.random() < self.probMut:
                    i = i ^ 1<<n
            # Assign mutated bit string to the list
            self.generation[index] = i

    ###
    # Process a new generation using the previous one
    # Cycles through selection, crossover, and mutation
    # Manipulates list directly so no returns are needed
    ###
    def _generateNewGen(self, knapsack):
        for i in range(self.numGens):
            self._selectNewGen(knapsack)
            self._crossNewGen()
            self._mutateNewGen()
            self._addBestOfRun(knapsack)

    ###
    # Static, deviation dependant penalty approach
    # Positive values are over capacity
    ###
    def _penalty(self, knapsack, chromo, constant = 0):
        if constant is 0:
            constant = int(knapsack.size / 4)
        return constant * (knapsack.getTotalWeight(chromo) - knapsack.capacity)

    ###
    # Gets the best bitstring of the run.
    ###
    def _addBestOfRun(self, knapsack):
        # Set an initial value for best of run on first generation
        start = 0
        if self.bestOfRun['Best Penalty'] is None:
            start = 1
            self.bestOfRun['Best Penalty'] = self._penalty(knapsack, self.generation[0])
            self.bestOfRun['Best BitString'] = self.generation[0]
            self.bestOfRun['Best Value'] = knapsack.getTotalValue(self.generation[0])

        # Loop through all bitstrings in generation to check for best
        for i in range(start, self.populationSize):
            tempPen = self.bestOfRun['Best Penalty']
            newPen = self._penalty(knapsack, self.generation[i])
            
            # If the new string is over capacity, only accept if the
            # old one had a worse penalty
            if newPen > 0 and tempPen > newPen:
                self.bestOfRun['Best Penalty'] = newPen
                self.bestOfRun['Best BitString'] = self.generation[i]
                self.bestOfRun['Best Value'] = knapsack.getTotalValue(self.generation[i])

            # If the new string is under capacity, compare value to the current best
            # Accept the new one if its value is higher
            elif newPen <= 0:
                tempVal = self.bestOfRun['Best Value']
                newVal = knapsack.getTotalValue(self.generation[i])
                if tempVal < newVal:
                    self.bestOfRun['Best Penalty'] = newPen
                    self.bestOfRun['Best BitString'] = self.generation[i]
                    self.bestOfRun['Best Value'] = newVal

    ###
    # Returns the fitness value and vector of the current best of run, if any exist
    ###
    def getBestOfRun(self):
        return self.bestOfRun

###
# Stores values and weights for a knapsack of given size
# Each value and weight is associated with a specific index
# Includes options for special or trivial cases
#   Special = 1: weights are the minimum so all may be included
#   Special = 2: weights are made large enough none may be included
###
class knapsack:
    def __init__(self, size, capacity, special = 0):
        self.size = size
        self.values = []
        self.weights = []
        self.capacity = capacity

        # If special is set, for 1 give small trivial weights. For 2 give
        # large trivial weights. Small weights should allow sum to less than
        # capacity, allowing all elements to be included. Large weights should
        # all be over capacity.
        if special > 0 and special <= 2:
            self.values = [(i % 10 + 1) for i in range(size)]
            if special is 1:
                self.weights = [1] * size
            else:
                self.weights = [capacity * 100] * size
        # For normal cases
        else:
            # Allow a unique value for every slot. This is unlikely, but will
            # still provide varied values to help with giving multiple solutions.
            self.values = [(random.randint(1, size)) for i in range(size)]
            # Low weight limit for randomization will, on average, have all
            # weights sum to twice the capacity
            smWeight = int(capacity * 4 / size)
            # Sum of weights must be at least twice the capacity
            tpWeight = int(capacity * 2)
            self.weights = [(random.randint(1, smWeight)) for i in range(size)]

            # If the sum of weights is less than twice the capacity, increment
            # them unless if it would place them over the smaller limit used.
            # This attempts to keep weights spread and the number of elements in
            # the best solution closer to half of them.
            while sum(self.weights) < tpWeight - 1:
                index = random.randint(0, size - 1)
                if self.weights[index] < smWeight:
                    self.weights[index] += 1

            # Add a check to modify weights that go well over the limit
            # Randomly decrement weights that are greater than 1 to
            # lower weights back to twice the capacity.
            while sum(self.weights) > tpWeight + 1:
                index = random.randint(0, size - 1)
                if self.weights[index] > 1:
                    self.weights[index] -= 1

    ###
    # Get the combined value of all elements currently included in the knapsack
    # from a chromosome (set to 1, not 0).
    ###
    def getTotalValue(self, chromo):
        value = 0
        breakPoint = self.size
        for i in range(self.size):
            breakPoint -= 1
            temp = int(chromo / (2 ** breakPoint))
            temp = temp % 2
            value += temp * self.values[i]
        return value

    ###
    # Get the combined weights of all elements currently included in the knapsack
    # from a chromosome (set to 1, not 0).
    ###
    def getTotalWeight(self, chromo):
        value = 0
        breakPoint = self.size
        for i in range(self.size):
            breakPoint -= 1
            temp = int(chromo / (2 ** breakPoint))
            temp = temp % 2
            value += temp * self.weights[i]
        return value

# Set initial values for the problem
knapSize = 20       # The number of elements (bits) in each chromosome (space in knapsack)
popSize = 20        # The number of chromosomes in a generation
capacity = 60       # The weight cap, or capacity, of the knapsack. Penalize anything higher.
numGens = 50        # The number of generations each run will go through improving
numRuns = 10        # The number of runs made of all those generations from random initial states

pointCross = 8      # Point in the bitstring where crossover happens. Between 0 and knapsize(not inclusive)
probCross = .8      # Probability that crossover occurs with a pair.
probMut = .05       # Probability that mutation happens on a bit.

# Random seeds passed into the run collection object, handling all runs
seeds = [ 30,  45, 101,   3, 923,
         111,  23, 456, 234, 500,
          76,  67, 323, 610, 400,
         156, 211, 349, 982, 820]

# Do 3 instances. One normal, two special cases with trivial weights.
for i in range(3):
    knap = knapsack(knapSize, capacity, i)
    allRuns = RunCollection(numRuns, knap, numGens, knapSize, popSize, pointCross, probCross,
                            probMut, seeds)
    avgVal = 0
    for x, val in allRuns.allRunData.items():
        avgVal += val.bestOfRun['Best Value']
    avgVal /= numRuns
    print("Instance {}".format(i + 1))
    print("  Weights: {}".format(knap.weights))
    print("  Values: {}".format(knap.values))
    print("  Capacity: {}".format(capacity))
    print("  Average of Best Runs: {}".format(avgVal))
    print()

    # Printing additional information for debugging
##    for x, val in allRuns.allRunData.items():
##        temp = val.getBestOfRun()
##        print(temp['Best Value'])
##        print(temp['Best Penalty'])
##        print(format(temp['Best BitString'], '020b'))
##    print()

