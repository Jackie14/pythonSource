#!/usr/bin/env python
"""
    This script is used to parse the log in CFS sever

    Example:

    import cfsServerLogParser

    missLogData = cfsServerLogParser.parseRatingMissLogFile("logfile")
    print("Missing log file: " + missLogData["file"])
    print("Missing log line count: " + str(missLogData["lineCount"]))
    print("Missing log err line count: " + str(missLogData["errLineCount"]))
    print("Missing log OK line count: " + str(missLogData["okLineCount"]))
    
    for e in missLogData["logList"]:
        print("domain: " + e["domain"])
        print("path: " + e["path"])


"""

import sys

def parseRatingMissLogLine(logLine, printError = False):
    """
    Parse a rating missing log line: 
    Following is example of content of rating missing log:
    Sep 10 02:24:48 sjl0vm-cfs401 webcfsd: dk3.lunrac.com /api/test UNRATED
    0    1     2          3          4           5            6        7

    """
    entryMap = {}
    entryList = logLine.split(sep = None)

    # Verify the log format
    if len(entryList) < 6: #  webcfsd: <domain> is must
        if printError:
            print("Ignore log line with invalid format: " + logLine)
        return entryMap

    if entryList[4] != "webcfsd:":
        if printError:
            print("Ignore log line with invalid format: " + logLine)
        return entryMap

    # Record base info. "time", "server", "logType", "domain"
    entryMap["time"] = entryList[0] + " " + entryList[1] + " " + entryList[2]
    entryMap["server"] = entryList[3]
    entryMap["logType"] = entryList[4]
    entryMap["domain"] = entryList[5]

    # Handle the "path" case
    if len(entryList) > 6:
        entryMap["path"] = entryList[6]
    else :
        entryMap["path"] = ""
    if entryMap["path"] == "NULL":
        entryMap["path"] = ""
    
    # Handle the "msg" case
    if len(entryList) > 7:
        entryMap["msg"] = entryList[7]
    else:
        entryMap["msg"] = ""

    return entryMap

def parseRatingMissLogFile(logFile):
    """
    Parse Rating missing log file.
    The return is a map of file log info.
    {
        "file": <log file name>,
        "lineCount": <line count of file>,
        "errLineCount": <line count of error>,
        "okLineCount": <line count of ok>,
        "logList": <list of format log>
    }

    Each format log is a map of log line info
    {
        "time": "Sep 10 02:24:48", 
        "server": "sjl0vm-cfs401",
        "logType": "webcfsd", 
        "domain": "yahoo.com", 
        "path": "/news",
        "msg": "UNRATED"
    }


    """
    logData = {}
    lineCount = 0
    errLineCount = 0
    validLineCount = 0
    logList = []

    with open(logFile) as f:
        line = f.readline()
        while line:
            lineCount += 1
            logLineMap = parseRatingMissLogLine(line)
            if logLineMap.get("domain") != None:
                logList.append(logLineMap)
                validLineCount += 1
            else : 
                errLineCount += 1

            line = f.readline()

    logData["file"] = logFile
    logData["lineCount"] = lineCount
    logData["errLineCount"] = errLineCount
    logData["okLineCount"] = validLineCount
    logData["logList"] = logList

    return logData

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide log file path")
        sys.exit()

    missLogFile = sys.argv[1]
    missLogData = parseRatingMissLogFile(missLogFile)
    print("Missing log file: " + missLogData["file"])
    print("Missing log line count: " + str(missLogData["lineCount"]))
    print("Missing log err line count: " + str(missLogData["errLineCount"]))
    print("Missing log OK line count: " + str(missLogData["okLineCount"]))

    print("\nMising domain + path examples: \n\n")
    limit = 10
    for e in missLogData["logList"]:
        print(e["domain"] + e["path"])
        limit -= 1
        if limit < 0:
            break