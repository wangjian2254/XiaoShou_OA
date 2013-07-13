#coding=utf-8
# Create your views here.
import json

import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import QianDao, UserQianDao, Office, Person, Depatement
from xiaoshou_oa.tools import getResult, permission_required
from django.contrib.auth.models import User


@login_required
@permission_required
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
@permission_required
def check_qiandao(request):
    name = request.REQUEST.get('name')
    if name:
        count = QianDao.objects.filter(name=name).count()
        if count>0:
            return getResult(False,u'名称已经注册过了')
        else:
            return getResult(True,u'名称可用')

@login_required
@permission_required
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
@permission_required
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
@permission_required
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
@permission_required
def qiandaoList(request):
    return render_to_response('oa/qiandaoList.html', RequestContext(request, {'qiandaolist': QianDao.objects.all()}))

@login_required
@permission_required
def qiandaoListJson(request):
    l = []
    for qiandao in QianDao.objects.all():
        if qiandao.isdel:
            l.append({'id':qiandao.id, 'isdel':qiandao.isdel})
        else:
            l.append({'id':qiandao.id, 'name':qiandao.name, 'needTime':qiandao.needTime, 'needGPS':qiandao.GPS, 'needAddress':qiandao.needAddress, 'isdel':qiandao.isdel})

    return getResult(True, u'更新签到服务成功', l)

@login_required
@permission_required
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
    else:
        return getResult(False,u'请选择签到厅台信息')
    userQianDao.save()
    return getResult(True, u'提交签到信息成功')



def getUserByDepartment(users,depatelist=[]):
    u=[]
    for user in users:
        if user.department_manager and user.department_manager.pk not in depatelist:
            for p in Person.objects.filter(depate=user.department_manager):
                u.append(p.user)
                depatelist.append(user.department_manager.pk)
    return u


@login_required
@permission_required
def userQianDaoList(request):
    return render_to_response('oa/userqiandaoList.html', RequestContext(request, { 'depatementlist':Depatement.objects.all(), 'qiandaolist':QianDao.objects.all(), 'today':datetime.datetime.now()}))


@login_required
@permission_required
def userQianDaoQuery(request):
    '''
    查询用户签到信息

    '''
    userid = request.REQUEST.get('userid')
    qiandaoid = request.REQUEST.get('qiandaoid')
    startdate = request.REQUEST.get('startdate')
    enddate = request.REQUEST.get('enddate')
    if not startdate or not enddate:
        raise Http404
    startdate = datetime.datetime.strptime(startdate+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    enddate = datetime.datetime.strptime(enddate+' 23:59:59', '%Y-%m-%d %H:%M:%S')
    if userid:
        user=User.objects.get(pk=userid)
        users=[user]
        d=[]
        for i in range(5):
            u=getUserByDepartment(users,d)
            users.extend(u)
    else:
        users=User.objects.all()
    if qiandaoid:
        qiandao = QianDao.objects.get(pk = id)
    else:
        raise Http404
    query = UserQianDao.objects.filter(user__in=users).filter(qiandao=qiandao)
    query = query.filter(dateTime__gte=startdate).filter(dateTime__lte=enddate)
    query = query.order_by('dateTime').order_by('office').order_by('user')

    dategroup=[]
    datedict={}
    dateformate='%Y-%m-%d %H:%M:%S'
    date=None
    for uqd in query:
        date = uqd.dateTime.strftime(dateformate)
        if not datedict.has_key(date):
            datedict[date]=[]
            dategroup.append({'date':date, 'query':datedict[date]})
        datedict[date].append(uqd)


    return render_to_response('oa/userqiandaoListPage.html', RequestContext(request, {'query': dategroup}))








