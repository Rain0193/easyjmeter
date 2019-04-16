import paramiko
import threading
import logging
import json
import traceback
from core.EasyJmeterException import *


logger = logging.getLogger('easyjmeter.core.executor')



class Executor:


    def __init__(self, ip, port,userName,password,clientTerminal):
        self.ip = ip
        self.port = port
        self.userName = userName
        self.password = password
        self.clientTerminal = clientTerminal
        self.__init_connection()
    
    def __init_connection(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, port=self.port, username=self.userName, password=self.password)


    # execute short term cmd and first deal with error and return execResult and stdout
    def execShortTermCmd(self,cmd):
        _,stdout,stderr = self.ssh.exec_command(cmd)
        errLine = stderr.readline()
        execResult = True
        while errLine:
            if execResult:
                execResult = False
            self.clientTerminal.send(text_data=json.dumps({
                'message': "std_error: "+ errLine
            }))
            errLine = stderr.readline()
        return execResult,stdout


        
    # execute long term cmd and return stdout and stderr
    def execLongTermCmd(self,cmd):
        _,stdout,stderr = self.ssh.exec_command(cmd)
        return stdout,stderr

    
    # execute cmd and mute stdout and return the execResult
    def execCmdMuteStdout(self,cmd):
        cmd += ' 1>/dev/null'
        _,_,stderr = self.ssh.exec_command(cmd)
        errline = stderr.readline()
        exec_result = True
        while errline:
            if exec_result:
                exec_result = False
            self.clientTerminal.send(text_data=json.dumps({
                'message': "std_error: "+ errline
            }))
            errline = stderr.readline()
        return exec_result


    # exec short term cmd and get result
    def execShortTermCmdAndGetResult(self,cmd):
        _,stdout,stderr = self.ssh.exec_command(cmd)
        errline = stderr.readline()
        execResult = True
        while errline:
            if execResult:
                execResult = False
                break
        if execResult:
            result = stdout.read().decode()
            return result    
        else:
            return execResult


        




    def closeConnection(self):
        self.ssh.close()
        self.ssh = None

    # upload file
    def uploadFile(self,source,target):
        try:
            t = paramiko.Transport((self.ip, self.port))
            t.connect(username=self.userName, password = self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(source,target)
            sftp.close()
        except Exception as e:
            msg = traceback.format_exc()
            logger.error(str(e))
            raise EasyJmeterException("Upload file fail,reason:"+msg)

        

    # upload file
    def downloadFile(self,source,target):
        try:
            t = paramiko.Transport((self.ip, self.port))
            t.connect(username=self.userName, password = self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.get(source,target)
            sftp.close()
        except Exception as e:
            msg = traceback.format_exc()
            logger.error(str(e))
            raise EasyJmeterException("Donwload file fail,reason:"+msg)
        


        

    #return the ip of the connection
    def getIp(self):
        return self.ip
    #return the port of the connection
    def getPort(self):
        return self.port

    