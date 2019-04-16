from core.Executor import Executor
from core.ConfigParser import *
from core.EasyJmeterException import *
from core.SlaveController import *
from core.util import *
from core.models import Script,Master
import json,threading,traceback,logging,sys,os

logger = logging.getLogger('easyjmeter.core.MasterController')

# get result Task
class TaskResultThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self,name,stdoutThread,taskStderrThread,masterController):
        threading.Thread.__init__(self)
        self.name = name
        self.stdoutThread = stdoutThread
        self.taskStderrThread = taskStderrThread
        self.masterController = masterController

    def run(self):
        try:                #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
            self.stdoutThread.join()
            self.taskStderrThread.join()
            if self.masterController.status == 'FINISH':
                linuxSeperator = ConfigParser.get_config('seperator','linuxSeperator')
                remoteFile = self.masterController.remoteDir+linuxSeperator+'result.tar'
                localFile = self.masterController.instanceRandomName+'.tar'
                tarCmd = 'tar -cPvf '+remoteFile+' -C '+self.masterController.remoteDir+linuxSeperator+' result'
                _,execResult = self.masterController.masterExecutor.execShortTermCmd(tarCmd)
                if not execResult:
                    raise EasyJmeterException('Fail to compress the result file')
                self.masterController.masterExecutor.downloadFile(remoteFile,self.masterController.localResultPath+localFile)
                self.masterController.master.status = 'STOP'
                self.masterController.master.resultMsg = ''
                self.masterController.master.save()
                if self.masterController.masterExecutor is not None:
                    self.masterController.cleanTempFile()
                    self.masterController.masterExecutor.close_connection()
        except Exception:
            errorMsg = 'Fail to get the result,reason:'+traceback.format_exc()
            logger.error(errorMsg)
            self.masterController.master.status = 'STOP'
            self.masterController.master.resultMsg = errorMsg
            self.masterController.master.save()
            self.masterController.cleanTempFile()



#stdout Thread
class StdoutThread (threading.Thread):   #继承父类threading.Thread
    
    def __init__(self,name,std_stream,clientTerminal):
        threading.Thread.__init__(self)
        self.name = name
        self.std_stream = std_stream
        self.clientTerminal = clientTerminal

    def run(self):                #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        text_line = self.std_stream.readline()
        while text_line:
            text_line = self.std_stream.readline()
            if text_line != '':
                self.clientTerminal.send(text_data=json.dumps({
                    'message': "stdout:"+text_line
                }))

#stderr Thread
class TaskStderrThread (threading.Thread):   #继承父类threading.Thread
    
    def __init__(self,name,std_stream,masterController):
        threading.Thread.__init__(self)
        self.name = name
        self.std_stream = std_stream
        self.masterController = masterController

    def run(self):                #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        textLine = self.std_stream.readline()
        self.masterController.master.resultMsg = textLine
        execResult = True
        while textLine:
            if execResult:
                execResult = False
            self.masterController.clientTerminal.send(text_data=json.dumps({
                'message': "stderr:"+textLine
            }))
            textLine = self.std_stream.readline()
            self.masterController.master.resultMsg += textLine
        if execResult:
            if self.masterController.status == 'None':   
                self.masterController.status = 'FINISH'
                self.masterController.clientTerminal.send(text_data=json.dumps({
                        'message': "Task execute success"
                    }))
            self.masterController.master.status = "STOP"
            self.masterController.master.resultMsg = ''
            self.masterController.master.save()
        else:
            self.masterController.clientTerminal.send(text_data=json.dumps({
                        'message': "Task execute fail"
                    }))
            self.masterController.master.status = "STOP"
            self.masterController.master.save()
            




# Master Controller
class MasterController:


    def __init__(self,master,scriptCode,slaveList,clientTerminal):
        self.master = master
        self.scriptCode = scriptCode
        self.slaveList = slaveList
        self.clientTerminal = clientTerminal
        self.status = 'None'



    # create ssh connection between server to master and slave
    def initialize(self):
        try:
            #update master status
            # self.master.status = 'INIT'
            # self.master.save()
            #create remoteDir and remoteFile
            self.masterExecutor = Executor(self.master.ip,self.master.port,self.master.userName,self.master.password,self)
            self.slaveControllers = []
            if len(self.slaveList) > 0:
                for slave in self.slaveList:
                    slaveController = SlaveController(slave,self.clientTerminal)
                    slaveController.initialize()
                    self.slaveControllers.append(slaveController)
            else:
                raise EasyJmeterException("No slave in cluster")
            # get template instance by template_instance_code
            script = Script.objects.get(code=self.scriptCode)
            self.instanceRandomName = self.scriptCode+'_'+str(getTimestampe())
            #连接到Master上面，在指定目录下创建文件夹
            winSeperator = ConfigParser.get_config('seperator','winSeperator')
            linuxSeperator = ConfigParser.get_config('seperator','linuxSeperator')
            localTempFilePath = ConfigParser.get_config('local_temp_file','localTempFilePath')
            jmeterTempPath = ConfigParser.get_config('jmeter_temp_path','jmeterTempPath')
            instanceRandomFile = self.instanceRandomName+'.jmx'
            # Create localResultPath localTempFile remoteDir and remoteFile
            self.localResultPath = ConfigParser.get_config('local_result','localResultPath')
            self.localTempFile = localTempFilePath+winSeperator+instanceRandomFile
            self.remoteDir = jmeterTempPath+linuxSeperator+self.instanceRandomName
            self.remoteFile = self.remoteDir+linuxSeperator+instanceRandomFile
            if not os.path.exists(localTempFilePath):
                os.makedirs(localTempFilePath)
            if os.path.isfile(self.localTempFile):
                os.remove(self.localTempFile)
            localTempFileDescriptor = open(self.localTempFile,'w')
            writeFile(localTempFileDescriptor,script.content)
            execResult,_ = self.masterExecutor.execShortTermCmd("mkdir -p "+self.remoteDir)
            if not execResult:
                raise EasyJmeterException('Create dir on master fail')
            self.masterExecutor.uploadFile(self.localTempFile,self.remoteFile)
        except EasyJmeterException:
            self.master.status = 'STOP'
            self.master.resultMsg = traceback.format_exc()
            self.master.save()
            raise EasyJmeterException(traceback.format_exc())
        except Exception:
            errorMsg = "Initialize cluster fail,master ip:"+self.master.ip+" reason:"+traceback.format_exc()
            self.master.status = 'STOP'
            self.master.resultMsg = errorMsg
            self.master.save()
            self.cleanTempFile()
            logger.error(errorMsg) 
        


    # start jmeter task
    def startTask(self):
        try:
            slaveStr = ''
            for slave in self.slaveList:
                slaveStr+=slave.ip+","
            for slaveController  in self.slaveControllers:
                slaveController.startSlave()
            setenv_cmd = self.master.jmeterPath + '/bin/setenv.sh'
            linuxSeperator = ConfigParser.get_config('seperator','linuxSeperator')
            jmeter_cmd = '/usr/local/apache-jmeter-4.0/bin/jmeter -n -t '+self.remoteFile+' -R '+slaveStr[:-1]+' -l '+self.remoteFile+linuxSeperator+'Report.jtl -e -o '+self.remoteDir+linuxSeperator+'result'
            if not self.masterExecutor.execCmdMuteStdout(setenv_cmd):
                raise EasyJmeterException("Set env fail")
            stdout,stderr = self.masterExecutor.execLongTermCmd(jmeter_cmd)
            self.master.status = "RUNNING"
            self.master.resultMsg = ''
            self.master.save()
            stdoutThread = StdoutThread("TaskStdoutThread",stdout,self.clientTerminal)
            taskStderrThread = TaskStderrThread("TaskStderrThread",stderr,self)
            stdoutThread.start()
            taskStderrThread.start()
            taskResultThread = TaskResultThread("TaskResultThread",stdoutThread,taskStderrThread,self)
            taskResultThread.start()
        except EasyJmeterException:
            self.master.status = 'STOP'
            self.master.resultMsg = traceback.format_exc()
            self.master.save()
            raise EasyJmeterException(traceback.format_exc())
        except Exception:
            errorMsg = "Start task fail,master ip:"+self.master.ip+" reason:"+traceback.format_exc()
            self.cleanTempFile()
            for slaveController  in self.slaveControllers:
                slaveController.stopSlave()
            self.master.status = 'STOP'
            self.master.resultMsg = errorMsg
            self.master.save()
            logger.error(errorMsg) 
        


    #stop jmeter task
    def stopTask(self):
        try:
            if not self.instanceRandomName is None or self.instanceRandomName != '':
                masterPid = self.masterExecutor.execShortTermCmdAndGetResult('ps -ef | grep '+self.instanceRandomName+' | egrep -v grep | awk -F " " \'{print $2}\'')
                if masterPid is None or masterPid == '':
                    return
                self.status = 'STOP'
                stopMasterCmd = 'ps -ef | grep '+self.instanceRandomName+' | egrep -v grep | awk -F " " \'{print $2}\' | xargs kill -s 9'   
                execResult = self.masterExecutor.execCmdMuteStdout(stopMasterCmd)
                if execResult:
                    if hasattr(self,"masterExecutor") and self.masterExecutor is not None:  
                        self.master.status = 'STOP'
                        self.master.save()
                        self.cleanTempFile()
                        self.masterExecutor.closeConnection()
                        self.masterExecutor=None
                    for slaveController in self.slaveControllers:
                        slaveController.stopSlave()
                else:
                    raise EasyJmeterException('Stop the master fail')
        except EasyJmeterException:
            self.master.status = 'STOP'
            self.master.resultMsg = traceback.format_exc()
            self.master.save()
            raise EasyJmeterException(traceback.format_exc())
        except Exception:
            errorMsg = "Stop task fail,ip:"+self.master.ip+" reason:"+traceback.format_exc()
            self.cleanTempFile()
            self.master.status = 'STOP'
            self.master.resultMsg = errorMsg
            self.master.save()
            logger.error(errorMsg)   

    #clean the temp file
    def cleanTempFile(self):
        try:
            if os.path.isfile(self.localTempFile):
                os.remove(self.localTempFile)
            if hasattr(self,'remoteDir') and self.remoteDir != '':
                self.masterExecutor.execCmdMuteStdout('rm -rf '+self.remoteDir)
        except Exception:
            errorMsg = 'Clean temp file fail,reason:'+traceback.format_exc()
            logger.error(errorMsg) 
        

               


    
