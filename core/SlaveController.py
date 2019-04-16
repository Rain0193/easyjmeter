from core.Executor import Executor
from core.EasyJmeterException import *
import json,threading,traceback,logging


logger = logging.getLogger('easyjmeter.core.SlaveController')

# Slave Controller 
# Use to start and stop slave
class SlaveController:

    def __init__(self,slave,clientTerminal):
        self.slave = slave
        self.clientTerminal = clientTerminal


    # initialize slave
    def initialize(self):
        try:
            self.slaveExecutor = Executor(self.slave.ip,self.slave.port,self.slave.userName,self.slave.password,self.clientTerminal)
            self.slave.status = 'STOP'
            self.slave.resultMsg = ''
            self.slave.save()
            #first stop the slave
            self.clearSlaveProcess()
        except Exception:
            errorMsg = "Initialize slave failed,ip:"+self.slave.ip+" reason:"+traceback.format_exc()
            logger.error(errorMsg)

    #start slave
    def startSlave(self):
        try:
            #then start the slave
            setenv_cmd = self.slave.jmeterPath + '/bin/setenv.sh'
            jmeter_cmd = '/usr/local/apache-jmeter-4.0/bin/jmeter-server 1>&2 &'
            if not self.slaveExecutor.execShortTermCmd(setenv_cmd):
                raise EasyJmeterException('Set env fail')
            execResult = self.slaveExecutor.execCmdMuteStdout(jmeter_cmd)
            if not execResult:
                raise EasyJmeterException('Execute Start slave cmd fail')
            self.slave.status = "RUNNING"
            self.slave.resultMsg = ''
            self.slave.save()
        except EasyJmeterException:
            self.slave.resultMsg = errorMsg
            self.slave.status = "STOP"
            self.slave.save()
            self.stopSlave()
            raise EasyJmeterException(traceback.format_exc())
        except Exception:
            errorMsg = 'Start slave fail,ip:'+self.slave.ip+' reason:'+traceback.format_exc()
            self.slave.resultMsg = errorMsg
            self.slave.status = "STOP"
            self.slave.save()
            self.stopSlave()
            logger.error(errorMsg) 

        



    #stop slave
    def stopSlave(self):
        try:
            slavePid = self.slaveExecutor.execShortTermCmdAndGetResult('ps -ef | grep jmeter | egrep -v grep | awk -F " " \'{print $2}\'')
            if slavePid is None or slavePid == '':
                return
            stopSlaveCmd = 'ps -ef | grep jmeter | egrep -v grep | awk -F " " \'{print $2}\' | xargs kill -s 9'
            execResult = self.slaveExecutor.execCmdMuteStdout(stopSlaveCmd)
            if execResult:
                self.slave.status = "STOP"
                self.slave.save()
                self.slaveExecutor.closeConnection()
                self.slaveExecutor = None
        except Exception:
            errorMsg = "Stop slave fail,ip:"+self.slave.ip+" reason:"+traceback.format_exc()
            logger.error(errorMsg)

    # clear slave process
    def clearSlaveProcess(self):
        try:
            slavePid = self.slaveExecutor.execShortTermCmdAndGetResult('ps -ef | grep jmeter | egrep -v grep | awk -F " " \'{print $2}\'')
            if slavePid is None or slavePid == '':
                return
            stopSlaveCmd = 'ps -ef | grep jmeter | egrep -v grep | awk -F " " \'{print $2}\' | xargs kill -s 9'
            self.slaveExecutor.execCmdMuteStdout(stopSlaveCmd)
        except Exception:
            errorMsg = "Stop slave fail,ip:"+self.slave.ip+" reason:"+traceback.format_exc()
            logger.error(errorMsg)

