# Concatenation of two NFA/DFA's

 - This program was written and run on python 3.7
 - The program takes 4 arguments, the python file name, the first NFA/DFA (A), the second NFA/DFA (B), and then the output file which the concatenation will be written to
 
## Functions
 - properInput
    - Check that there are proper amount of arguments read in from command line
 - checkFileInfo
    - Check that information within read in files is correct/properly formatted
 - checkTransitions
    - Make sure the transitions are labeled such that it goes (state state alphabet_symbol)
 - readFile
    - Read the information from the formal description into split up lists if all previous checks have passed
 - adjustStates
    - If states share the same name between A and B, adjust all of them and label with A and B
 - adjustTransitions
    - Same changes as adjustStates, just done within the transitions
 - concatAllStates
    - Create the concatenated state list
 - concatAlphabet
    - Create the concatenated alphabet, include -1 for empty transition
 - newTransitions
    - Generate the new transitions that are necessary when concatenating A and B (final states of A to start state of B)
 - concatAcceptStates
    - return the accept states of B
 - concatStartStates
    - return the start state of A
 - writeOutput
    - Write the new concatenation NFA to a file specified by the command line arguments and put all the new information into this file in formal description form