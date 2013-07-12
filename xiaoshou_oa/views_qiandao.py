#coding=utf-8
# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import QianDao, UserQianDao, Office
from xiaoshou_oa.tools import getResult
from django.contrib.auth.models import User


@login_required
def qiandaoAdd(request):
    '''
    添加、修改用户信息
    离职用户
    '''
    id = request.REQUEST.get('qiandaoid')
    qiandao = {}
    if id:
        qiandao = QianDao.objects.get(pk=id)
    return render_to_response('oa/qiandaoSave.html', RequestContext(request, {'qiandao': qiandao}))

@login_required
def check_qiandao(request):
    name = request.REQUEST.get('name')
    if name:
        count = QianDao.objects.filter(name=name).count()
        if count>0:
            return getResult(False,u'名称已经注册过了')
        else:
            return getResult(True,u'名称可用')

@login_required
def qiandaoSave(request):
    '''
    保存用户信息
    '''
    id = request.REQUEST.get('qiandaoid')
    name = request.REQUEST.get('name')
    needgps = request.REQUEST.get('needgps')
    needaddress = request.REQUEST.get('needaddress')
    needtime = request.REQUEST.get('needtime')

    if id:
        qiandao = QianDao.objects.get(pk=id)
        msg=u'修改签到服务成功'
    else:
        qiandao = QianDao()
        msg=u'添加签到服务成功'
    qiandao.name = name
    if needgps=='1':
        qiandao.needGPS = True
    else:
        qiandao.needGPS = False
    if needaddress=='1':
        qiandao.needAddress = True
    else:
        qiandao.needAddress = False
    if needtime=='1':
        qiandao.needTime = True
    else:
        qiandao.needTime = False

    qiandao.save()

    return getResult(True, msg, qiandao.id)


@login_required
def qiandaoDelete(request):
    '''
    离职用户
    '''
    id = request.REQUEST.get('qiandaoid')
    if id:
        try:
            qiandao = QianDao.objects.get(pk=id)

            qiandao.isdel = True
            qiandao.save()
            return getResult(True, u'删除签到服务成功')
        except:
            return getResult(False, u'签到服务不存在')
    return getResult(False, u'请传递签到服务id')

@login_required
def qiandaoOpen(request):
    '''
    离职用户
    '''
    id = request.REQUEST.get('qiandaoid')
    if id:
        try:
            qiandao = QianDao.objects.get(pk=id)

            qiandao.isdel = False
            qiandao.save()
            return getResult(True, u'开通签到服务成功')
        except:
            return getResult(False, u'签到服务不存在')
    return getResult(False, u'请传递签到服务id')


@login_required
def qiandaoList(request):
    return render_to_response('oa/qiandaoList.html', RequestContext(request, {'qiandaolist': QianDao.objects.all()}))

@login_required
def qiandaoListJson(request):
    l = []
    for qiandao in QianDao.objects.all():
        if qiandao.isdel:
            l.append({'id':qiandao.id, 'isdel':qiandao.isdel})
        else:
            l.append({'id':qiandao.id, 'name':qiandao.name, 'needTime':qiandao.needTime, 'needGPS':qiandao.GPS, 'needAddress':qiandao.needAddress, 'isdel':qiandao.isdel})

    return getResult(True, u'更新签到服务成功', l)

@login_required
def userqiandaoUpload(request):
    '''
    手机端提交签到信息
    '''
    user=request.user
    id = request.REQUEST.get('qiandaoid')
    if id:
        try:
            qiandao = QianDao.objects.get(pk=id)
        except:
            return getResult(False, u'签到服务不存在')
    else:
        return getResult(False, u'请传递签到服务id')
    gps = request.REQUEST.get('gps')
    address = request.REQUEST.get('address')
    officeid = request.REQUEST.get('officeid')
    userQianDao = UserQianDao()
    userQianDao.user = user
    userQianDao.qiandao = qiandao
    if gps:
        userQianDao.gps = gps
    if address:
        userQianDao.address = address
    if officeid:
        userQianDao.office=Office.objects.get(pk=officeid)
    userQianDao.save()
    return getResult(True, u'提交签到信息成功')

