from django.db import models
import django.utils.timezone as timezone
from django.core.validators import *
from core.validator import *
from django.forms import ModelForm

# Create your models here.

#Jmeter Slave
class Slave(models.Model):
    code = models.CharField(max_length=64,null=True) 
    ip = models.GenericIPAddressField(
        null=True,
        validators=[validate_empty_str]) 
    port = models.IntegerField(null=True)
    status = models.CharField(max_length=16,null=True)
    clusterCode = models.CharField(
        max_length=64,
        null=True,
        validators=[validate_empty_str])
    delStatus = models.BooleanField(default=False)
    userName = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str])
    password = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str])
    resultMsg = models.TextField(
        null=True)
    jmeterPath = models.CharField(
        max_length=100,
        null=True,
        validators=[validate_empty_str])
    
    

class SlaveForm(ModelForm):
    class Meta:
        model = Slave
        fields = ('ip','port','clusterCode','userName','password','jmeterPath')      #字段，如果是__all__,就是表示列出所有的字段
        exclude = None         #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = {
            'ip':{'required':"IP地址不能为空",},
            'clusterCode':{'required':"集群编码不能为空",},
            'userName':{'required':"用户名不能为空",},
            'password':{'required':"密码不能为空",},
            'jmeterPath':{'required':"Jmeter部署路径为空"}
        }

#集群，一个集群可以包含多个Jmeter的slave
class Cluster(models.Model):
    code = models.CharField(
        max_length=64,
        null=True
        )
    clusterName = models.CharField(max_length=32,
        null=True,
        validators=[validate_empty_str]
        )
    description = models.CharField(max_length=1000,null=True)
    delStatus = models.BooleanField(default=False)

class ClusterForm(ModelForm):
    class Meta:
        model = Cluster
        fields = ('clusterName','description')      #字段，如果是__all__,就是表示列出所有的字段
        exclude = None         #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = {
            'clusterName':{'required':"集群名称不能为空",},
        }

#master,master能控制slave进行压测
class Master(models.Model):
    code = models.CharField(max_length=64,null=True)
    masterName = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str])
    ip = models.GenericIPAddressField(
        null=True,
        validators=[validate_empty_str])
    port = models.IntegerField()
    status = models.CharField(
        max_length=16,
        null=True,
        default='stop')
    userName = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str])
    password = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str])
    description = models.CharField(max_length=1000,null=True)
    delStatus = models.BooleanField(default=False)
    clusterCode = models.CharField(
        max_length=64,
        null=True,
        validators=[validate_empty_str])
    resultMsg = models.TextField(
        null=True,
        validators=[validate_empty_str])
    jmeterPath = models.CharField(
        max_length=100,
        null=True,
        validators=[validate_empty_str])

class MasterForm(ModelForm):
    class Meta:
        model = Master
        fields = ('masterName','ip','port','userName','password','jmeterPath')      #字段，如果是__all__,就是表示列出所有的字段
        exclude = None         #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = {
            'masterName':{'required':"Master名称不能为空",},
            'ip':{'required':"IP地址不能为空",},
            'port':{'required':"端口不能为空",},
            'userName':{'required':"账号不能为空",},
            'password':{'required':"密码不能为空",},
            'jmeterPath':{'required':"Jmeter部署路径为空"}
        }

#任务
class Task(models.Model):
    code = models.CharField(max_length=64,null=True)
    taskName = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str],
        )
    description = models.CharField(max_length=1000,null=True)
    userCode = models.CharField(
        max_length=64,
        null=True,
        validators=[validate_empty_str],)
    status = models.CharField(max_length=16,null=True,default='stop')
    createTime = models.DateTimeField(default = timezone.now)
    modifyTime = models.DateTimeField(default = timezone.now)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('taskName','description','userCode')      #字段，如果是__all__,就是表示列出所有的字段
        exclude = None         #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = {
            'taskName':{'required':"任务名称不能为空",},
            'userCode':{'required':"用户编码不能为空",},
        }

class Script(models.Model):
    code = models.CharField(max_length=64,null=True)
    scriptName = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str])
    description = models.CharField(max_length=1000,null=True)
    content = models.TextField(
        null=True,
        validators=[validate_empty_str])
    userCode = models.CharField(
        max_length=64,
        null=True,
        validators=[validate_empty_str])

class ScriptForm(ModelForm):
    class Meta:
        model = Script
        fields = ('scriptName','userCode')      #字段，如果是__all__,就是表示列出所有的字段
        exclude = None         #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = {
            'scriptName':{'required':"脚本名称不能为空",},
            'userCode':{'required':"用户编码不能为空",},
        }

class JmeterScriptParameter(models.Model):

    code = models.CharField(max_length=64,null=True)
    scriptCode = models.CharField(max_length=64,null=True)
    planName = models.CharField(
        max_length=24,
        null=True,
        validators=[validate_empty_str])
    httpSampleName = models.CharField(
        max_length=24,
        null=True,
        validators=[validate_empty_str])
    domain = models.CharField(
        max_length=64,
        null=True,
        validators=[validate_empty_str])
    port = models.IntegerField()
    path = models.CharField(
        max_length=64,
        null=True,
        validators=[validate_empty_str])
    method = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str])
    loopCount = models.IntegerField()
    threadGroupName = models.CharField(
        max_length=64,
        null=True,
        validators=[validate_empty_str])
    threadNumber = models.IntegerField()
    rampUp = models.IntegerField()
    scheduler = models.CharField(
        max_length=16,
        null=True,
        validators=[validate_empty_str])
    duration = models.IntegerField()
    httpParameter = models.TextField(
        null=True)

class JmeterScriptParameterFrom(ModelForm):
    class Meta:
        model = JmeterScriptParameter
        fields = ('planName','httpSampleName','domain','port','path','method','loopCount','threadGroupName','threadNumber','rampUp','duration','scheduler')      #字段，如果是__all__,就是表示列出所有的字段
        exclude = None         #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = {
            'planName':{'required':"脚本名称不能为空",},
            'httpSampleName':{'required':"HTTP采样器名称不能为空",},
            'domain':{'required':"请求地址不能为空",},
            'path':{'required':"上下文路径不能为空",},
            'method':{'required':"请求方法不能为空",},
            'threadGroupName':{'required':"线程组名称不能为空",}
        }
