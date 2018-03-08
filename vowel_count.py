#!/usr/bin/python
#
# Count the vowel of a input string
# output a dict like {"A": 34, "E": 323, "I": 32, "O":43, "U":323}
#

import sys

vowleSet = {'a', 'e', 'i', 'o', 'u'}

def charCount(text):
    countDict = {}
    for i in range(len(text)):
        if text[i] in countDict:
            countDict[text[i]] += 1
        else:
            countDict[text[i]] = 1

    return countDict

def vowleCount(text):
    charDict = charCount(text)
    vowleDict = {}
    for k, v in charDict.items():
        lowerK = k.lower()
        if lowerK in vowleSet:
            if lowerK in vowleDict: 
                vowleDict[lowerK] += v
            else:
                vowleDict[lowerK] = v

    return vowleDict

if __name__ == "__main__":
    print(vowleCount(sys.argv[1]))
