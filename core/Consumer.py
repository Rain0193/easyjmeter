# chat/TaskConsumer.py
from channels.generic.websocket import WebsocketConsumer
from core.MasterController import *
from core.models import Master,Slave
import json,paramiko,threading,sys,os,time
import logging
import traceback

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)

logger = logging.getLogger('easyjmeter.core.TaskConsumer')
         

class TaskConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print("websocket 连接已关闭")
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        scriptCode = 'script-1554654435-6003'
        clusterCode = text_data_json['clusterCode']
        
        try:
            if message.strip() == 'start':
                if not hasattr(self,"status"):
                    self.status = True
                    master = Master.objects.filter(status="STOP",clusterCode=clusterCode)
                    if len(master) <= 0:
                        self.send(text_data=json.dumps({
                            'message': "当前没有空闲的Master主机,请稍后再试"
                        }))
                        self.close()
                    #从templateInstance中将jmx内容读出来,并上传到目录下
                    slaveList = Slave.objects.filter(clusterCode=clusterCode)
                    self.masterController = MasterController(master[0],scriptCode,slaveList,self)
                    self.send(text_data=json.dumps({
                        'message': "Initialize the cluster"
                    }))
                    self.masterController.initialize()
                    self.send(text_data=json.dumps({
                        'message': "Start the task"
                    }))
                    self.masterController.startTask()
                else:
                    self.send(text_data=json.dumps({
                        'message': "The task is already running,please retry later"
                    }))
                    self.close()   
            elif message.strip() == 'stop':
                self.send(text_data=json.dumps({
                    'message': "Stop the task"
                }))
                self.masterController.stopTask()
                self.close()   
            else:
                self.send(text_data=json.dumps({
                        'message': "Please enter the valid command"
                    }))
        except EasyJmeterException:
            logger.error(traceback.format_exc())
            self.send(text_data=json.dumps({
                'message': "Ops!! something wrong,the reason maybe:"+traceback.format_exc()
            })) 
        except Exception:
            logger.error(traceback.format_exc())

    
    



            
            
        
            
        
        




        
        





