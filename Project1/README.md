# Evolutionary Algorithm
Not all problems have a sleek solution. In order to solve some of the harder problems, we find a way to calculate how effective a solution was, and then run multiple attempts that prune out the weaker solutions to find the best one we can. This method mimics evolution in a biological sense.

This project attempts to find a solution to an easy problem with this method. Given a range of values both negative and positive, we want to minimize the result of x^2 + y^2 + z^2. Obviously the best solution sets all three values to 0, but we cannot just do that this time.

We create several vectors of randomized values and then rate them. This problem provides an easy way to calculate the fitness - plug all three values into the above function. We prioritize the best vectors for selection, but we still allow some results from weaker solutions because parts of it might be better. After calculating the vectors for the next iteration (generation), we run it again and repeat.

As shown in the partial output below, none of the results included a value of 0. However, as the generations progressed, the values overall went closer to 0.

## Finding the next generation
The three ways to determine the next generation are selection, crossover, and mutation. Each can change a little depending on the problem being solved. In this example, each vector is in the format (x, y, z), where each is a real number.

Selection here randomly selects vectors from the previous generation to be used in the new one, with a favorable rate for the vectors with better fitness.

Crossover will take random pairs of vectors and, given a starting position in the vector, swap all elements from there to the end. By default, this will select two vectors, decide if they will be crossed, and then swap their y and z values. So (x1, y1, z1) and (x2, y2, z2) will become (x1, y2, z2) and (x2, y1, z1).

Mutation will take a vector and randomly, with a low chance, slightly shift the values. By default, the shift will be -0.1 or 0.1, clamped to the minimum and maximum values allowed.

## Partial Output
Recall fitness is the result of x^2 + y^2 + z^2
Across all 30 runs

**Generation**|** Average Fitness**
:-----:|:-----:
0| 21.12320002593753
10| 1.2210781592915534
20| 0.5526066227472156
30| 0.4745854224740938
40| 0.42343158690920296
50| 0.36314621289362653

**Generation**|** Best Fitness**
:-----:|:-----:
0| 1.1317750938801319
10| 0.45410821024342957
20| 0.4209748672207123
30| 0.3636089839610129
40| 0.332663582999799
50| 0.2820540025689745

**Best-of-Runs**
:-----:
Average Fitness, 0.26203359103355445
Standard Deviation, 2.049849182629643

Run 1's results (vectors precision lowered for space at the time)

Random Seed:|54|Best Fitness:| 0.010864| Best Vector:| 0.75131; -0.005082; 0.072068
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
**Generation**|**Average Fitness**|**Worst Fitness**| **Worst Fitness Vector**| **Best Fitness**| **Best Fitness Vector**
0| 20.713668| 61.056131| 3.473281; 4.993205; 4.905135| 1.349053| -0.924184; 0.594827; 0.375654
10| 0.645246| 1.401399| -0.924184; 0.560211; -0.483162| 0.191014| 0.327869; -0.232312; 0.171891
20| 0.204064| 0.278902| 0.456374; -0.199733; 0.175305| 0.137268| 0.305147; -0.176543; 0.113955
30| 0.138819| 0.260681| 0.446976; -0.170765; 0.178138| 0.068357| 0.190585; -0.085946; 0.156996
40| 0.080051| 0.150913| 0.298847; -0.191764; 0.157576| 0.035078| 0.126714; -0.101254; 0.093645
50| 0.035843| 0.063690| 0.225336; -0.110068; 0.028259| 0.010864| 0.075131; -0.005082; 0.072068
