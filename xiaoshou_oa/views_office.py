#coding=utf-8
# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import  Office, Depatement
from xiaoshou_oa.tools import getResult
from django.contrib.auth.models import User



@login_required
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

    else:
        office = Office()
    office.name=name
    office.flag=flag
    if gps:
        office.gps=gps
    if address:
        office.address=address
    office.save()

    return getResult(True,u'操作成功')

@login_required
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
def officeList(request):
    return render_to_response('oa/officeList.html',RequestContext(request,{'officelist':Office.objects.all()}))

def officeUploadGPS(request):
    username = request.REQUEST.get('username')
    password = request.REQUEST.get('password')

    if username and password:
        user = User.objects.filter(username=username)[:1]
        if len(user)>0:
            user=user[0]
            count = Depatement.objects.filter(manager=user).count()
            if count==0:
                getResult(False,u'不具备权限')
        else:
            return getResult(False,u'不具备权限')

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

