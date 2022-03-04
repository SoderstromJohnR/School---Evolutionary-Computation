# Jaya Algorithm
This algorithm changes the determination of the next generation from previous projects. The first generation is randomly determined as before.

First, the two extremes of a generation are found, best and worst. Then two random vectors are generated. At each vector of a generation, each element is altered based on the newly generated vectors and the extremes. The new element is clamped to the minimum or maximum as necessary. Finally, if the resulting vector is better than the original, we keep it. Otherwise we keep the original. This continues until all vectors have been altered and tested or kept as they were.

## From project report for class
### Partial Output
Run 1
{'Best Fitness': 2.865815883339255e-06,
 'Best Vector': [0.0015096449907122424,
                 0.00071776392702956,
                 -0.0002675870520256787]}

Run 2
{'Best Fitness': 6.300988454522829e-07,
 'Best Vector': [0.0005417544042070848,
                 0.0005792150626435319,
                 -3.3330499266573214e-05]}

Run 3
{'Best Fitness': 2.3644316085947458e-07,
 'Best Vector': [-0.0002766912056361571,
                 -0.00022134423880943571,
                 -0.00033300430256823395]}

Run 4
{'Best Fitness': 3.2947591043511283e-06,
 'Best Vector': [0.0015103611997561786,
                 0.0006170904578368834,
                 0.0007954668550410322]}

Run 5
{'Best Fitness': 3.6681109674501576e-07,
 'Best Vector': [0.00030443129168748924,
                 0.00026068437782872297,
                 -0.00045406644947909797]}

Run 6
{'Best Fitness': 7.889957254490673e-07,
 'Best Vector': [0.00041685853930329905,
                 -0.000515320484785214,
                 0.0005913285733158166]}
