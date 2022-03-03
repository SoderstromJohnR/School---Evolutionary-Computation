import argparse, sys, getopt


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

argList = sys.argv[1:]

manInput = False
fileName = None
try:
    if len(argList) is 0:
        manInput = True
    elif len(argList) is 2:
        options = "hfs:"
        args, values = getopt.getopt(argList, options)
        for curArg, curVal in args:
            if curArg in ('-f'):
                fileName = argList[-1]
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

if fileName:
    try:
        file = open(fileName, "r")
        boolCheck = [False] * 10
        readLine = file.readlines()
        for li in readLine:
            tok = li.split()
            if tok[0] is "BitLength:":
                for i in range(len(tok) - 1):
                    xLen.append(int(tok[i + 1]))
                boolCheck[0] = True
            if tok[0] is "Min:":
                minX = float(tok[1])
                boolCheck[1] = True
            if tok[0] is "Max:":
                maxX = float(tok[1])
                boolCheck[2] = True
            if tok[0] is "Pop:":
                popSize = int(tok[1])
                boolCheck[3] = True
            if tok[0] is "Runs:":
                numRuns = int(tok[1])
                boolCheck[4] = True
            if tok[0] is "Gens:":
                numGens = int(tok[1])
                boolCheck[5] = True
            if tok[0] is "CrossPoint:":
                pointCross = int(tok[1])
                boolCheck[6] = True
            if tok[0] is "P_Cross:":
                probCross = float(tok[1])
                boolCheck[7] = True
            if tok[0] is "P_Mut:":
                probMut = float(tok[1])
                boolCheck[8] = True
            if tok[0] is "RandomSeed:":
                rSeed = int(tok[1])
                boolCheck[9] = True
            if tok[0] is "Selection:":
                selectionChoice = int(tok[1])
                if selectionChoice < 0 and selectionChoice > 2:
                    selectionChoice = 0
            if tok[0] is "MaxFitness:":
                if tok[1] is "f":
                    isMaxFitness = False
                else:
                    isMaxFitness = True

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
    while not (choice is "y" or choice is "n"):
        choice = input("Would you like to use default values? (y/n): ")

    # Accept default values used for the assignment
    if choice is "y":
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

    if maxX > minX:
        print("The maximum value given is below the minimum.")
        sys.exit()

    if numRuns < 1 or numGens < 1:
        print("The number of runs and generations must be a positive integer.")
        sys.exit()
