# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^cluster/add$', views.add_cluser, name='cluster_add'),
    url(r'^cluster/modify$', views.modify_cluster, name='cluster_modify'),
    url(r'^cluster/del$', views.del_cluster, name='cluster_del'),
    url(r'^master/add$', views.add_master, name='master_add'),
    url(r'^master/modify$', views.modify_master, name='master_modify'),
    url(r'^master/del$', views.del_master, name='master_del'),
    url(r'^slave/add$', views.add_slave, name='slave_add'),
    url(r'^slave/modify$', views.modify_slave, name='slave_modify'),
    url(r'^slave/del$', views.del_slave,name='slave_del'),
    url(r'^task/add$', views.add_task, name='task_add'),
    url(r'^task/modify$', views.modify_task, name='task_modify'),
    url(r'^task/del$', views.del_task, name='task_del'),
    url(r'^script/add$', views.add_script, name='script_add'),
    url(r'^script/modify$', views.modify_script, name='script_modify'),
    url(r'^script/del$', views.del_script, name='script_del'),
]