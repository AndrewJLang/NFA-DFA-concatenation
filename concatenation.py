import sys

#Andrew Lang and Alex Weininger

#Check that the command line arguments are correct
def properInput():
    A_file, B_file = 0, 0
    #Need 3 additional command line arguments (2 inputs and one write file)
    if len(sys.argv) != 4:
        print("Improper amount of arguments, program terminating")
        sys.exit()
    #check file extension
    if sys.argv[1].endswith('.txt') == False or sys.argv[2].endswith('.txt')==False or (sys.argv[3].endswith('.txt')==False):
        print("Not proper file extension, make sure to include .txt")
        sys.exit()
    #see if the two input files exist
    try:
        A_file = open(sys.argv[1], "r")
        B_file = open(sys.argv[2], "r")
    except FileNotFoundError:
        print("Input file does not exist, program terminating")
        sys.exit()
    concatFile = sys.argv[3]
    #return all the information if it is proper format
    return A_file, B_file, concatFile
    
#check input file contents to see if correct
def checkFileInfo(description):
    #Need 5 elements for correct formal description
    if len(description) != 5:
        print("Improper amount of information in file")
        return False
    #Check how many arguments are in alphabet, only accepts integer transitions (not a and b)
    try:
        alphabetElements = list(map(int, description[1].split()))
    except ValueError:
        print("Alphabet contains characters")
        return False

    #check if value is [0,1,-1], if not, it is not proper alphabet
    for x in alphabetElements:
        if x != 1 and x != 0 and x != -1:
            print("Wrong number value, only [1,0,-1] accepted as alphabet elements")
            return False

    return True

#Transform the transitions so overlapping states between A and B are labeled accordingly
def checkTransitions(stateList, transitionList, alphabetList):
    splitTransitions = []
    #Format transitions so they can be checked
    for x in range(len(transitionList)):
            splitTransitions.append(transitionList[x].split(sep=" "))
            try:
                splitTransitions[len(splitTransitions)-1].remove('')
            except ValueError:
                continue
    
    #Check that the transitions are proper
    for x in range(len(splitTransitions)):
        if len(splitTransitions[x]) != 3:
            return False
        #Ensure that the first two elements are states in the state list, and the transition value is in the alphabet
        if splitTransitions[x][0] not in stateList or splitTransitions[x][1] not in stateList or splitTransitions[x][2] not in alphabetList:
            return False
    return splitTransitions, True


A_file, B_file, concatFile = properInput()

#Read in the file and split the information up to be in separate lists
def readFile(fileName):
    fileElements = fileName.readlines()
    formalDescription = [x.strip() for x in fileElements]
    # print(formalDescription)

    #error check the file to make sure it is a proper DFA/NFA
    if checkFileInfo(formalDescription) == False:
        print("File errors, program terminating")
        A_file.close()
        B_file.close()
        sys.exit()
    
    #Separate each portion of the formal description
    listOfStates = formalDescription[0].split(sep=" ")
    alphabet = formalDescription[1].split(sep=" ")
    transitions = formalDescription[2].split(sep=",")
    startState = formalDescription[3].split(sep=" ")
    
    updatedTransitions, tempCheck = checkTransitions(listOfStates, transitions, alphabet)
    if tempCheck == False:
        print("Improper element in transition, program terminating")
        A_file.close()
        B_file.close()
        sys.exit()

    #check if there is more than 1 initial state, exit if so
    if len(startState) != 1:
        print("More than one start state in the file, program terminating")
        A_file.close()
        B_file.close()
        sys.exit()
    
    acceptStates = formalDescription[4].split(sep=" ")

    return listOfStates, alphabet, transitions, startState, acceptStates, updatedTransitions

A_states, A_alphabet, A_transitions, A_startState, A_acceptStates, A_splitTransitions = readFile(A_file)
B_states, B_alphabet, B_transitions, B_startState, B_acceptStates, B_splitTransitions = readFile(B_file)

#Close the files once we have read all the information
A_file.close()
B_file.close()

#Define all our final output lists
concatStates, concatAlphabet, concatTransitions, concatStartState, concatAcceptStates = [], [], [], [], []

#fix duplicate named states from different files
def adjustStates(A_states, B_states):
    unionStates = A_states + B_states
    unionStates = list(dict.fromkeys(unionStates))

    if len(unionStates) == (len(A_states) + len(B_states)):
        return A_states, B_states
    else:
        for x in range(len(A_states)):
            A_states[x] = f'A_{A_states[x]}'
        for x in range(len(B_states)):
            B_states[x] = f'B_{B_states[x]}'
        return A_states, B_states

A_states, B_states = adjustStates(A_states, B_states)

#adjust transitions so they show proper states
def adjustTransitions(transitions, A_states):
    for x in range(len(transitions)):
        tempArr = transitions[x].split(sep=" ")
        if tempArr[0] == '':
            tempArr.pop(0)
        if A_states == True:
            tempArr[0] = f'A_{tempArr[0]}'
            tempArr[1] = f'A_{tempArr[1]}'
        else:
            tempArr[0] = f'B_{tempArr[0]}'
            tempArr[1] = f'B_{tempArr[1]}'
        transitions[x] = tempArr[0] + " " + tempArr[1] + " " + tempArr[2]
    return transitions

A_transitions = adjustTransitions(A_transitions, A_states=True)
B_transitions = adjustTransitions(B_transitions, A_states=False)

#join all the states
def concatAllStates(A_states, B_states):
    return A_states + B_states

#Union together the alphabets
def concatAlphabet(A_alph, B_alph):
    union_Alph = A_alph + B_alph + ['-1']
    return list(dict.fromkeys(union_Alph))

#Transitions between states for the concatenation
def newTransitions(A_transitions, B_transitions, A_acceptStates, B_startState):
    transitionTable = A_transitions + B_transitions
    for x in range(len(A_acceptStates)):
        transitionTable.append(f"A_{A_acceptStates[x]} B_{B_startState[0]} -1")
    return transitionTable

#Fix the accept states for the final concatenated language
def concatAcceptStates(A_acceptStates, B_acceptStates):
    return "B_" + B_acceptStates[0]

#Get the start state for the final language
def concatStartStates(A_startState, B_startState):
    return "A_" + A_startState[0]

concatStates = concatAllStates(A_states, B_states)
concatAlphabet = concatAlphabet(A_alphabet, B_alphabet)
concatTransitions = newTransitions(A_transitions, B_transitions, A_acceptStates, B_startState)
concatStartState = concatStartStates(A_startState, B_startState)
concatAcceptStates = concatAcceptStates(A_acceptStates, B_acceptStates)

#Write the new concatenation to an output terminal
def writeOutput(fileName):
    outputFile = open(fileName, "w")
    for x in range(len(concatStates)):
        outputFile.write(concatStates[x] + ' ')
    outputFile.write("\n")
    for x in range(len(concatAlphabet)):
        outputFile.write(concatAlphabet[x] + ' ')
    outputFile.write("\n")
    for x in range(len(concatTransitions)):
        outputFile.write(f"({concatTransitions[x].strip()}) ")
    outputFile.write("\n")
    outputFile.writelines(concatStartState)
    outputFile.write("\n")
    outputFile.writelines(concatAcceptStates)
    outputFile.close()

writeOutput(concatFile)