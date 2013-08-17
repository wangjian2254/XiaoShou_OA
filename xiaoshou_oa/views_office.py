#coding=utf-8
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import  Office, Depatement, UserQianDao
from xiaoshou_oa.tools import getResult, permission_required, client_login_required


import datetime
timezone=datetime.timedelta(hours =8)

@login_required
@permission_required
def officeAdd(request):
    '''
    添加、修改用户信息
    离职用户
    '''
    id=request.REQUEST.get('officeid')
    office={}
    if id:
        office=Office.objects.get(pk=id)
    return render_to_response('oa/officeSave.html',RequestContext(request,{'office':office}))


@login_required
@permission_required
def check_office(request):
    name = request.REQUEST.get('name')
    if name:
        count = Office.objects.filter(name=name).count()
        if count>0:
            return getResult(False,u'名称已经注册过了')
        else:
            return getResult(True,u'名称可用')
    flag = request.REQUEST.get('flag')
    if flag:
        count = Office.objects.filter(flag=flag).count()
        if count>0:
            return getResult(False,u'标记已经被注册过了')
        else:
            return getResult(True,u'标记可用')

@login_required
@permission_required
def officeSave(request):
    '''
    保存用户信息
    '''
    id = request.REQUEST.get('officeid')
    flag = request.REQUEST.get('flag')
    name = request.REQUEST.get('name')
    gps = request.REQUEST.get('gps')
    address = request.REQUEST.get('address')


    if id:
        office = Office.objects.get(pk=id)
        msg=u'修改厅台成功。'
    else:
        office = Office()
        msg=u'添加厅台成功。'
    office.name=name
    office.flag=flag
    if gps:
        office.gps=gps
    if address:
        office.address=address
    try:
        office.save()
    except:
        return getResult(False,u'操作失败，信息不正确')
    return getResult(True,msg ,office.id)

@login_required
@permission_required
def officeDelete(request):
    '''
    离职用户
    '''
    id=request.REQUEST.get('officeid')
    if id:
        try:
            office = Office.objects.get(pk=id)

            office.isdel=True
            office.save()
            return getResult(True,u'删除厅台成功')
        except:
            return getResult(False,u'厅台不存在')
    return getResult(False,u'请传递厅台id')


@login_required
@permission_required
def officeOpen(request):
    '''
    离职用户
    '''
    id=request.REQUEST.get('officeid')
    if id:
        try:
            office = Office.objects.get(pk=id)

            office.isdel=False
            office.save()
            return getResult(True,u'启用厅台成功')
        except:
            return getResult(False,u'厅台不存在')
    return getResult(False,u'请传递厅台id')


@login_required
@permission_required
def officeList(request):
    return render_to_response('oa/officeList.html',RequestContext(request,{'officelist':Office.objects.all()}))


@login_required
@permission_required
def officeUploadGPS(request):
    # username = request.REQUEST.get('username')
    # password = request.REQUEST.get('password')
    user=request.user
    if user:
        # user = User.objects.filter(username=username)[:1]
        # if len(user)>0:
        #     user=user[0]
        count = Depatement.objects.filter(manager=user).count()
        if count==0:
            getResult(False,u'不具备权限')
        # else:
        #     return getResult(False,u'不具备权限')

    flag = request.REQUEST.get('flag')
    id = request.REQUEST.get('officeid')
    if id:
        office=Office.objects.get(pk=id)
    if flag:
        office2=Office.objects.filter(flag=flag)[0]
    if office.id!=office2.id:
        return getResult(False,u'错误的参数')
    gps = request.REQUEST.get('gps')
    address = request.REQUEST.get('address')
    if gps:
        office.gps = gps
    if address:
        office.address = address
    office.save()
    return getResult(True,u'设置厅台gps信息成功')

@login_required
@permission_required
def calculateOffice(request):
    id = request.REQUEST.get('officeid')
    date = request.REQUEST.get('enddate')
    if  not date:
        date = (datetime.datetime.utcnow()+timezone).strftime('%Y-%m-%d')
    startdate = datetime.datetime.strptime(date+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    enddate = datetime.datetime.strptime(date+' 23:59:59', '%Y-%m-%d %H:%M:%S')

    type=request.REQUEST.get('type')
    msg = u''
    result=u''
    if type:
        if type=='1':
            msg=u'设置成功'
            result=u'succeed'

        if type=='2':
            msg=u'设置失败'
            result=u'warning'

    if id:
        office = Office.objects.get(pk=id)
        query = UserQianDao.objects.filter(office=office)
        query = query.filter(dateTime__gte=startdate).filter(dateTime__lte=enddate)
        query = query.order_by('dateTime').order_by('user')
    else:
        office = {}
        query = []

    return render_to_response('oa/officeGPSPage.html', RequestContext(request, {'msg':msg,'result':result, 'query': query, 'office':office, 'today':date, 'officelist':Office.objects.all()}))


@login_required
@permission_required
def setGPSoffice(request):
    officeid = request.REQUEST.get('officeid')
    userqiandaoid = request.REQUEST.get('userqiandaoid')
    if officeid and userqiandaoid:
        try:
            office = Office.objects.get(pk=officeid)
            userqiandao = UserQianDao.objects.get(pk=userqiandaoid)
            office.gps=userqiandao.gps
            office.address=userqiandao.address
            office.save()
            return HttpResponseRedirect('/oa/calculateOffice/?officeid=%s&endate=%s&type=1'%(officeid,userqiandao.dateTime.strftime('%Y-%m-%d')))
        except:
            return HttpResponseRedirect('/oa/calculateOffice/?type=2')
    else:
        return HttpResponseRedirect('/oa/calculateOffice/?type=2')

@client_login_required
def officeListClient(request):
    l = []
    for qiandao in Office.objects.all():
        if qiandao.isdel:
            l.append({'id':qiandao.id, 'isdel':qiandao.isdel})
        else:
            l.append({'id':qiandao.id, 'name':qiandao.name, 'flag':qiandao.flag, 'gps':(qiandao.gps and [qiandao.gps] or [''])[0], 'address':(qiandao.address and [qiandao.address] or [''])[0], 'isdel':qiandao.isdel})

    return getResult(True, u'更新厅台信息成功', l)