from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from core.models import *
from core.EasyJmeterException import EasyJmeterException
from core.util import *
from core.JmxMaker import *
from django.forms import modelform_factory
import json,logging,re,datetime
from django.forms.models import model_to_dict
from django.db import transaction


logger = logging.getLogger('easyjmeter.core.views')

from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html', {})

def room(request, room_name):
    return render(request, 'core/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

@csrf_exempt
#添加集群
def add_cluser(request):
    try:
        cluster = Cluster()
        form = ClusterForm(request.POST,instance=cluster)
        if form.is_valid():
            code = getCode("cluster")
            cluster.code = code
            cluster.save()
            logger.debug('添加集群成功')
            return getSuccessHttpResponse(True,"success")
        else:
            return getSuccessHttpResponse(False,form.errors)
    except Exception as e:
        logger.error('添加集群失败，失败原因:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
#修改集群
def modify_cluster(request):
    try:
        modify_cluster = Cluster()
        form = ClusterForm(request.POST,instance=modify_cluster)
        if form.is_valid():
            code = request.POST.get('code','').strip()
            existCluster = Cluster.objects.get(code=code)
            if isNone(existCluster,logger,"集群",code):
                return getSuccessHttpResponse(False,"集群不存在")
            existCluster.clusterName = modify_cluster.clusterName
            existCluster.description = modify_cluster.description
            existCluster.save()
            logger.debug('修改集群成功')
            return getSuccessHttpResponse(True,"修改集群成功")
        else:
            return getSuccessHttpResponse(False,form.errors)
    except Exception as e:
        logger.error('修改集群失败:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
#删除集群
def del_cluster(request):
    try:
        code = request.POST.get('code','').strip()
        existCluster = cluster.objects.get(code=code)
        if isNone(existCluster,logger,"集群",code):
            return getSuccessHttpResponse("false","集群不存在")
        existCluster = Cluster.objects.get(code=code)
        existCluster.delStatus = True
        existCluster.save()
        return getSuccessHttpResponse("true","删除集群成功")
    except Exception as e:    
        logger.error('删除集群失败:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
#添加Master
def add_master(request):
    try:
        master = Master()
        form = MasterForm(request.POST,instance=master)
        if form.is_valid():
            code = getCode("master")
            master.code = code
            master.status = 'STOP'
            master.save()
            logger.debug('添加Master成功')
            return getSuccessHttpResponse("true","添加Master成功")
        else:
           return getSuccessHttpResponse(False,form.errors) 
    except Exception as e:
        logger.error('添加Master失败,失败原因:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
#修改Master
def modify_master(request):
    try:
        modify_master = Master()
        form = MasterForm(request.POST,instance=modify_cluster)
        if form.is_valid():
            code = request.POST.get('code','').strip()
            existMaster = Master.objects.get(code=code)
            if isNone(existMaster,logger,"Master",code):
                return getSuccessHttpResponse(False,"Master不存在")
            existMaster.clusterName = modify_master.masterName
            existMaster.ip = modify_master.ip
            existMaster.port = modify_master.port
            existMaster.description = modify_master.description
            existMaster.save()
            logger.debug('修改Master成功')
            return getSuccessHttpResponse(True,"修改Master成功")
        else:
            return getSuccessHttpResponse(False,form.errors)
    except Exception as e:
        logger.error('修改Master失败:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
#删除master
def del_master(request):
    try:
        code = request.POST.get('code','').strip()
        existMaster =  Master.objects.get(code=code)
        if isNone(existMaster,logger,"Master",code):
            return getSuccessHttpResponse("false","Master不存在")
        existMaster.delStatus = True
        existMaster.delete()
        return getSuccessHttpResponse("true","删除成功")
    except Exception as e:    
        logger.error('删除Master失败:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
#添加SLAVE
def add_slave(request):
    try:
        slave = Slave()
        form = SlaveForm(request.POST,instance=slave)
        if form.is_valid():
            code = getCode("slave")
            slave.code = code
            slave.status = 'STOP'
            slave.save()
            logger.debug('添加SLAVE成功')
            return getSuccessHttpResponse(True,'添加SLAVE成功')
        else:
            return getSuccessHttpResponse(False,form.errors)
    except Exception as e:
        logger.error('添加Slave失败,失败原因:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
def modify_slave(request):
    try:
        modify_slave = Slave()
        form = SlaveForm(request.POST,instance=modify_slave)
        if form.is_valid():
            code = request.POST.get('code','').strip()
            existSlave = Slave.objects.get(code=code)
            if isNone(existSlave,logger,"Slave",code):
                return getSuccessHttpResponse(False,"Slave不存在")
            existSlave.clusterName = modify_slave.clusterCode
            existSlave.ip = modify_slave.ip
            existSlave.port = modify_slave.port
            existSlave.save()
            logger.debug('修改Slave成功')
            return getSuccessHttpResponse(True,"修改Slave成功")
        else:
            return getSuccessHttpResponse(False,form.errors)
    except Exception as e:
        logger.error('添加Slave失败:'+format(e))
        return getErrorHttpResponse()
@csrf_exempt
def del_slave(request):
    try:
        code = request.POST.get('code','').strip()
        existSlave = Slave.objects.get(code=code)
        if isNone(existSlave,logger,"Slave",code):
            return getSuccessHttpResponse("false","Slave不存在")
        existSlave.delStatus = True
        existSlave.save()
        return getSuccessHttpResponse("true","删除成功")
    except Exception as e:    
        logger.error('删除Slave失败:'+format(e))
        return getErrorHttpResponse()




@csrf_exempt
def add_task(request):
    try:
        task = Task()
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            code = getCode("task")
            task.code = code
            task.save()
            logger.debug('添加任务成功')
            return getSuccessHttpResponse(True,'添加任务成功')
        else:
            return getSuccessHttpResponse(False,form.errors)
    except Exception as e:
        logger.error('添加任务失败，原因是:'+format(e))
        return getErrorHttpResponse()
@csrf_exempt
def modify_task(request):
    try:
        modify_task = Task()
        form = TaskForm(request.POST,instance=modify_task)
        if form.is_valid():
            code = request.POST.get('code','').strip()
            existTask = Task.objects.get(code=code)
            if isNone(existTask,logger,"任务",code):
                return getSuccessHttpResponse(False,"任务不存在")
            existTask.taskName = modify_task.taskName
            existTask.description = modify_task.description
            existTask.userCode = modify_task.userCode
            existTask.modifyTime = datetime.datetime.now()
            existTask.save()
            logger.debug('修改任务成功')
            return getSuccessHttpResponse(True,"修改任务成功")
        else:
            return getSuccessHttpResponse(False,form.errors)
    except Exception as e:
        logger.error('修改任务失败，失败原因:'+format(e))
        return getErrorHttpResponse()
@csrf_exempt
def del_task(request):
    from django.db import transaction
    
    try:
        code = request.POST.get('code','').strip()
        existTask = Task.objects.get(code=code)
        taskRuntime = TaskRuntime.objects.get(taskCode = code)
        if isNone(existTask,logger,"Task",code):
            return getSuccessHttpResponse("false","任务不存在")
        if existTask.status == "running":
            logger.error('任务还在执行，无法进行删除')
            return getSuccessHttpResponse("false","任务还在执行，无法进行删除")
        with transaction.atomic():
            existTask.delete()
            taskRuntime.delete()
        return getSuccessHttpResponse("true","删除任务成功")
    except Exception as e:    
        logger.error('删除任务失败,失败原因:'+format(e))
        return getErrorHttpResponse()


@csrf_exempt
def add_script(request):
    try:
        requestDict = json.loads(request.body)
        scriptName = requestDict.get("scriptName")
        if scriptName == '' or scriptName is None:
            raise EasyJmeterException("scriptName should not be null or empty")
        userCode = requestDict.get("userCode")
        if userCode == '' or userCode is None:
            raise EasyJmeterException("userCode should not be null or empty")
        script = Script()
        script.scriptName = scriptName
        script.userCode = userCode
        scriptCode = getCode("script")
        script.code = scriptCode
        requestDict.pop("scriptName")
        requestDict.pop("userCode")
        jmxMaker = JmxMaker()
        scriptParameter = JmeterScriptParameter()
        scriptContent = jmxMaker.createSimpleJmeterScript(requestDict,scriptParameter)
        script.content = scriptContent
        setScriptParameter(requestDict)
        scriptParameter.code = getCode("ScriptParameter")
        scriptParameter.scriptCode = scriptCode
        with transaction.atomic():
            scriptParameter.save()
            script.save()
        logger.debug('添加脚本成功')
        return getSuccessHttpResponse(True,'添加脚本成功')      
    except Exception as e:
        logger.error('添加脚本失败,失败原因:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
def modify_script(request):
    try:
        requestDict = json.loads(request.body)
        scriptCode = requestDict.get("scriptCode")
        scriptParameterCode = requestDict.get("scriptParameterCode")
        existScript = Script.objects.get(code=scriptCode)
        if isNone(existScript,logger,"脚本",scriptCode):
                return getSuccessHttpResponse(False,"脚本不存在")
        existJmeterScriptParameter = JmeterScriptParameter.objects.get(code=scriptParameterCode)
        if isNone(existJmeterScriptParameter,logger,"脚本参数",scriptParameterCode):
                return getSuccessHttpResponse(False,"脚本参数不存在")
        scriptName = requestDict.get("scriptName")
        if scriptName == '' or scriptName is None:
            raise EasyJmeterException("scriptName should not be null or empty")
        userCode = requestDict.get("userCode")
        if userCode == '' or userCode is None:
            raise EasyJmeterException("userCode should not be null or empty")
        existScript.scriptName = scriptName
        existScript.userCode = userCode
        requestDict.pop("scriptName")
        requestDict.pop("userCode")
        jmxMaker = JmxMaker()
        scriptContent = jmxMaker.createSimpleJmeterScript(requestDict)
        existScript.content = scriptContent
        setScriptParameter(requestDict,existJmeterScriptParameter)
        with transaction.atomic():
            existScript.save()
            existJmeterScriptParameter.save()
        logger.debug('添加更新成功')
        return getSuccessHttpResponse(True,'添加更新成功')
    except Exception as e:
        logger.error('更新脚本失败,失败原因:'+format(e))
        return getErrorHttpResponse()
    

@csrf_exempt
def del_script(request):
    try:
        scriptCode = request.POST.get('code','').strip()
        existScript = Script.objects.get(code=scriptCode)
        if isNone(existScript,logger,"脚本",scriptCode):
            return getSuccessHttpResponse("false","脚本不存在")
        existJmeterScriptParameter = JmeterScriptParameter.objects.get(scriptCode=scriptCode)
        if isNone(existJmeterScriptParameter,logger,"脚本参数",scriptCode):
            return getSuccessHttpResponse(False,"脚本参数不存在")
        with transaction.atomic():
            existScript.delete()
            existJmeterScriptParameter.delete()
    except Exception as e:
        logger.error('删除的模板出错了:'+format(e))
        return getErrorHttpResponse()

@csrf_exempt
def add_script_upload(request):
    try:
        scriptName = request.POST.get('scriptName','').strip()
        if scriptName == '' or scriptName is None:
                raise EasyJmeterException("scriptName should not be null or empty")
        userCode = request.POST.get('userCode','').strip()
        if userCode == '' or userCode is None:
            raise EasyJmeterException("userCode should not be null or empty")

        jmxFile = request.FILES.get('jmxFile')
        script = Script()
        script.scriptName = scriptName
        script.userCode = userCode
        scriptCode = getCode("script")
        script.code = scriptCode
        script.content = jmxFile
        script.save()
    except Exception as e:
        logger.error('添加脚本出错:'+format(e))
        return getErrorHttpResponse()
    






def setScriptParameter(requestDict,scriptParameter):

    planName = requestDict.get('planName')
    if planName == '' or planName is None:
        raise EasyJmeterException("planName should not be null or empty")
    scriptParameter.planName = planName

    httpSampleName = requestDict.get('httpSampleName')
    if httpSampleName == '' or httpSampleName is None:
        raise EasyJmeterException("httpSampleName should not be null or empty")
    scriptParameter.httpSampleName = httpSampleName

    domain = requestDict.get('domain')
    if domain == '' or domain is None:
        raise EasyJmeterException("domain should not be null or empty")
    scriptParameter.domain = domain

    port = requestDict.get('port')
    if port == '' or port is None:
        raise EasyJmeterException("port should not be null or empty")
    scriptParameter.port = port

    path = requestDict.get('path')
    if path == '' or path is None:
        raise EasyJmeterException("path should not be null or empty")
    scriptParameter.path = path

    method = requestDict.get('method')
    if method == '' or method is None:
        raise EasyJmeterException("method should not be null or empty")
    scriptParameter.method = method

    loopCount = requestDict.get('loopCount')
    if loopCount == '' or loopCount is None:
        raise EasyJmeterException("loopCount should not be null or empty")
    scriptParameter.loopCount = loopCount

    threadGroupName = requestDict.get('threadGroupName')
    if threadGroupName == '' or threadGroupName is None:
        raise EasyJmeterException("threadGroupName should not be null or empty")
    scriptParameter.threadGroupName = threadGroupName

    threadNumber = requestDict.get('threadNumber')
    if threadNumber == '' or threadNumber is None:
        raise EasyJmeterException("threadNumber should not be null or empty")
    scriptParameter.threadNumber = threadNumber

    rampUp = requestDict.get('rampUp')
    if rampUp == '' or rampUp is None:
        raise EasyJmeterException("rampUp should not be null or empty")
    scriptParameter.rampUp = rampUp

    scheduler = requestDict.get('scheduler')
    if scheduler == '' or scheduler is None:
        raise EasyJmeterException("scheduler should not be null or empty")
    scriptParameter.scheduler = scheduler

    duration = requestDict.get('duration')
    if duration == '' or duration is None:
        raise EasyJmeterException("duration should not be null or empty")
    scriptParameter.duration = duration

    httpParameter = requestDict.get('httpParameter')
    if httpParameter == '' or httpParameter is None:
        raise EasyJmeterException("httpParameter should not be null or empty")
    scriptParameter.httpParameter = httpParameter



