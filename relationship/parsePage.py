#! /usr/bin/env python
'''
Parse the baidu baike page, extract the description and page
'''

from bs4 import BeautifulSoup
import urllib.request
import sys

def parsePage(page):
    """
    Parse page return tuple (<descrition str>, <image tytes>)
    """
    soup = BeautifulSoup(page, 'html.parser')
    des = soup.find('meta', attrs={'name':'description'})
    des = des["content"]

    # Try to got ficture for that person
    gotPic = False
    headers = {'Referer': 'http://www.baidu.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"}
    if not gotPic:
        try: 
            picDir = soup.find('div', attrs={'class':"summary-pic"})
            pic = picDir.find('img')
            picLink = pic['src']
            httpPicLink = picLink.replace("https://", "http://")
            req = urllib.request.Request(httpPicLink, None, headers=headers)
            picResp = urllib.request.urlopen(req, timeout=10)
            gotPic = True
        except:
            print('Pic Format one: failed')

    if not gotPic:
        try: 
            picDir = soup.find('ul', attrs={'class':"lemmaWgt-secondsKnow-gallery"})
            pic = picDir.find('img')
            picLink = pic['src']
            httpPicLink = picLink.replace("https://", "http://")
            req = urllib.request.Request(httpPicLink, None, headers=headers)
            picResp = urllib.request.urlopen(req, timeout=10)
            gotPic = True
        except:
            print('Pic Format two: failed')

    if not gotPic:
        return (des, None)

    return (des, picResp.read())


if __name__ == "__main__" :
    if len(sys.argv) < 2:
        print("Please specify the page file path to page")
        sys.exit()

    with open(sys.argv[1], 'br') as f:
        print(parsePage(f))