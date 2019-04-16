import json
from urllib import request, parse
from core.EasyJmeterException import *


class JmxMaker:

    def createSimpleJmeterScript(self,requestDict):
        headers = {
            'content-type' : r'application/json'
        }
        data = json.dumps(requestDict) 
        data = bytes(data, 'utf8')
        url = r'http://127.0.0.1:8080/simpleJmeterScript'
        req = request.Request(url,headers=headers,data=data)
        resData = request.urlopen(req).read()
        scriptContent = resData.decode('utf-8')
        if scriptContent == 'FAIL':
            raise EasyJmeterException('Generate script jmx fail')
        return scriptContent