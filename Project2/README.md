# Genetic Algorithm
Nearly identical to project 1, bitstrings replace the real numbers. We also delved a little deeper into python and read user input or a file, with default values usable instead of needing to change the script. This includes the parameters of the problem to some extent.

Where a vector before was (x, y, z) where all are real numbers, now a vector is a series of 0s and 1s, with specific splits. Bitstring lenths of 2, 3, and 4 would provide something like (01, 110, 1001) which would be represented simply as 011101001.

Fitness needs to be calculated a little differently now. The bitstring is effectively split into the separate values, and then each bit represents a different decimal value similar to binary numbers. It is not particularly important how those numbers are scaled as long as they are consistent. As before, the best result would be a string of 0s.

### Determining the next generation

Selection can still work as in project 1, but the weighting may be changed. A rank selection simply sorts each bitstring without regard to their actual fitness values, so the gap in fitness has no bearing, just the order. Proportional selection gives more weight to that, so a bitstring with a massive fitness improvement over the one before is far more likely to be selected than in rank selection. The tournament method randomly selects two bitstrings and takes the best one, which removes the worst bitstring from ever showing up in the next generation. It will always lose to the other bitstrings, where in previous methods it could randomly be chosen however small the chance.

Crossover now selects a specific point in the bitstring and swaps the values in each. Given bitstrings (00100010) and (11100111), swapping at the fifth position results in the bitstrings (00100111) and (11100010).

Mutation now randomly selects a bit to change.

## From project report for class
All three forms of input are accepted. When manual input is required, the user is first asked if they want to use default values. Default values include the three bitstring lengths given for the assignment and the set of parameters I used for the output.

Defaults:
	Bitstring Lengths: 10, 15, 20
	Minimum Value: -1.0
	Maximum Value: 5.0
	Population Size: 30
	Minimum fitness value is desired, not max
	Crossover Point: 25 (from left of combined bitstrings)
	Probability of Crossover: .8
	Probability of Mutation: .1
	Number of Runs: 30
	Number of Generations: 50
	Selection: Proportional
	Initial Random Seed: 15

The initial random seed creates a list of random seeds the length of the number of runs. Each run is almost certain to have a different random seed, though an additional check to make sure there are no duplicates could be an easy addition. This also ensures that there will be a random seed for each run without requiring an additional list to be passed in and checking the length.

#### Output
Would you like to use default values? (y/n): y

Mean of Best of Runs: 1.546754038517247
Standard Deviation of Best of Runs: 1.2418226380700574
Best of Best of Runs: 0.221587744923454
  X0: 0011010001
  X1: 001011011100010
  X2: 00111100000010110001
