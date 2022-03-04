# Evolutionary Algorithm
Not all problems have a sleek solution. In order to solve some of the harder problems, we find a way to calculate how effective a solution was, and then run multiple attempts that prune out the weaker solutions to find the best one we can. This method mimics evolution in a biological sense.

This project attempts to find a solution to an easy problem with this method. Given a range of values both negative and positive, we want to minimize the result of x^2 + y^2 + z^2. Obviously the best solution sets all three values to 0, but we cannot just do that this time.

We create several vectors of randomized values and then rate them. This problem provides an easy way to calculate the fitness - plug all three values into the above function. We prioritize the best vectors for selection, but we still allow some results from weaker solutions because parts of it might be better. After calculating the vectors for the next iteration (generation), we run it again and repeat.



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

**Best-of-Runs,**
:-----:
Average Fitness, 0.26203359103355445
Standard Deviation, 2.049849182629643
