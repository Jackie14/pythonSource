#! /usr/bin/env python
'''
Access baidu baike to get the description and pic one persson by providing the person's name
'''

import sys
import urllib.request
import parsePage

def getPersonDes(personName):
    url = "http://baike.baidu.com/item/" + urllib.request.quote(personName)
    print(url)
    req = urllib.request.Request(url, None, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"})
    resp = urllib.request.urlopen(req, timeout = 10)

    pageByte = resp.read()
    with open(personName + ".html", 'bw') as f:
        f.write(pageByte)

    des = parsePage.parsePage(pageByte)

    with open(personName + ".dec.txt", 'w') as f:
        f.write(des[0])

    if des[1] != None:
        with open(personName + ".jpg", 'bw') as f:
            f.write(des[1])

    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify the name")
        sys.exit()
    
    name = sys.argv[1]
    getPersonDes(name)