#coding=utf-8
# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import Person, Depatement
from xiaoshou_oa.tools import getResult



@login_required
def depatementAdd(request):
    '''
    添加、修改用户信息
    离职用户
    '''
    id=request.REQUEST.get('depatementid')
    depatement={}
    if id:
        depatement=Depatement.objects.get(pk=id)
        personquery=Person.objects.filter(depate=depatement)
        userlist=User.objects.filter(person__in=personquery)
    return render_to_response('oa/depatementSave.html',RequestContext(request,{'depatement':depatement,'userlist':userlist, 'userall':User.objects.all()}))

@login_required
def depatementSave(request):
    '''
    保存用户信息
    '''
    id = request.REQUEST.get('depatementid')
    name = request.REQUEST.get('name')
    depatementfatherid = request.REQUEST.get('depatementfatherid')
    userid = request.REQUEST.get('managerid')


    if id:
        depate = Depatement.objects.get(pk=id)

    else:
        depate = Depatement()
    depate.name=name
    depate.save()
    if depatementfatherid:
        depatefather=Depatement.objects.get(pk=depatementfatherid)
        depate.fatherDepart=depatefather
        depate.save()
    if userid:
        user=User.objects.get(pk=id)
        depate.manager=user
        depate.save()
        user.person.depate=depate
        user.person.save()
        user.save()

    return getResult(True,u'操作成功')

@login_required
def depatementDelete(request):
    '''
    离职用户
    '''
    id=request.REQUEST.get('depatementid')
    if id:
        try:
            depate = Depatement.objects.get(pk=id)
            count=Person.objects.filter(depate=depate).count()
            if 0<count:
                return getResult(False,u'该职务还有属下，请先删除该职务底属下员工。')
            depate.isdel=True
            depate.save()
            return getResult(True,u'删除职务成功')
        except:
            return getResult(False,u'职务不存在')
    return getResult(False,u'请传递职务id')


@login_required
def depatementList(request):
    return render_to_response('oa/depatementList.html',RequestContext(request,{'depatementlist':Depatement.objects.all()}))


