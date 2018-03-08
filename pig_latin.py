#!/usr/bin/python
# The pig latin game.
# Move the first consonant char of a word, to the end, and tailing that word with "ay"
# Example: provided word "banana", and we will returen "anana-bay"

import sys

def pigLatin(word):
    charList = list(word)
    vowelSet = {'a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U'}
    firstConso = '*'
    for i in range(len(charList)):
        if not charList[i] in vowelSet:
            firstConso = charList.pop(i)
            break;

    charList.append("-" + firstConso + "ay")
    return "".join(charList)
            


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print("Please provoid a string")
        exit(1)
    
    print(pigLatin(sys.argv[1]))
