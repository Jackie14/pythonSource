#!/usr/bin/python
# Reverse the provided string.
# If user provide a string "abc"
# the method reverseString will return a reversed string "cba"

import sys

def reverseString(orgStr = ""):
    if len(orgStr) < 1:
        return ""
    reversedStr = ""
    for c in range(len(orgStr) - 1,  -1, -1):
        reversedStr += orgStr[c]
    return reversedStr 

if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print("Please specific a string")
        exit(1) 

    print(reverseString(sys.argv[1]))

