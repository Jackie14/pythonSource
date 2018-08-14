#!/usr/bin/env python
"""
Get URL category from Websense server
Two methods to use:
1) Execute the file directly.
    wse_client.py <url> [<parseCategoryName> [<wseAddr>, <wsePort>, <clientIp>]]
    Example: 
        wse_client.py yahoo.com

2) Import it as a module

    import wse_client

    wseClient = wse_client.wse_client()
    print(wseClient.getCategory("yahoo.com"))
    ...
    print(wseClient.getCategoryNumName("goolge.com"))

***OUTPUT****
Return positive number as the category number
Return negative number, when failed.
        -1: geneneral erro
        -2: network time out
        -3: invalid URL

"""



import sys
import struct
import socket
import urllib.request

class wse_protocol:
    """
    struct WS_MESSAGE_HEADER
    {
        uint16 length;
        uint16 version;
        uint16 messageType;
        uint16 bitMap;
        uint32 messageId;
    };
    """    
    HEADER_FORMAT = '!HHHHI'
    HEADER_LEN = 12

    """
    struct WS_URL_LOOKUP_REQUEST_EX
    {
        // WS_MESSAGE_HEADER header;
        uint16 serviceType;
        uint16 reserved;
        uint32 sourceAddress;
        uint32 destAddress;
        /* uint16 fullUrlLength;
        *  char fullUrl [fullUrlLength];
        *  uint16 userNameLength;
        *  char userName [userNameLength];
        */
    };
     """
    REQ_BODY_FORMAT = '!HHII'
    REQ_BODY_LEN = 12

    """
    struct WS_URL_LOOKUP_RESPONSE_EX
    {
        // WS_MESSAGE_HEADER header;
        uint16 lookupStatusCode;
        uint16 lookupDescriptionCode;
        uint16 categoryNumber;
        /* uint16 blockMessageLength;
        *  char blockMessage [blockMessageLength];
        *  uint16 keyWordLength;
        *  char keyWord [keyWordLength];
        */		
    };	
    """
    RESP_BODY_FORMAT = '!HHH'
    RESP_BODY_LEN = 6

    WS_PROT_HTTP = 0x0001
    WS_API_VERSION = 0x0420
    WS_URL_LOOKUP_AND_LOG_FOR_CACHE_ID_EX = 0x008B

    WS_URL_OK = 0x0000
    WS_URL_BLOCKED = 0x0001

    @classmethod
    def _composeHeader(cls, len, id):
        return struct.pack(cls.HEADER_FORMAT, len, cls.WS_API_VERSION, cls.WS_URL_LOOKUP_AND_LOG_FOR_CACHE_ID_EX, 0, id)

    @classmethod
    def _parseHeader(cls, headerBytes):
        return struct.unpack(cls.HEADER_FORMAT, headerBytes)

    @classmethod
    def _composeReqBody(cls, srcAddr, url):
        # The websense protocol needs URL having protocl string
        # We here use http:// as default protocl
        protPos = url.find("://")
        if protPos < 0 :
            url = "http://" + url
        elif protPos == 0:
            url = "http" + url

        # Compose req body format
        fmt = (cls.REQ_BODY_FORMAT + 
                 'H' + str(len(url)) + 's' # urlLen + url
                 'H') # userLen + user. Currently it's empty

        # Get src addr Int
        srcAddrByte = socket.inet_aton(srcAddr)
        srcAddrInt = struct.unpack("!I", srcAddrByte)[0]

        return struct.pack(fmt, cls.WS_PROT_HTTP, 0, srcAddrInt, 0, len(url), url.encode(), 0)

    @classmethod
    def composeReqMsg(cls, srcAddr, url, reqId):
        body = cls._composeReqBody(srcAddr, url)
        msgLen = cls.HEADER_LEN + len(body)
        header = cls._composeHeader(msgLen, reqId)
        return header + body

    @classmethod
    def parseRespBody(cls, respBodyPrefix):
        return struct.unpack(cls.RESP_BODY_FORMAT, respBodyPrefix)


class wse_request:
    def __init__(self, srcAddr, url, reqId):
        self.srcAddr = srcAddr
        self.url = url
        self.reqId = reqId

    def buildRequest(self):
        return wse_protocol.composeReqMsg(self.srcAddr, self.url, self.reqId)


class wse_response:
    def __init__(self, resp):
        self.resp = resp
        self.categoryNum = -1
        self.categoryName = ""
        self.isParseCategoryName = False
        self.isParsed = False

    def setParseCategoryName(self, isParse):
        self.isParseCategoryName = isParse

    def _parseCategoryName(self):
        # Try get the category name
        # 1) Only when URL was blocked, we can get the block page, 
        #    and through block page, we get category name
        # 2) Do not set websense policy to "block-all", it will only
        #    respond with "Your access to all sites is currently blocked" without category name
        # 3) The category name is in the block page's sub-iframe page, 
        #   whose link is http://10.103.228.18:15871/cgi-bin/block_message.cgi?ws-session=2063602609
        #   We get that link by blockpage's link http://10.103.228.18:15871/cgi-bin/blockpage.cgi?ws-session=2063602609

        # Get length of block page
        bodyMsgIdx = wse_protocol.HEADER_LEN + wse_protocol.RESP_BODY_LEN
        blockPageLen = struct.unpack('!H', self.resp[bodyMsgIdx : bodyMsgIdx + 2])[0]

        # Get the block page
        blockPage = struct.unpack(str(blockPageLen) + 's', self.resp[(bodyMsgIdx + 2) : (bodyMsgIdx + 2 + blockPageLen)])[0]
        blockPage = str(blockPage)

        # Get the redirect link from block page
        linkStart = blockPage.find("Location: ")
        if linkStart < 0 :
            return
        linkStart += len("Location: ")
        linkEnd = blockPage.find("\\r\\n", linkStart)
        if linkEnd < 0:
            linkEnd = blockPageLen
        link = blockPage[linkStart: linkEnd]

        # Get the message page link through block page link
        link = str(link)
        blockMsgLink = link.replace("blockpage.cgi", "block_message.cgi", 1)

        # Get the real block page through link
        resp = urllib.request.urlopen(blockMsgLink, timeout=20) # Use 20 second timeout
        blockMsg = str(resp.read())

        # Get the category name from block page
        categoryStart = blockMsg.find("This Websense category is filtered: ")
        if categoryStart < 0 :
            return
        categoryStart += len("This Websense category is filtered: ")
        categoryEnd = blockMsg.find(". ", categoryStart)
        if categoryEnd < 0 :
            categoryEnd = len(blockMsg)
        
        self.categoryName = blockMsg[categoryStart : categoryEnd]

    def _parseResp(self):
        # response message should not shorter than header len
        if len(self.resp) < wse_protocol.HEADER_LEN :
            return

        # Parse the header
        self.len, self.ver, self.type, self.bitMap, self.reqId = wse_protocol._parseHeader(self.resp[:wse_protocol.HEADER_LEN])

        # Currently, we only accept API_VERSION
        if self.ver != wse_protocol.WS_API_VERSION:
            return 

        # Parse the response body pre
        self.lookupStatusCode, self.lookupDesCode, self.categoryNum = \
            wse_protocol.parseRespBody(self.resp[wse_protocol.HEADER_LEN : wse_protocol.HEADER_LEN + wse_protocol.RESP_BODY_LEN])

        if self.lookupStatusCode == wse_protocol.WS_URL_OK:
            #print("!!!!!! The URL was allowed by Websense. desCode: "+ str(self.lookupDesCode) +" category number: " + str(self.categoryNum))

            # lookupDesCode == 1024. Allowed, for invalid URL, with fixed category number 146
            # lookupDesCode == 1025. Blocked, for policy, with correct category number
            # lookupDesCode == 1026. Allowed, for policy, with correct category
            if self.lookupDesCode == 1024:
                self.categoryNum = -3
            elif self.lookupDesCode == 1025:
                pass
            elif self.lookupDesCode == 1026:
                pass
            elif self.lookupDesCode == 1028:
                self.categoryNum = -3
            else:
                self.categoryNum = -3 

        self.parsedOK = True

        if self.isParseCategoryName and self.lookupStatusCode != wse_protocol.WS_URL_OK:
            self._parseCategoryName()

    class _decorators:
        @staticmethod
        def parse(func):
            def parseAndDo(self, *argv, **kwargv):
                if not self.isParsed:
                    self._parseResp()
                    self.isParsed = True
                return func(self, *argv, **kwargv)

            return parseAndDo

    @_decorators.parse
    def getCategory(self):
        return self.categoryNum

    @_decorators.parse
    def getCategoryName(self):
        return self.categoryName


class wse_client:
    def __init__(self, wseAddr = "10.103.228.18", wsePort = 15868, clientIp = "192.168.168.100"):
        self.wseAddr = wseAddr
        self.wsePort = wsePort
        self.clientIp = clientIp

    # OK. Return Positive number as the category number
    # Failed: Return negative number.
    #         -1: geneneral erro
    #         -2: network time out
    #         -3: invalid URL
    def _getCategoryImpl(self, url, parseCategoryName):
        so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        so.settimeout(5)
        serverAddr = (self.wseAddr, self.wsePort)
        so.sendto(wse_request(self.clientIp, url, 1).buildRequest(), serverAddr)

        try:
            respMsg = so.recv(2048)
        except:
            #print("Time out")
            return (-2, "")
        
        wse_resp = wse_response(respMsg)
        wse_resp.setParseCategoryName(parseCategoryName)

        return (wse_resp.getCategory(), wse_resp.getCategoryName())
    
    def getCategory(self, url):
        return self._getCategoryImpl(url, False)[0]

    def getCategoryNumName(self, url):
        return self._getCategoryImpl(url, True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide URL")
        sys.exit()
    
    url = sys.argv[1]

    parseCategoryName = False
    if len(sys.argv) >= 3 :
        if sys.argv[2] == "parseCategoryName" :
            parseCategoryName = True

    wseClient = wse_client()
    if len(sys.argv) >= 5:
        serverAddr = sys.argv[3]
        serverPort = int(sys.argv[4])
        clientIp = sys.argv[5]
        wseClient = wse_client(serverAddr, serverPort, clientIp)

    if parseCategoryName == False :
        print(wseClient.getCategory(url))
    else :
        print(wseClient.getCategoryNumName(url))
