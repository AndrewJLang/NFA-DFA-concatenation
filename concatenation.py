import numpy as np

A_file = open("001_start.txt", "r")
B_file = open("111_start.txt", "r")

#Need to error check the files in this method
# def checkErrors(description):


def readFile(fileName):
    fileElements = fileName.readlines()
    formalDescription = [x.strip() for x in fileElements]

    #call error checking method in this file

    #Separate each portion of the formal description
    listOfStates = formalDescription[0].split(sep=" ")
    alphabet = formalDescription[1].split(sep=" ")
    transitions = formalDescription[2].split(sep=",")
    startState = formalDescription[3].split(sep=" ")
    acceptStates = formalDescription[4].split(sep=" ")

    return listOfStates, alphabet, transitions, startState, acceptStates

A_states, A_alphabet, A_transitions, A_startState, A_acceptStates = readFile(A_file)
B_states, B_alphabet, B_transitions, B_startState, B_acceptStates = readFile(B_file)

#Close the files once we have read all the information
A_file.close()
B_file.close()

#Define all our final output lists
concatStates, concatAlphabet, concatTransitions, concatStartState, concatAcceptStates = [], [], [], [], []

#fix duplicate named states
def adjustStates(A_states, B_states):
    unionStates = A_states + B_states
    unionStates = list(dict.fromkeys(unionStates))
    changed = False

    if len(unionStates) == (len(A_states) + len(B_states)):
        return A_states, B_states, changed
    else:
        changed = True
        for x in range(len(A_states)):
            A_states[x] = f'A_{A_states[x]}'
        for x in range(len(B_states)):
            B_states[x] = f'B_{B_states[x]}'
        return A_states, B_states, changed

A_states, B_states, _ = adjustStates(A_states, B_states)

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
        transitionTable.append(f"{A_acceptStates[x]} {B_startState[0]} -1")
    return transitionTable

#Fix the accept states for the final concatenated language
def concatAcceptStates(A_acceptStates, B_acceptStates):
    return B_acceptStates

#Get the start state for the final language
def concatStartStates(A_startState, B_startState):
    return A_startState

concatStates = concatAllStates(A_states, B_states)
concatAlphabet = concatAlphabet(A_alphabet, B_alphabet)
concatTransitions = newTransitions(A_transitions, B_transitions, A_acceptStates, B_startState)
concatStartState = concatStartStates(A_startState, B_startState)
concatAcceptStates = concatAcceptStates(A_acceptStates, B_acceptStates)

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

writeOutput("testOutput.txt")