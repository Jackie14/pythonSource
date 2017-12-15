#!/usr/bin/python
import os
import sys
import time

def _timeStr2Second(timeStr):
    """
    Convert the time string to seconds
    It may raise some exception when encounter parsing error
    """
    if len(timeStr) == 4 :
        formatStr = "%Y"
    elif len(timeStr) == 6 :
        formatStr = "%Y%m"
    elif len(timeStr) == 8 :
        formatStr = "%Y%m%d"
    elif len(timeStr) == 10 :
        formatStr = "%Y%m%d%H"
    elif len(timeStr) == 12 :
        formatStr = "%Y%m%d%H%M"
    elif len(timeStr) == 14 :
        formatStr = "%Y%m%d%H%M%S"
    else :
        raise Exception("Time string is incorrect")

    return time.mktime(time.strptime(timeStr, formatStr))

def _cleanOlderImpl(pathStr, modifyTimeSecond, deleteEmptyDir) :
    """
    Delete files which is not modified after timeSecond
    """
    if not os.path.exists(pathStr) :
        raise Exception("Do not exists: " + pathStr)

    if os.path.isdir(pathStr) :
        # Clean file/dir in this directory
        fileList = os.listdir(pathStr)
        oriDir = os.getcwd()
        os.chdir(pathStr)
        for f in fileList :
            _cleanOlderImpl(f, modifyTimeSecond, deleteEmptyDir)
        os.chdir(oriDir)

        # Delete current directory, if it's empty
        if deleteEmptyDir :
            fileList = os.listdir(pathStr)
            if len(fileList) == 0 :
                try :
                    os.rmdir(pathStr)
                    print("Delete dir %s, since it's empty now"%(pathStr))
                except Exception as e :
                    print (e)

    else :
        # Delete older file
        modifyTime = os.stat(pathStr).st_mtime
        if  modifyTime < modifyTimeSecond :
            try :
                os.remove(pathStr)
                print("Delete file %s since it's not modified after %s"%(pathStr, time.asctime(time.gmtime(modifyTimeSecond))))
            except Exception as e :
                print (e)
    
def cleanOlder(pathStr, latestModifyTime, deleteEmptyDir=False) :
    """
    Remove those older files within specified path, which is not modified after lastestModifyTime 
    pathStr: directory or file path string
    latestModifyTime: it can be time string, like: "1999" "199901" "19990101" "19990101010101"
                      it can also be time seconds from Epoch time
    deleteEmptyDir: whether delete those empty directories
    """
    try :
        if isinstance(latestModifyTime, str) :
            modifyTimeSecond = _timeStr2Second(latestModifyTime)
        else : # Supposing it's integer of time seconds from Epoch time
            modifyTimeSecond = latestModifyTime

        _cleanOlderImpl(pathStr, modifyTimeSecond, deleteEmptyDir)
    except Exception as e:
        print(e)
        
if __name__ == "__main__" :
    # Mock arguments
    # sys.argv =[sys.argv[0], "testDir", "2018"]
    
    if len(sys.argv) < 3 :
        print("Error!!!")  
        print("Sytax: fileOper.py <path> <time> [delete Empty Dir]")        
    else :
        deleteEmptyDir = False
        if len(sys.argv) > 3 and sys.argv[3][0] == '1' :
            deleteEmptyDir = True
        cleanOlder(sys.argv[1], sys.argv[2], deleteEmptyDir)
