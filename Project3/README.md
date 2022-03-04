# Knapsack problem - Evolutionary Algorithm
Imagine a knapsack with several objects to add that are all worth different amounts of money. When leaving the site, you may only carry a certain amount of weight, and you want the highest value possible. A high value, low weight object would be ideal, and a low value, high weight object should be left unless capacity remains and no better objects exist.

Objects are represented as bits or a bitstring as in project 2, but now must be represented with two numbers instead of one (weight and value).

Selection, crossover, and mutation are not particularly different from previous projects. The fitness, however, is replaced by the value of each object. Solutions that go over capacity are penalized so they are less likely to show up in later generations. However, some elements of that poor solution may still be part of the best one, so allowing a chance for them to remain and get crossed into another solution allows those objects another chance.

## From project report for class
**Penalty**
For the penalty, I used a static, deviation-dependent approach. To get the base value of how extreme the penalty is, I subtracted the capacity of the knapsack from the total weight value of the bitstring. I allowed a constant to be passed in to multiply that value, but by default I multiply it by the size of the knapsack divided by 4. The result is multiplying the penalty by 5. In hindsight, it may have been better to also connect the constant to the capacity. Overtaking the capacity by 5 points seems more meaningful if your capacity is 20 instead of 200. The size of the knapsack seemed a worthwhile addition though, as a greater size means more variety in how you can overtake the capacity.

**Weights**
I state how I handle weights and values in comments, but I believe it is worthwhile to mention here. I generate weights randomly with 2 separate values to help constrain them. The upper limit for any weight is the capacity divided by size and multiplied by 4. Each weight may be between 1 and that value. The sum of all such weights will be between the size and 4 times the capacity, so on average they will sum to twice the capacity. Given that, on average half of the weights will sum to the capacity, allowing the greater variation in possible solutions; choosing 10 of 20 elements will allow more possible solutions than 11 of 20, or 15 of 20.

After generating the weights, I compare their sum to the value of twice the capacity. If they are more than 1 off, I increment or decrement random weights until that changes. If incrementing, I do not allow any weights to go above the initial individual limit. If decrementing, I do not allow any weights to go below 1. Weights are randomized while still forcing a great deal of choice without restricting best solutions to exactly half of the elements.

Trivial weights are initialized either to 1 or to the capacity multiplied with some constant over 1.

**Values**
Values are randomized in the normal cases, where weights are not trivial. They may be initialized anywhere from 1 to the size of the knapsack. Theoretically, this allows every element to have a different value. Practically, there will be some repetition, but it avoids constant repetition and keeps lower values more viable for the solution.

**Trivial Cases**
I noticed that in trivial cases, the best runs often did not get close to the best solution. Even the best solutions were 2 to 4 bits away. I believe that comes from selection and crossover leading to common bitstrings that may not have 1s or 0s in places to fill in the last slots. Mutation is not reliable in finishing the remaining spots on its own. My impression is that EAs are best when the best solution in a bit string is not all or nothing. As long as some variation in the best solution exists, it seems more likely that the process will find the pieces it needs. But that impression is still just an impression and not nearly fully tested.

### Output
Instance 1
  Weights: [6, 6, 10, 10, 10, 3, 10, 7, 1, 1, 1, 3, 1, 8, 9, 8, 11, 1, 6, 9]
  Values: [4, 10, 15, 20, 5, 11, 1, 5, 5, 9, 5, 18, 16, 19, 10, 7, 3, 3, 1, 1]
  Capacity: 60
  Average of Best Runs: 113.1

Instance 2
  Weights: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  Values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  Capacity: 60
  Average of Best Runs: 82.1

Instance 3
  Weights: [6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000]
  Values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  Capacity: 60
  Average of Best Runs: 28.1
