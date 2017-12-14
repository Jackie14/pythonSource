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

def _cleanOlerdImpl(pathStr, timeSecond) :
    """
    Delete files which is not modified after timeSecond
    """
    if not os.path.exists(pathStr) :
        raise Exception("Do not exists: " + pathStr)

    if os.path.isdir(pathStr) :
        fileList = os.listdir(pathStr)
        oriDir = os.getcwd()
        os.chdir(pathStr)
        for f in fileList :
            _cleanOlerdImpl(f, timeSecond)
        os.chdir(oriDir)

        fileList = os.listdir(pathStr)
        if len(fileList) == 0 :
            try :
                os.rmdir(pathStr)
                print("Delete dir %s, since it's empty now"%(pathStr))
            except Exception as e :
                print (e)

    else :
        mTime = os.stat(pathStr).st_mtime
        if mTime < timeSecond :
            try :
                os.remove(pathStr)
                print("Delete file %s since it's not modified after %s"%(pathStr, time.asctime(time.gmtime(timeSecond))))
            except Exception as e :
                print (e)
    
def cleanOlder(pathStr, timeStr) :
    """
    Remove those old files, which is not modified after timeStr
    pathStr: directory or file path string
    timeStr: time string. "1999" "199901" "19990101" "19990101010101"
    """
    try :
        modifyTimeSecond = _timeStr2Second(timeStr);
        _cleanOlerdImpl(pathStr, modifyTimeSecond)
    except Exception as e:
        print(e)
        
if __name__ == "__main__" :
    # Mock arguments
    # sys.argv =[sys.argv[0], "testDir", "2018"]
    
    if len(sys.argv) != 3 :
        print("Error!!!")  
        print("Sytax: fileOper.py <path> <time>")        
    else :
        cleanOlder(sys.argv[1], sys.argv[2])

    # Just do want to keep the window stay
    input()
