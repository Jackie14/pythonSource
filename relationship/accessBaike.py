#! /usr/bin/env python
'''
Access baidu baike to get the description and pic one persson by providing the person's name
'''

import sys
import urllib.request
import parsePage
import datetime
import time

def getPersonDes(personName):
    url = "https://baike.baidu.com/item/" + urllib.request.quote(personName)
    headers = {'Referer': 'http://www.baidu.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"}
    req = urllib.request.Request(url, None, headers)
    resp = urllib.request.urlopen(req, timeout = 30)

    # We do not need to download the whole page，useing resp.read(), it may take long time
    bytesBuf = bytearray(1024 * 40)
    resp.readinto(bytesBuf)

    with open(personName + ".html", 'bw') as f:
        f.write(bytesBuf)

    des = parsePage.parsePage(bytesBuf)


    with open(personName + ".dec.txt", 'w') as f:
        f.write(des[0])

    if des[1] != None:
        with open(personName + ".jpg", 'bw') as f:
            f.write(des[1])

    return bytesBuf, des[0], des[1]
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify the name")
        sys.exit()
    startTime = time.time()
    name = sys.argv[1]
    getPersonDes(name)
    print("Take %f"%(time.time() - startTime))