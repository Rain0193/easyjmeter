import time
import random
import json
from django.http import HttpResponse

def getCode(prefix):
    return prefix+"-"+str(int(time.time()))+"-"+str(random.randint(1,10000))

def getSuccessHttpResponse(status,message):
    response_data = {}
    response_data["status"] = status
    response_data["message"] = message
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def getErrorHttpResponse():
    response_data = {}
    response_data["message"] = "出错啦!!!"
    return HttpResponse(json.dumps(response_data), content_type="application/json",status=500)

def isNone(object,logger,object_name,code):
    if object is None:
            logger.error(object_name+'不存在,code:'+code)
            return True
    else:
        return False

def getTimestampe():
    t = time.time()
    return (int(round(t * 1000)))

def writeFile(file,content):
    try:
        file.write(content)
    except Exception as e:
        print(format(e))
    finally:
        file.close()

def getWrapperCmd(cmd,real_cmd,process_id):
    return cmd + ' ' + real_cmd + ' ' + process_id